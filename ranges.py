#!/usr/bin/env python3

import sys
import os
import argparse

from PyQt4 import QtCore, QtGui
import re


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

#parser.add_argument("-r", "--rmsf", dest = 'rmsf_filename', default = "rmsf.xvg", help="rmsf file", action=CheckExt({'xvg','txt'}))
parser.add_argument("-c", "--coords", dest = 'my_gro_filename', default = "protein.gro", help=".gro file used for rmsf", action=CheckExt({'gro'}))

args = parser.parse_args()



# List of values from gro_file
gro_residue_val, gro_residue_name, gro_atom_name, gro_atom_number = [], [], [], []

# selected_range = [] # residue name+value and atom name+value derived from selected_points

atom_val_list = [] # list of atom numbers obtained from user selection



# Open the given .gro file and assign needed variables (residue/atom values and names)
with open(args.my_gro_filename) as gro_file:

    for line in gro_file:
        
        cols = line.split()

        if len(cols) == 9:
            res_col = cols[0]

            match = re.match(r"([0-9]+)([a-zA-Z]+)", res_col, re.I)
            if match:
                items = match.groups()
                
                if len(items) == 2:
                    val_col = items[0]
                    res_col = items[1]

            gro_residue_val.append(int(items[0]))
            gro_residue_name.append(str(items[1]))
            gro_atom_name.append(str(cols[1]))
            gro_atom_number.append(int(cols[2]))

            # print(gro_residue_name)

# save the chosen atom numbers to a new .ndx file. Also prints the values in the terminal. 
def saving_and_output():
    atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

    print('[your_chosen_atoms]')
    print(atom_val_list_out)
    # main_window.reply_log_object.append("[your_chosen_atoms]")
    # main_window.reply_log_object.append(atom_val_list_out)

    with open("sel_atoms_index.ndx", 'wt') as out:
        out.write( "[ chosen_atoms ]" + '\n')
        out.write( '\n' )
        out.write((atom_val_list_out) + '\n')

#get range
def input_range():
    from_input = input("from value: ")
    to_input = input("to value: ")

    res_range = list(range(int(from_input), int(to_input) + 1))

    selected_range = []

    print(res_range)


    for i in res_range:
        num = i
        # print(num)
        for index, select_res in enumerate(gro_residue_val):
            # print("ok")
            if select_res == num: # check if residue number of our point is in .gro and add other variables to the list

                selected_range.append(
                    {
                        "resval":gro_residue_val[index], 
                        "resname":gro_residue_name[index], 
                        "atomname":gro_atom_name[index], 
                        "atomval":gro_atom_number[index]
                    }
                )
    selected_range = sorted(selected_range, key=lambda item: item["atomval"])

    print(selected_range)  

    atom_val_list = []

    l = 1
    while l == 1 :
        atom_input = input("atom name: ")
        # # print(atom_input)
        # for index, select_atom in enumerate(selected_range):
        #     print(select_atom["atomname"])
        #     if select_atom["atomname"] == atom_input:
        #         selected_atoms.append(
        #             {
        #                 "resval":gro_residue_val[index], 
        #                 "resname":gro_residue_name[index], 
        #                 "atomname":gro_atom_name[index], 
        #                 "atomval":gro_atom_number[index]
        #             }
        #         )

        for item in selected_range:
            # select automatically all defaults
            if item["atomname"] == atom_input:
                if not [point for point in atom_val_list if point == item['atomval']]:
                        atom_val_list.append( item['atomval'])
                        atom_val_list = sorted(atom_val_list, key=lambda item: item)
                # print(atom_input)
                # print(selected_atoms)
            if atom_input == "q":
                l = 0

    atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

    print('[your_chosen_atoms]')
    print(atom_val_list_out)
    # main_window.reply_log_object.append("[your_chosen_atoms]")
    # main_window.reply_log_object.append(atom_val_list_out)

    with open("sel_atoms_index.ndx", 'wt') as out:
        out.write( "[ chosen_atoms ]" + '\n')
        out.write( '\n' )
        out.write((atom_val_list_out) + '\n')

    # print(atom_val_list)

        





input_range()

# saving_and_output()
# select_range()



# # # #get backbone

# # add default atoms to atom_val_list

# self.default_atoms = "CA"

# self.reply_log_object.append(self.default_atoms)

# for item in selected_range:
#     # select automatically all defaults
#     if item["atomname"] == self.default_atoms:
#         self.reply_log_object.append(str(item))
#         # val.setTextColor(QtGui.QColor("red")) 

#         if not [point for point in atom_val_list if point == item['atomval']]:
#                 atom_val_list.append( item['atomval'] )
#                 atom_val_list = sorted(atom_val_list, key=lambda item: item)
