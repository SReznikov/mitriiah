#!/usr/bin/env python3

# mitriiah - an umbrella sampling preparation tool.
# Copyright (C) 2018  Sylvia Reznikov
# email contact: s.reznikov@newcastle.ac.uk

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



import sys
import os
import argparse
import signal
import itertools 

from PyQt4 import QtCore, QtGui
import re
import shelve

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

# # from matplotlib.backends.qt_compat import QtCore, QtGui, is_pyqt5
# # if is_pyqt5():
# #     from matplotlib.backends.backend_qt5agg import (
# #         FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
# # else:
# #     from matplotlib.backends.backend_qt4agg import (
# #         FigureCanvas, NavigationToolbar2QT as NavigationToolbar)



from matplotlib.figure import Figure


from graph_window import GraphWindow 
from main_gui_window import MainGuiWindow
from ranges import SelectedRangeList
from selected_points import SelectedPointsList
from selected_residues import SelectedResiduesList
from reply_log import ReplyLog

import app as app


choices=["*.xvg","*.txt","*.gro"] # accepted file extensions

# check if the file has an accepted extension
def CheckExt(choices):
    class Act(argparse.Action):
        def __call__(self,parser,namespace,fname,option_string=None):
            ext = os.path.splitext(fname)[1][1:]
            if ext not in choices:
                option_string = '({})'.format(option_string) if option_string else ''
                parser.error("file doesn't end with one of {}{}".format(choices,option_string))
            else:
                setattr(namespace,self.dest,fname)

    return Act


parser = argparse.ArgumentParser()

parser.add_argument("-r", "--rmsf", dest = 'rmsf_filename', default = "rmsf.xvg", help="rmsf file", action=CheckExt({'xvg','txt'}))
parser.add_argument("-c", "--coords", dest = 'my_gro_filename', default = "protein.gro", help=".gro file used for rmsf", action=CheckExt({'gro'}))

app.args = parser.parse_args()

# Open the rmsf.xvg file and assign residue and rmsf variables
with open(app.args.rmsf_filename) as rmsf:

    index_rmsf_counter = 0
    temp_x_a_res = []
    temp_y_a_rmsf = []

    rmsf_lines = [line.strip() for line in rmsf if not line.startswith(('#', '@'))]

    for line in rmsf_lines:

        cols = line.split()

        if len(cols) == 2:

            temp_x_a_res.append(float(cols[0]))
            temp_y_a_rmsf.append(float(cols[1]))


# Open the given .gro file and assign needed variables (residue/atom values and names)
with open(app.args.my_gro_filename) as gro_file:

    temp_gro_residue_val = []
    temp_gro_residue_name = []
    temp_gro_atom_name = []
    temp_gro_atom_number = []

    prev_item = 0
    current_item = 0
    index_counter = 0


    # load the complex
    for line in gro_file:
        #separate the columns for big files
        first_part = line[:15]
        rest_of_line = line[15:]

        line = str.join(' ', (first_part, rest_of_line))

        cols = line.split()

        # if len(cols) == 9: #number of cols in gro file. will depend if pre or post sim (6 or 9 cols)
        if len(cols) == 9 or len(cols) == 6: #number of cols in gro file. will depend if pre or post sim (6 or 9 cols)

            res_col = cols[0]

            match = re.match(r"([0-9]+)([a-zA-Z]+)", res_col, re.I)
            if match:
                items = match.groups()

                if len(items) == 2:
                    val_col = items[0]
                    res_col = items[1]

            temp_gro_residue_val.append(int(items[0]))
            temp_gro_residue_name.append(str(items[1]))
            temp_gro_atom_name.append(str(cols[1]))
            temp_gro_atom_number.append(int(cols[2]))


ongoing_atom_list = []

