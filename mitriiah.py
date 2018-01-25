#!/usr/bin/env python3

import sys
import os
import argparse

from PyQt4 import QtCore, QtGui
import re
import shelve

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure



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

args = parser.parse_args()



# Data from rmsf.xvg file
x_a_res, y_a_rmsf = [], [] 

# List of selected points
selected_points = [] # residue value and rmsf value from graph selection

selected_points_x = [] # residue value
selected_points_y = [] # rmsf value

# List of values from gro_file
gro_residue_val, gro_residue_name, gro_atom_name, gro_atom_number = [], [], [], []


##RMSF
selected_residues = [] # residue name+value and atom name+value derived from selected_points

atom_val_list = [] # list of atom numbers obtained from user selection

## ranges
ranges_list = {} # dict containing all the chosen ranges
n = 1 # range counter

default_atoms = ["CA", "C", "N", "O"]







# Open the rmsf.xvg file and assign residue and rmsf variables
with open(args.rmsf_filename) as rmsf:

    rmsf_lines = [line.strip() for line in rmsf if not line.startswith(('#', '@'))]

    for line in rmsf_lines:

        cols = line.split()

        if len(cols) == 2:
            x_a_res.append(float(cols[0]))
            y_a_rmsf.append(float(cols[1]))

# Open the given .gro file and assign needed variables (residue/atom values and names)
with open(args.my_gro_filename) as gro_file:

    for line in gro_file:
        
        cols = line.split()

        if len(cols) == 6: #number of cols in gro file. will depend if pre or post sim (6 or 9 cols)
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





# save the chosen atom numbers to a new .ndx file and generate a posres.itp file. Also prints the values in the terminal. 
def saving_and_output():
    #save index
    atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order
    gro_filename = args.my_gro_filename

    print('[your_chosen_atoms]')
    print(atom_val_list_out)
    main_window.reply_log_object.append("[your_chosen_atoms]")
    main_window.reply_log_object.append(atom_val_list_out)

    with open(gro_filename[:-4] + "_atoms_index.ndx", 'wt') as out:
        out.write( "[ chosen_atoms ]" + '\n')
        out.write( '\n' )
        out.write((atom_val_list_out) + '\n')
     
    with open(gro_filename[:-4] + "_posres.itp", 'w') as out:
        out.write( "[ position_restraints ]" + '\n')
        out.write( "; atom  type      fx      fy      fz" + '\n')
        
        '''
            1
           40
          808     1  1000  1000  1000
         1549     1  1000  1000  1000
        23904

        '''

        posre_list = [] # list of renumbered atoms corresponding to selected atoms

        # gro_atom_number_out = (' '.join(str(g) for g in gro_atom_number)) 
        total_atoms = len(gro_atom_number) # total number of atoms in the file
        renum_vals = range(1, total_atoms+1) # new numbering from 1 for posres
        posre_dict = zip(renum_vals, gro_atom_number) # dictionary containing original atom numbers and the corresponding renumbered ones

        # create a new renumbered selected atom list
        for renum, atmnum in posre_dict:
            for atom_val in atom_val_list:
                if atom_val == atmnum:
                    posre_list.append(renum)


        for s in posre_list:
            if s >= 0 and s < 10:
                out.write("     %s     1  1000  1000  1000\n" % s)

            if s >= 10 and s < 100:
                out.write("    %s     1  1000  1000  1000\n" % s)

            if s >= 100 and s < 1000:
                out.write("   %s     1  1000  1000  1000\n" % s)

            if s >= 1000 and s < 10000:
                out.write("  %s     1  1000  1000  1000\n" % s)

            if s >= 10000:
                out.write(" %s     1  1000  1000  1000\n" % s)


def save_variables():
    
    saved_vars = {}
    saved_vars['x_a_res'] = x_a_res
    saved_vars['y_a_rmsf'] = y_a_rmsf
    saved_vars['selected_points'] = selected_points 
    saved_vars['selected_points_x'] = selected_points_x 
    saved_vars['selected_points_y'] = selected_points_y 
    saved_vars['gro_residue_val'] = gro_residue_val
    saved_vars['gro_residue_name'] = gro_residue_name
    saved_vars['gro_atom_name'] = gro_atom_name
    saved_vars['gro_atom_number '] = gro_atom_number 
    saved_vars['selected_residues'] = selected_residues 
    saved_vars['atom_val_list'] = atom_val_list 
    saved_vars['ranges_list'] = ranges_list 
    saved_vars['n'] = n 


    gro_filename = args.my_gro_filename
    my_shelf = shelve.open(gro_filename[:-4] + "_saved_session.out", 'n')

    for key, value in saved_vars.items():

        if not key.startswith('__'):
            try:
                my_shelf[key] = value
            except Exception:
                print('ERROR saving: "%s"' % key)
            
    my_shelf.close()

    print('saved session')
    main_window.reply_log_object.append("session saved")


def open_variables():

    gro_filename = args.my_gro_filename
    my_shelf = shelve.open(gro_filename[:-4] + "_saved_session.out")
    for key in my_shelf:
        globals()[key]=my_shelf[key]

    main_window.graph_object.redraw_graph()
    main_window.selected_points_list_object.add_points()
    main_window.selected_residues_list_object.redraw_res_list() 
    main_window.select_ranges_list_object.redraw_range_list()

    my_shelf.close()

    print("previous session loaded")
    main_window.reply_log_object.append("previous session loaded")