def chain_splitter():
    global prev_item
    global current_item
    global index_counter
    global index_rmsf_counter
    global temp_x_a_res
    global temp_y_a_rmsf
    global ongoing_atom_list


    temp_list = []
    temp_rmsf_list = []
    min_max_vals_list = []
    rmsf_vals_list = []
    resvalues = []


    for rv, rn, an, av in zip(temp_gro_residue_val[index_counter::], temp_gro_residue_name[index_counter::], temp_gro_atom_name[index_counter::], temp_gro_atom_number[index_counter::]):

        current_item = rv
        current_atom = av

        diff = abs(current_item - prev_item)


        if av not in ongoing_atom_list:

            if diff == 1 or diff == 0:

                app.chain_list["chain_%s" % app.chain_num]["chain_num"] = app.chain_num

                temp_list.append( {
                        "resval":rv,
                        "resname":rn,
                        "atomname":an,
                        "atomval":av
                         } )

                ongoing_atom_list.append(av)

                prev_item = rv
                index_counter += 1


                app.chain_list["chain_%s" % app.chain_num]["gro_data"] = temp_list


                for rmsf_res, rmsf_val in zip(temp_x_a_res[index_rmsf_counter::], temp_y_a_rmsf[index_rmsf_counter::]):

                    if rmsf_res == rv:

                        temp_rmsf_list.append( {
                                "rmsf_res":rmsf_res,
                                "rmsf_val":rmsf_val
                                 } )

                        index_rmsf_counter += 1

                        resvalues.append(rmsf_res)

                        app.chain_list["chain_%s" % app.chain_num]["rmsf_data"] = temp_rmsf_list
                        app.chain_list["chain_%s" % app.chain_num]["values_r"] = resvalues

                        min_max_vals_list.append(rmsf_res)

                        app.chain_list["chain_%s" % app.chain_num]["min"] = min(app.chain_list["chain_%s" % app.chain_num]["values_r"])
                        app.chain_list["chain_%s" % app.chain_num]["max"] = max(app.chain_list["chain_%s" % app.chain_num]["values_r"])



            if diff > 1:

                prev_item = current_item-1

                app.chain_num += 1

                min_max_vals_list = []

                for n in temp_rmsf_list:

                    rmsf_vals_list.append(n['rmsf_val'])

                chain_splitter()
                break


def user_select():

    for chain in range(app.chain_num+1):
        if chain != 0:

            app.chain_num = chain

            first_res = app.chain_list["chain_%s" % app.chain_num]["min"]
            last_res = app.chain_list["chain_%s" % app.chain_num]["max"]

            print(chain,":", "chain %s" % chain, "- residues", first_res, "to", last_res)


    chain_to_load = int(input("chain to load: "))

    ## restrict the input
    ## link it to the group (print the values from the selected group)

    print("loading " + str(chain_to_load))


    for chain in range(app.chain_num+1):

        if chain != 0:

            if app.chain_list["chain_%s" % chain]["chain_num"] == chain_to_load :

                for line in app.chain_list["chain_%s" % chain_to_load]['gro_data']:
                    # print(line["resval"])
                    app.gro_residue_val.append(line["resval"])
                    app.gro_residue_name.append(line["resname"])
                    app.gro_atom_name.append(line["atomname"])
                    app.gro_atom_number.append(line["atomval"] )

                app.min_res = min(app.gro_residue_val)
                app.max_res = max(app.gro_residue_val)

                app.to_vals.append(str(app.max_res + 1))
                app.from_vals.append(str(app.min_res - 1))


                for line in app.chain_list["chain_%s" % chain_to_load]['rmsf_data']:
                    app.x_a_res.append(line["rmsf_res"])
                    app.y_a_rmsf.append(line["rmsf_val"])


#######################


def signal_handler(signal, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

def main():


    app.qapp = QtGui.QApplication(sys.argv)

    app.main_window = MainGuiWindow()
    app.main_window.move(50, 60)
    app.main_window.resize(1550, 1000)
    app.main_window.setWindowTitle("mitriiah")
    app.main_window.setWindowIcon(QtGui.QIcon("hamster.jpg"))


    app.main_window.show()
    app.main_window.raise_()

    sys.exit(app.qapp.exec_())


# if __name__ == '__main__':
chain_splitter()
user_select()
main()