# Points selection on graph:
def add_point_by_mouse(event):

    global selected_points
    global selected_residues

    if event.button == 3: # right mouse button (1 = LMB, 2 = wheel, 3 = RMB)

        if event.xdata == None:
            return

        mx_l = event.xdata - 5 # 5 residues either side from where the mouse was clicked to consider for lowest rmsf
        mx_h = event.xdata + 5
        lowest_point = None # lowest rmsf value 
        x_of_lowest_point = None

        # check if point is within range, set lowest point. 
        for index, curr_point in enumerate(x_a_res):
            if curr_point > mx_l and curr_point < mx_h: # is it within the range?
                
                if lowest_point is None: # did we set the lowest point?
                    lowest_point = y_a_rmsf[index] # just use the first one
                    x_of_lowest_point = x_a_res[index]
                
                if y_a_rmsf[index] < lowest_point: # look for the lowest point
                    lowest_point = y_a_rmsf[index]
                    x_of_lowest_point = x_a_res[index]

        # add the selected lowest point to the list of selected points   
        if not [point for point in selected_points if point['x'] == x_of_lowest_point]:
            if x_of_lowest_point != None and lowest_point != None: 
                selected_points.append({"x":x_of_lowest_point, "y":lowest_point}) # add our lowest point to list of selected points only if residue number isn't already present in the list
                selected_points = sorted(selected_points, key=lambda item: item["x"])

                # for every added point, add corresponding data from .gro file:
                for index, select_res in enumerate(gro_residue_val):
                    if select_res == x_of_lowest_point: # check if residue number of our point is in .gro and add other variables to the list

                        selected_residues.append(
                            {
                                "resval":gro_residue_val[index], 
                                "resname":gro_residue_name[index], 
                                "atomname":gro_atom_name[index], 
                                "atomval":gro_atom_number[index]
                            }
                        )
                        selected_residues = sorted(selected_residues, key=lambda item: item["atomval"])
                    


        # add selected_points (residue value and rmsf value) to the selected_points_list (also displayed)
        
        main_window.selected_points_list_object.add_points()


        #refresh the list display
        main_window.selected_residues_list_object.redraw_res_list() 
        main_window.graph_object.redraw_graph()
    

# Space in which the rmsf figure is drawn
class GraphWindow(QtGui.QDialog):
    def __init__(self, x_a_res, y_a_rmsf):
        super(GraphWindow, self).__init__()

        self.main()
  
        self.redraw_graph()

    # set the drawing space
    def main(self):
        # a figure instance to plot on
        self.figure = Figure(figsize = (5,4))

        # this is the Canvas Widget that displays the `figure`. it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget. it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        # create an axis
        ax = self.figure.add_subplot(111)
        self.ax = ax

        # use the selecter on graph
        cid = self.figure.canvas.mpl_connect('button_press_event', add_point_by_mouse)


    # plot the graph
    def redraw_graph(self):

        self.ax.clear() # discards the old graph

        self.ax.plot(x_a_res,y_a_rmsf, c='k') # plot the rmsf graph

        # plot every selected point
        for point in selected_points:
            self.ax.plot(point['x'],point['y'], c='r', marker='o')

        self.ax.set_title("RMSF")    
        self.ax.set_xlabel('Residue number')
        self.ax.set_ylabel('rmsf (nm)')

        # refresh canvas
        self.canvas.draw()

    # define the keyboard shortcuts
    def keyPressEvent(self, event):

        super(GraphWindow, self).keyPressEvent(event)

        # atom output shortcut
        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list')
            main_window.reply_log_object.append("Saved atom list")

            saving_and_output()

        # quit the program shortcut
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')


            app.quit()

        if event.key() == QtCore.Qt.Key_S:
            save_variables()


        if event.key() == QtCore.Qt.Key_L:
            open_variables()


    # close down all open windows when this one is closed -- is it needed??
    def closeEvent(self, event):
        app.quit()



class ReplyLog(QtGui.QTextEdit):
    def __init__(self):
        super(ReplyLog, self).__init__()

        self.append(" Hello... hamster is running. To start right-click on the graph, or input a range. ")
        self.setReadOnly(True)

    # define the keyboard shortcuts
    # def keyPressEvent(self, event):

    #     super(ReplyLog, self).keyPressEvent(event)

    #     # key_shortcuts(event)

    #     # atom output shortcut
    #     if event.key() == QtCore.Qt.Key_P:
            
    #         print('Saved atom list')
    #         main_window.reply_log_object.append("Saved atom list")

    #         saving_and_output()

    #     # quit the program shortcut
    #     if event.key() == QtCore.Qt.Key_Q:
            
    #         print('Hamster ran out!')

    #         app.quit()

    #     if event.key() == QtCore.Qt.Key_S:
    #         save_variables()


    #     if event.key() == QtCore.Qt.Key_L:
    #         open_variables()




# The window which contains everything - layouts included
class MainGuiWindow(QtGui.QWidget):
    def __init__(self):
        super(MainGuiWindow, self).__init__()

        # instantiate the required objects

        #classes
        graph_object = GraphWindow(x_a_res, y_a_rmsf)
        self.graph_object = graph_object

        selected_points_list_object = SelectedPointsList(selected_points)
        self.selected_points_list_object = selected_points_list_object

        selected_residues_list_object = SelectedResiduesList(selected_residues)
        self.selected_residues_list_object = selected_residues_list_object

        select_ranges_list_object = SelectedRangeList(ranges_list)
        self.select_ranges_list_object = select_ranges_list_object

        reply_log_object = ReplyLog()
        self.reply_log_object = reply_log_object

        

        # functions
        # RMSF
        self.default_atom_selection()
        self.default_atom_deletion()
        self.atom_radiobuttons()

        # Range
        self.range_selection()

        self.atom_selection()
        self.atom_deletion()

        self.atom_range_selection()
        self.atom_range_deletion()

        self.range_radiobuttons()

        # Layout of the program
        self.layouts()

    ######################    
    ## RMSF atom window ##
    ######################

    ## signalboard 
    
    # radiobuttons
    def atom_radiobuttons(self):

        # radiobutton titles
        self.default_button_title = u'Default Atoms'
        self.all_button_title = u'All Atoms'

        # radiobuttons
        self.default_atom_radiobutton = QtGui.QRadioButton(self.default_button_title)
        self.all_atom_radiobutton = QtGui.QRadioButton(self.all_button_title)

    # button states
    def select_atom_btnstate(self):

        if self.default_atom_radiobutton.isChecked() == True:
            self.default_button_clicked()

        if self.all_atom_radiobutton.isChecked() == True:
            self.all_button_clicked()

    def delete_atom_btnstate(self):

        if self.default_atom_radiobutton.isChecked() == True:
            self.default_delete_button_clicked()

        if self.all_atom_radiobutton.isChecked() == True:
            self.all_delete_button_clicked()

    
    ## default atom buttons 
    def default_atom_selection(self):
            
        self.default_atoms_button =  QtGui.QPushButton("Select")
        self.default_atoms_button.setFixedWidth(80)

        self.default_atoms_button.clicked.connect(self.select_atom_btnstate)

    def default_atom_deletion(self):
            
        self.default_atoms_button_delete =  QtGui.QPushButton("Delete")
        self.default_atoms_button_delete.setFixedWidth(80)

        self.default_atoms_button_delete.clicked.connect(self.delete_atom_btnstate)
    

    # functions
    # add default atoms
    def default_button_clicked(self):
        global selected_residues
        global atom_val_list
        global default_atoms


        for atom in default_atoms:

            for item in selected_residues:

                if item["atomname"] == atom:

                    if not [point for point in atom_val_list if point == item['atomval']]:
                            atom_val_list.append( item['atomval'] )
                            atom_val_list = sorted(atom_val_list, key=lambda item: item)


        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        self.reply_log_object.append("full chosen atoms list:")
        self.reply_log_object.append(str(atom_val_list_out))


        main_window.selected_residues_list_object.redraw_res_list()

    # add all atoms
    def all_button_clicked(self):
        global selected_residues
        global atom_val_list


        for item in selected_residues:

            if not [point for point in atom_val_list if point == item['atomval']]:
                    atom_val_list.append( item['atomval'] )
                    atom_val_list = sorted(atom_val_list, key=lambda item: item)


        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        self.reply_log_object.append("full chosen atoms list:")
        self.reply_log_object.append(str(atom_val_list_out))


        main_window.selected_residues_list_object.redraw_res_list()


    # delete default atoms
    def default_delete_button_clicked(self):
    
        global atom_val_list
        global selected_residues
        global default_atoms


        for_deleting = []


        for atom in default_atoms:

            for item in selected_residues:

                if item["atomname"] == atom:
                    for_deleting.append(item['atomval'])


                    for index, val in enumerate(atom_val_list):
                        for point in for_deleting:
                            if point == val:
                                del atom_val_list[index]



        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order


        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        self.reply_log_object.append("full chosen atoms list:")
        self.reply_log_object.append(str(atom_val_list_out))


        main_window.selected_residues_list_object.redraw_res_list()


    # delete all atoms
    def all_delete_button_clicked(self):
    
        global atom_val_list
        global selected_residues

        for_deleting = []


        for item in selected_residues:

            for_deleting.append(item['atomval'])

            for index, val in enumerate(atom_val_list):
                for point in for_deleting:
                    if point == val:
                        del atom_val_list[index]


        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        self.reply_log_object.append("full chosen atoms list:")
        self.reply_log_object.append(str(atom_val_list_out))


        main_window.selected_residues_list_object.redraw_res_list()



    ###################
    ## RANGES window ##
    ###################

    ## residue range selections

    # button and function
    def range_selection(self):
            
        self.select_button = QtGui.QPushButton("Select")
        self.select_button.setFixedWidth(80)

        self.select_button.clicked.connect(self.range_button_clicked)


    def range_button_clicked(self):

        global ranges_list
        global gro_residue_val
        global n

        
        from_input = self.from_res.text()
        to_input = self.to_res.text()

        min_res = min(gro_residue_val)
        max_res = max(gro_residue_val)

   
        temp_list = []

        # input restrictions
        if (int(from_input)) < min_res or (int(to_input)) > max_res:

            print("Error: number entered out of bounds")
            self.reply_log_object.append("Error: number entered out of bounds")

        else:
            temp_res_range = list(range(int(from_input), int(to_input) + 1))


            # setting of the data structure for each range added
            for i in temp_res_range:
                
                num = i

                for index, select_res in enumerate(gro_residue_val):
                    if select_res == num: # check if residue number of our point is in .gro and add other variables to the list
                        temp_list.append( {
                                "resval":gro_residue_val[index], 
                                "resname":gro_residue_name[index], 
                                "atomname":gro_atom_name[index], 
                                "atomval":gro_atom_number[index]
                                 } )

            ranges_list["range%s" % n] = {}
            ranges_list["range%s" % n]["range"] = temp_list
            ranges_list["range%s" % n]["current_atoms"] = []
            ranges_list["range%s" % n].update({
                                "range_number":'range%s' % n,
                                "from_val":from_input,
                                "to_val":to_input
                                })
           
            n += 1 



        main_window.select_ranges_list_object.redraw_range_list()

   

    ## signalboard

    # radiobuttons     
    def range_radiobuttons(self):

        # titles
        self.default_button_title = u'Default Atoms'
        self.all_button_title = u'All Atoms'
        self.specific_atm_range_radiobutton_title = u'Specific Atoms'

        # radiobuttons
        self.default_range_radiobutton = QtGui.QRadioButton(self.default_button_title)
        self.all_range_radiobutton = QtGui.QRadioButton(self.all_button_title)
        self.specific_atm_range_radiobutton = QtGui.QRadioButton(self.specific_atm_range_radiobutton_title)
        self.specific_atm_range_radiobutton.toggled.connect(self.select_range_btnstate)


    # buttons linking to the buttonstate of radiobuttons
    def atom_range_selection(self):
           
        self.atoms_range_button =  QtGui.QPushButton("Select")
        self.atoms_range_button.setFixedWidth(80)

        self.atoms_range_button.clicked.connect(self.select_range_btnstate)



    def atom_range_deletion(self):
           
        self.atoms_range_button_delete =  QtGui.QPushButton("Delete")
        self.atoms_range_button_delete.setFixedWidth(80)

        self.atoms_range_button_delete.clicked.connect(self.delete_range_btnstate)




    # button states
    def select_range_btnstate(self):
        if self.default_range_radiobutton.isChecked() == True:
            self.add_default_atoms_range()

        if self.all_range_radiobutton.isChecked() == True:
            main_window.select_ranges_list_object.add_all_atoms_by_range()

        if self.specific_atm_range_radiobutton.isChecked() == True:
            self.atm_nam.setDisabled(False)
            self.select_atm_button.setDisabled(False)
            self.delete_atm_button.setDisabled(False)

        else:
            self.atm_nam.setDisabled(True)
            self.select_atm_button.setDisabled(True)
            self.delete_atm_button.setDisabled(True)
            

    def delete_range_btnstate(self):
        if self.default_range_radiobutton.isChecked() == True:
            main_window.select_ranges_list_object.delete_default_atoms_by_range()

        if self.all_range_radiobutton.isChecked() == True:
            main_window.select_ranges_list_object.delete_all_atoms_by_range()



    ## functions for ranges

    ## specific atoms
    # individual atom selection buttons for ranges
    def atom_selection(self):
            
        self.select_atm_button = QtGui.QPushButton("Submit")
        self.select_atm_button.setFixedWidth(80)
        self.select_atm_button.setDisabled(True)

        self.select_atm_button.clicked.connect(self.atom_button_clicked) 

    def atom_deletion(self):
            
        self.delete_atm_button = QtGui.QPushButton("Delete")
        self.delete_atm_button.setFixedWidth(80)
        self.delete_atm_button.setDisabled(True)

        self.delete_atm_button.clicked.connect(self.atom_deletion_clicked)


    # function for specific atom selection
    def atom_button_clicked(self):

        global atom_val_list
        global ranges_list
        current_atoms = []
       
        atom_input = self.atm_nam.text()

        self.atom_input = atom_input


        main_window.select_ranges_list_object.add_atoms_by_range()

        main_window.selected_residues_list_object.redraw_res_list()

    
    def atom_deletion_clicked(self):

        global atom_val_list
        
        atom_input = self.atm_nam.text()

        self.atom_input = atom_input

        for_deleting = []

        main_window.select_ranges_list_object.delete_atoms_by_range()

        main_window.selected_residues_list_object.redraw_res_list()



    ## default atom selection functions

    def add_default_atoms_range(self):

        global atom_val_list
        global default_atoms


        main_window.select_ranges_list_object.add_default_atoms_by_range()

        main_window.selected_residues_list_object.redraw_res_list()




    ## layout of the entire window

    def layouts(self):

        
        ### residue range selection gui items: ###

        #To allow only int
        min_res = 0 
        max_res = 999
        self.onlyInt = QtGui.QIntValidator(min_res, max_res)

        # line editor for 'from' input 
        self.from_res =  QtGui.QLineEdit()
        self.from_res.setFixedWidth(50)
        self.from_res.setValidator(self.onlyInt)

        # a label            
        self.to_label =  QtGui.QLabel(" to ")
        self.to_label.setFixedWidth(30)

        # line edit for 'to' input
        self.to_res =  QtGui.QLineEdit()
        self.to_res.setFixedWidth(50)
        self.to_res.setValidator(self.onlyInt)

        # line editor for inputting specific atoms
        self.atm_nam =  QtGui.QLineEdit()
        self.atm_nam.setFixedWidth(60)
        self.atm_nam.setPlaceholderText("e.g. CA")
        self.atm_nam.setDisabled(True)



        ### object labels ###

        # RMSF
        sel_point_label =  QtGui.QLabel("Selected residues:")
        sel_res_label =  QtGui.QLabel("Selected atoms:")

        # Ranges
        range_sel_label =  QtGui.QLabel("Select a range of residues:")
        range_atom_label =  QtGui.QLabel("Select atom names to add:")

        default_range_label = QtGui.QLabel("Default atoms:")
        default_atoms_label = QtGui.QLabel("Default atoms: CA, N, O, C")

        all_atoms_range_label = QtGui.QLabel("All atoms:")

        # window titles
        range_window_label =  QtGui.QLabel("Ranges Selection Window:")
        rmsf_selection_label =  QtGui.QLabel("Selection by RMSF Window:")

        # helper section
        help_info = QtGui.QLabel("Shortcuts: ")

        help_info_2 = QtGui.QLabel("'v' - select atoms")
        help_info_3 = QtGui.QLabel("'b' - deselect atoms ")
        help_info_4 = QtGui.QLabel("'del' - delete selected residues") 
        help_info_5 = QtGui.QLabel("'p' - print selected atom numbers")
        help_info_6 = QtGui.QLabel("'s' - save session") 
        help_info_7 = QtGui.QLabel("'l' - load session")

        # description = QtGui.QLabel("  ")


        log_label = QtGui.QLabel("Hamster Log: ")

        
        ### containers ###

        # info
        info_box1 = QtGui.QVBoxLayout()

        info_box1.addWidget(help_info_2)
        info_box1.addWidget(help_info_3)

        info_box2 = QtGui.QVBoxLayout()
        info_box2.addWidget(help_info_4)
        info_box2.addWidget(help_info_5)

        info_box3 = QtGui.QVBoxLayout()
        info_box3.addWidget(help_info_6)
        info_box3.addWidget(help_info_7)



        info_box = QtGui.QHBoxLayout()
        info_box.addLayout(info_box1)
        info_box.addLayout(info_box2)
        info_box.addLayout(info_box3)


        info_box_frame = QtGui.QGroupBox()
        info_box_frame.setStyleSheet("QGroupBox { border: 1px solid gray; margin-top: 0.5em} QGroupBox::title {    subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}")
        
        # sets the margins
        left, top, right, bottom = 10, 10, 10, 10
        info_box_frame.setContentsMargins(left, top, right, bottom)

        info_box_frame.setTitle("Shortcuts")
        info_box_frame.setLayout(info_box)



        # box_with_label = QtGui.QVBoxLayout()
        # box_with_label.addWidget(help_info)
        # box_with_label.addLayout(info_box)

        reply_log_layout = QtGui.QVBoxLayout()
        reply_log_layout.addWidget(self.reply_log_object)

        reply_log_box = QtGui.QGroupBox()
        reply_log_box.setStyleSheet("QGroupBox { border: 1px solid gray; margin-top: 0.5em} QGroupBox::title {    subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}")
        
        # sets the margins
        left, top, right, bottom = 10, 10, 10, 10
        reply_log_box.setContentsMargins(left, top, right, bottom)

        reply_log_box.setTitle("Hamster Log")
        reply_log_box.setLayout(reply_log_layout)

        # helper bar (below graph)
        helper_bar = QtGui.QGridLayout()
        
        # helper_bar.addWidget(log_label, 0, 0, 1, 1)
        # helper_bar.addWidget(self.reply_log_object, 2, 0, 3, 1)

        helper_bar.addWidget(reply_log_box, 1, 0, 6, 1)

        # helper_bar.addWidget(description, 5, 0, 1, 1)
        helper_bar.addWidget(info_box_frame, 7 , 0, 2, 1)



        # graph window
        # graph_window_layout = QtGui.QVBoxLayout()

        graph_window_layout = QtGui.QGridLayout()

        graph_window_layout.addWidget(self.graph_object, 0, 0, 2, 1)

        graph_window_layout.addLayout(helper_bar, 4, 0, 2, 1)




        ### RMSF window ###

        # RMSF add and delete buttons box
        default_buttons = QtGui.QHBoxLayout()
        default_buttons.addWidget(self.default_atoms_button)
        default_buttons.addWidget(self.default_atoms_button_delete)

        # RMSF radiobuttons
        atom_radiobutton_layout = QtGui.QHBoxLayout()

        atom_radiobutton_layout.addWidget(self.default_atom_radiobutton)
        atom_radiobutton_layout.addWidget(self.all_atom_radiobutton)


        # RMSF button container
        atom_buttons = QtGui.QVBoxLayout()

        atom_buttons.addWidget(default_atoms_label)

        atom_buttons.addLayout(atom_radiobutton_layout)
        atom_buttons.addLayout(default_buttons)



        # selected residues window
        selected_residues = QtGui.QVBoxLayout()

        selected_residues.addWidget(sel_point_label)
        selected_residues.addWidget(self.selected_points_list_object)

        selected_residues.addLayout(atom_buttons)


        # selected atoms window
        selected_atoms = QtGui.QVBoxLayout()

        selected_atoms.addWidget(sel_res_label)
        selected_atoms.addWidget(self.selected_residues_list_object)


        # RMSF layout
        atom_layout = QtGui.QHBoxLayout()

        atom_layout.addLayout(selected_residues)
        atom_layout.addLayout(selected_atoms)




        ### Ranges window ###

        # ranges window
        ranges_window = QtGui.QVBoxLayout()

        ranges_window.addWidget(self.select_ranges_list_object)


        # ranges selector objects
        range_options = QtGui.QHBoxLayout()

        range_options.addWidget(self.from_res)
        range_options.addWidget(self.to_label)
        range_options.addWidget(self.to_res)
        range_options.addWidget(self.select_button)





        # radiobutton layout
        range_radiobutton_layout = QtGui.QVBoxLayout()

        range_radiobutton_layout.addWidget(self.default_range_radiobutton)
        range_radiobutton_layout.addWidget(self.all_range_radiobutton)
        range_radiobutton_layout.addWidget(self.specific_atm_range_radiobutton)


        # buttons for adding and deleting - relating to radiobuttons
        button_options = QtGui.QVBoxLayout()

        button_options.addWidget(self.atoms_range_button)
        button_options.addWidget(self.atoms_range_button_delete)


        # container for the radiobuttons, adding and deleting
        selectors = QtGui.QHBoxLayout()

        selectors.addLayout(range_radiobutton_layout)
        selectors.addLayout(button_options)


        # specific atom selector objects
        specific_atoms_options = QtGui.QHBoxLayout()

        specific_atoms_options.addWidget(self.atm_nam)
        specific_atoms_options.addWidget(self.select_atm_button)
        specific_atoms_options.addWidget(self.delete_atm_button)


        ## container for all the buttons
        ranges_buttons_sel = QtGui.QVBoxLayout()

        # range selection
        ranges_buttons_sel.addWidget(range_sel_label)
        ranges_buttons_sel.addLayout(range_options)

        

        ranges_buttons_specific = QtGui.QVBoxLayout()

        # specific atom selection
        ranges_buttons_specific.addWidget(range_atom_label)
        ranges_buttons_specific.addLayout(specific_atoms_options)


        ranges_buttons = QtGui.QGridLayout()

        verticalSpacer = QtGui.QSpacerItem(10, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        ranges_buttons.addItem(verticalSpacer)

        ranges_buttons.addLayout(ranges_buttons_sel, 0, 0, 1, 1)

        
        ranges_buttons.addItem(verticalSpacer)

        # radiobuttons
        ranges_buttons.addLayout(selectors, 3, 0, 1, 1)

        ranges_buttons.addItem(verticalSpacer)

        ranges_buttons.addLayout(ranges_buttons_specific, 7, 0, 1, 1)
        ranges_buttons.addItem(verticalSpacer)




        ## range layout
        range_layout = QtGui.QHBoxLayout()

        range_layout.addLayout(ranges_window)
        range_layout.addLayout(ranges_buttons)
        


        ### code for frames ##

        atom_box_frame = QtGui.QGroupBox()
        atom_box_frame.setStyleSheet("QGroupBox { border: 1px solid gray; margin-top: 0.5em} QGroupBox::title {    subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}")
        
        # sets the margins
        left, top, right, bottom = 10, 10, 10, 10
        atom_box_frame.setContentsMargins(left, top, right, bottom)

        atom_box_frame.setTitle("&Atom selection by RMSF")
        atom_box_frame.setLayout(atom_layout)


        range_box_frame = QtGui.QGroupBox()
        range_box_frame.setStyleSheet("QGroupBox { border: 1px solid gray; margin-top: 0.5em} QGroupBox::title {    subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}")
        
        # sets the margins
        left, top, right, bottom = 10, 10, 10, 10

        range_box_frame.setContentsMargins(left, top, right, bottom)
        range_box_frame.setTitle("&Range Selection")
        range_box_frame.setLayout(range_layout)



        ### RMSF and Range window container ##
        atom_and_range = QtGui.QVBoxLayout()

        atom_and_range.addWidget(atom_box_frame)
        atom_and_range.addWidget(range_box_frame)


        ### main layout ##

        # main_layout = QtGui.QHBoxLayout()
        main_layout = QtGui.QGridLayout()

        main_layout.addLayout(graph_window_layout, 0, 0 , 1, 3)
        main_layout.addLayout(atom_and_range, 0, 4 , 1, 2)


        self.setLayout(main_layout)



    # define the keyboard shortcuts
    def keyPressEvent(self, event):

        super(MainGuiWindow, self).keyPressEvent(event)

        # atom output shortcut
        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list from Main Window')
            main_window.reply_log_object.append("Saved atom list from Graph-Window")

            saving_and_output()

        # quit the program shortcut
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')
            app.quit()

        if event.key() == QtCore.Qt.Key_S:
            save_variables()


        if event.key() == QtCore.Qt.Key_L:
            open_variables()



# object containing the selected points from the graph list
class SelectedPointsList(QtGui.QListWidget):
    def __init__(self, selected_points):
        super(SelectedPointsList, self).__init__()
    

    def add_points(self):

        self.clear()
        for point in selected_points:
            list_item = QtGui.QListWidgetItem("res: %d rmsf: %s" % (point['x'], point['y']))
            list_item.my_point = point # keep 'point' info for reference
              
            self.addItem( list_item ) # add visually line by line





    # deleting of items in rows
    def keyPressEvent(self, event):

        global selected_residues
        global atom_val_list


        super(SelectedPointsList, self).keyPressEvent(event)


        if event.key() == QtCore.Qt.Key_Delete:
            for item in self.selectedItems():

                # update the selected points list when deleting
                for index, point in enumerate(selected_points):
                    if( point['x'] == item.my_point['x']):
                        del selected_points[index]


                temp_res_list = []

                # update the selected residues list when deleting
                for index, vals in enumerate(selected_residues):
                    if (vals['resval'] != item.my_point['x']):
                        
                        temp_res_list.append( selected_residues[index] )
                    
                selected_residues = temp_res_list
                self.takeItem(self.row(item)) # delete the row visually

                # clear corresponding atoms out of memory
                temp_atom_list = []
                for index, atom in enumerate(atom_val_list):
                    for val in selected_residues:
                        
                        if atom == val['atomval']:
                            temp_atom_list.append(atom_val_list[index])

                atom_val_list = temp_atom_list


        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order


        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        main_window.reply_log_object.append("full chosen atoms list:")
        main_window.reply_log_object.append(str(atom_val_list_out))

        main_window.graph_object.redraw_graph()
        main_window.selected_residues_list_object.redraw_res_list()

        
        # atom numbers printing and saving shortcut
        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list from selction window')
            main_window.reply_log_object.append("Saved atom list from selection window")

            saving_and_output()

        # quit the program shortcut
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')

            app.quit()

        if event.key() == QtCore.Qt.Key_S:
            save_variables()


        if event.key() == QtCore.Qt.Key_L:
            open_variables()



# object responsible for handling gro vars list (the selected residues list)
class SelectedResiduesList(QtGui.QListWidget):
    def __init__(self, selected_residues):
        super(SelectedResiduesList, self).__init__()

        self.redraw_res_list()


    # populate the list window and keep it updated
    def redraw_res_list(self):
        self.clear()

        global atom_val_list
        
        last_line = {'resval': None}


        for val in selected_residues:
            res_item = QtGui.QListWidgetItem("Residue: %s" "  %s " "   Atom: %s " "  %s " % (val['resval'], val['resname'], val['atomname'], val['atomval']))
            res_item.my_res_atom = {'resval': val['resval'], 'atomval': val['atomval']}

            current_line = res_item.my_res_atom

            line_break = QtGui.QListWidgetItem(str(' '))
            line_break.setFlags(QtCore.Qt.NoItemFlags)

            line_title = QtGui.QListWidgetItem(str('Residue %s' % current_line['resval']))
            line_title.setFlags(QtCore.Qt.NoItemFlags)

            if last_line['resval'] != current_line['resval']:
                self.addItem(line_break)
                self.addItem(line_title)
            last_line = current_line


            for item in atom_val_list:
                if item == val['atomval']:

                    brush = QtGui.QBrush()
                    brush.setColor(QtGui.QColor('red')) 
                    res_item.setForeground(brush)


            self.addItem( res_item )


    # define keyboard actions
    def keyPressEvent(self, event):

        global selected_residues
        global atom_val_list

        super(SelectedResiduesList, self).keyPressEvent(event)
        
        # add desired atoms to atom_val_list by pressing 'v'
        if event.key() == QtCore.Qt.Key_V:
            
            for item in self.selectedItems():

                item.setTextColor(QtGui.QColor("red")) 

                if not [point for point in atom_val_list if point == item.my_res_atom['atomval']]:
                    atom_val_list.append( item.my_res_atom['atomval'] )
                    atom_val_list = sorted(atom_val_list, key=lambda item: item)

        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        
        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        main_window.reply_log_object.append("full chosen atoms list:")
        main_window.reply_log_object.append(str(atom_val_list_out))


        # delete desired atoms from the atom list by pressing 'b'
        if event.key() == QtCore.Qt.Key_B:
            for item in self.selectedItems():

                item.setTextColor(QtGui.QColor("black"))

                # update the selected atoms list when deleting
                for index, atm in enumerate(atom_val_list):
                    if( atm == item.my_res_atom['atomval']):
                        del atom_val_list[index]


        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        
        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        main_window.reply_log_object.append("full chosen atoms list:")
        main_window.reply_log_object.append(str(atom_val_list_out))

        # print and save the atom values by pressing 'p'
        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list from atom selection window')
            main_window.reply_log_object.append("Saved atom list from atom selection window")

            saving_and_output()

        # quit the program by pressing 'q'
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')

            app.quit()

        if event.key() == QtCore.Qt.Key_S:
            save_variables()


        if event.key() == QtCore.Qt.Key_L:
            open_variables()


# object containing the ranges functionality
class SelectedRangeList(QtGui.QListWidget):

    def __init__(self, ranges_list):
        super(SelectedRangeList, self).__init__()

        self.redraw_range_list()

    def redraw_range_list(self):
        self.clear()

        global ranges_list


        for range_name, range_list in ranges_list.items():

            range_item = QtGui.QListWidgetItem("%s : " " %s " "to" " %s " "atoms selected: " " %s"  % (range_name, range_list['from_val'], range_list['to_val'], range_list['current_atoms'] ))

            range_item.my_range = {'range_number': range_name}

            self.addItem( range_item )


    # adding specific atoms to a selected range
    def add_atoms_by_range(self):

        global atom_val_list
        
        current_atoms = []


        for item in self.selectedItems():

            for range_name, range_list in ranges_list.items():

                if range_name == item.my_range['range_number']:

                    for atom_name in ranges_list[range_name]['range']:

                        if atom_name['atomname'] == main_window.atom_input:

                            if not [point for point in atom_val_list if point == atom_name['atomval']]:
                                        atom_val_list.append( atom_name['atomval'])
                                        atom_val_list = sorted(atom_val_list, key=lambda item: atom_name['atomval'])
                                        current_atoms.append( atom_name['atomval'])

                            if not [point for point in ranges_list[range_name]["current_atoms"] if point == atom_name['atomname']]:

                                ranges_list[range_name]["current_atoms"].append(atom_name['atomname'])

                    

            atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order
            
            print('[your_chosen_atoms]')
            print(atom_val_list_out)
            main_window.reply_log_object.append("full chosen atoms list:")
            main_window.reply_log_object.append(str(atom_val_list_out))


            self.redraw_range_list()
            main_window.selected_residues_list_object.redraw_res_list()

    # deleting specific atoms
    def delete_atoms_by_range(self):

        global atom_val_list

        for_deleting = []


        for item in self.selectedItems():

            for range_name, range_list in ranges_list.items():

                if range_name == item.my_range['range_number']:

                    for atom_name in ranges_list[range_name]['range']:

                        if atom_name['atomname'] == main_window.atom_input:
                            for_deleting.append(atom_name['atomval'])

                            for index, val in enumerate(atom_val_list):
                                for point in for_deleting:

                                    if point == val:
                                        del atom_val_list[index]

                    for index, atom in enumerate(ranges_list[range_name]['current_atoms']):
                        if atom == main_window.atom_input:
                            del ranges_list[range_name]['current_atoms'][index]
                        

        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        
        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        main_window.reply_log_object.append("full chosen atoms list:")
        main_window.reply_log_object.append(str(atom_val_list_out))


        self.redraw_range_list()
        main_window.selected_residues_list_object.redraw_res_list()

    
    def add_default_atoms_by_range(self):

        global atom_val_list
        global default_atoms

        for item in self.selectedItems():

            for range_name, range_list in ranges_list.items():

                if range_name == item.my_range['range_number']:

                    for atom_name in ranges_list[range_name]['range']:

                        for atom in default_atoms:

                            if atom_name['atomname'] == atom:

                                if not [point for point in atom_val_list if point == atom_name['atomval']]:
                                            atom_val_list.append( atom_name['atomval'])
                                            atom_val_list = sorted(atom_val_list, key=lambda item: atom_name['atomval'])
                                   
                                if not [point for point in ranges_list[range_name]["current_atoms"] if point == atom_name['atomname']]:


                                    ranges_list[range_name]["current_atoms"].append(atom_name['atomname'])




        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        
        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        main_window.reply_log_object.append("full chosen atoms list:")
        main_window.reply_log_object.append(str(atom_val_list_out))


        self.redraw_range_list()
        main_window.selected_residues_list_object.redraw_res_list()


    def delete_default_atoms_by_range(self):

        global atom_val_list
        global default_atoms

        for_deleting = []


        for item in self.selectedItems():

            for range_name, range_list in ranges_list.items():

                if range_name == item.my_range['range_number']:

                    for atom_name in ranges_list[range_name]['range']:

                        for atom in default_atoms:

                            if atom_name['atomname'] == atom:

                                for_deleting.append(atom_name['atomval'])

                                for index, val in enumerate(atom_val_list):
                                    for point in for_deleting:
                                        if point == val:
                                            del atom_val_list[index]

                        for index, atom in enumerate(ranges_list[range_name]['current_atoms']):
                            del ranges_list[range_name]['current_atoms'][index]



        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        
        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        main_window.reply_log_object.append("full chosen atoms list:")
        main_window.reply_log_object.append(str(atom_val_list_out))

        self.redraw_range_list()
        main_window.selected_residues_list_object.redraw_res_list()


    def add_all_atoms_by_range(self):
        
        global atom_val_list

        for item in self.selectedItems():

            for range_name, range_list in ranges_list.items():

                if range_name == item.my_range['range_number']:

                    for atom_name in ranges_list[range_name]['range']:

                        if not [point for point in atom_val_list if point == atom_name['atomval']]:
                            atom_val_list.append( atom_name['atomval'])
                            atom_val_list = sorted(atom_val_list, key=lambda item: atom_name['atomval'])

                        if not [point for point in ranges_list[range_name]["current_atoms"] if point == atom_name['atomname']]:
                            ranges_list[range_name]["current_atoms"].append(atom_name['atomname'])



        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        
        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        main_window.reply_log_object.append("full chosen atoms list:")
        main_window.reply_log_object.append(str(atom_val_list_out))


        self.redraw_range_list()
        main_window.selected_residues_list_object.redraw_res_list()



    def delete_all_atoms_by_range(self):

        global atom_val_list

        for_deleting = []


        for item in self.selectedItems():

            for range_name, range_list in ranges_list.items():

                if range_name == item.my_range['range_number']:

                    for atom_name in ranges_list[range_name]['range']:

                        for_deleting.append(atom_name['atomval'])

                        for index, val in enumerate(atom_val_list):
                            for point in for_deleting:
                                if point == val:
                                    del atom_val_list[index]

                        for index, atom_name in enumerate(ranges_list[range_name]['current_atoms']):
                            del ranges_list[range_name]['current_atoms'][index]



        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        
        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        main_window.reply_log_object.append("full chosen atoms list:")
        main_window.reply_log_object.append(str(atom_val_list_out))


        self.redraw_range_list()
        main_window.selected_residues_list_object.redraw_res_list()



    # deleting of items in rows
    def keyPressEvent(self, event):

        global ranges_list
        global atom_val_list


        super(SelectedRangeList, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Delete:

            for item in self.selectedItems():
               
                # update the selected ranges list when deleting
                for range_name, range_list in list(ranges_list.items()):

                    if range_name == item.my_range['range_number']:
                        del ranges_list[range_name]
                

                self.takeItem(self.row(item)) # delete the row visually


                # clear corresponding atoms out of memory
                temp_atom_list = []

                for index, atom in enumerate(atom_val_list):

                    for range_name, range_list in list(ranges_list.items()):

                        for atom in ranges_list[range_name]['range']:
                        
                            if atom == atom['atomval']:
                                temp_atom_list.append(atom_val_list[index])

                atom_val_list = temp_atom_list

            atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

            
            print('[your_chosen_atoms]')
            print(atom_val_list_out)
            main_window.reply_log_object.append("full chosen atoms list:")
            main_window.reply_log_object.append(str(atom_val_list_out))


        self.redraw_range_list()

        # atom numbers printing and saving shortcut
        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list from selction window')
            main_window.reply_log_object.append("Saved atom list from selection window")

            saving_and_output()

        # quit the program shortcut
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')

            app.quit()

        if event.key() == QtCore.Qt.Key_S:
            save_variables()


        if event.key() == QtCore.Qt.Key_L:
            open_variables()


     



app = QtGui.QApplication(sys.argv)

main_window = MainGuiWindow()
main_window.move(50, 60)
main_window.resize(1500, 1000)
main_window.show()
main_window.raise_()

sys.exit(app.exec_())