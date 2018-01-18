#!/usr/bin/env python3

import sys
import os
import argparse

from PyQt4 import QtCore, QtGui
import re

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

selected_residues = [] # residue name+value and atom name+value derived from selected_points

atom_val_list = [] # list of atom numbers obtained from user selection

ranges_list = {} # dict containing all the chosen ranges
n = 1 # range counter
all_ranges = [] # a list of ranges which are chosen


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

# save the chosen atom numbers to a new .ndx file. Also prints the values in the terminal. 
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
        main_window.selected_points_list_object.clear()
        for point in selected_points:
            list_item = QtGui.QListWidgetItem("res: %d rmsf: %s" % (point['x'], point['y']))
            list_item.my_point = point # keep 'point' info for reference
              
            main_window.selected_points_list_object.addItem( list_item ) # add visually line by line


        #refresh the list display
        main_window.selected_residues_list_object.redraw_res_list() 
        main_window.graph_object.redraw_graph()
    

# Space in which the rmsf figure is drawn
class GraphWindow(QtGui.QDialog):
    def __init__(self, x_a_res, y_a_rmsf):
        super(GraphWindow, self).__init__()

        self.setWindowTitle('RMSF plot')

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
            
            print('Saved atom list from Graph-Window')
            main_window.reply_log_object.append("Saved atom list from Graph-Window")

            saving_and_output()

        # quit the program shortcut
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')

            app.quit()

    # close down all open windows when this one is closed -- is it needed??
    def closeEvent(self, event):
        app.quit()



class ReplyLog(QtGui.QTextEdit):
    def __init__(self):
        super(ReplyLog, self).__init__()

        self.append(" Hamster log:")
        self.setReadOnly(True)

        # define the keyboard shortcuts
    def keyPressEvent(self, event):

        super(GraphWindow, self).keyPressEvent(event)

        # atom output shortcut
        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list from Graph-Window')
            main_window.reply_log_object.append("Saved atom list from Graph-Window")

            saving_and_output()

        # quit the program shortcut
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')

            app.quit()



# The window which contains everything - layouts included
class MainGuiWindow(QtGui.QWidget):
    def __init__(self):
        super(MainGuiWindow, self).__init__()

        # instantiate the required objects

        graph_object = GraphWindow(x_a_res, y_a_rmsf)
        self.graph_object = graph_object

        selected_points_list_object = SelectedPointsList(selected_points)
        self.selected_points_list_object = selected_points_list_object

        selected_residues_list_object = SelectedResiduesList(selected_residues)
        self.selected_residues_list_object = selected_residues_list_object

        select_ranges_list_object = SelectedRangeList(all_ranges)
        self.select_ranges_list_object = select_ranges_list_object

        reply_log_object = ReplyLog()
        self.reply_log_object = reply_log_object


        self.range_selection()
        self.atom_selection()
        self.atom_deletion()
        self.default_atom_selection()
        self.layouts()


        
    # gui responsible for residue range selections.
    def range_selection(self):
            
        self.select_button = QtGui.QPushButton("Select")
        self.select_button.setFixedWidth(80)

        self.select_button.clicked.connect(self.range_button_clicked)


    def range_button_clicked(self):
        # self.select_ranges_list_object.range_button_clicked()

        global ranges_list
        global gro_residue_val
        global n
        global all_ranges

        
        from_input = self.from_res.text()
        to_input = self.to_res.text()

        min_res = min(gro_residue_val)
        max_res = max(gro_residue_val)

        print('min res, max res:')
        print(min_res , max_res)
        
        
        temp_list = []

        if (int(from_input)) < min_res or (int(to_input)) > max_res:

            print("Error: number entered out of bounds")
            self.reply_log_object.append("Error: number entered out of bounds")

        else:
            temp_res_range = list(range(int(from_input), int(to_input) + 1))


            print(temp_res_range)

            self.reply_log_object.append("residues range:")
            self.reply_log_object.append(str(temp_res_range))


            for i in temp_res_range:
                
                num = i
                for index, select_res in enumerate(gro_residue_val):
                    if select_res == num: # check if residue number of our point is in .gro and add other variables to the list
                        temp_list.append( {
                                "resval":gro_residue_val[index], 
                                "resname":gro_residue_name[index], 
                                "atomname":gro_atom_name[index], 
                                "atomval":gro_atom_number[index] } )

            ranges_list["range%s" % n] = temp_list
            all_ranges.append("range%s: %s to %s"   % (n , from_input, to_input))
            n += 1 

        print("mylist")
        print(ranges_list)  
        print("all ranges")
        print(all_ranges)

        main_window.select_ranges_list_object.redraw_range_list()

                # ranges_list = sorted(ranges_list["range%s" % n], key=lambda item: item["atomval"])
            

    def atom_selection(self):
            
        self.select_atm_button = QtGui.QPushButton("Submit")
        self.select_atm_button.setFixedWidth(80)

        self.select_atm_button.clicked.connect(self.atom_button_clicked) 

    def atom_deletion(self):
            
        self.delete_atm_button = QtGui.QPushButton("Delete")
        self.delete_atm_button.setFixedWidth(80)

        self.delete_atm_button.clicked.connect(self.atom_deletion_clicked)

    def atom_button_clicked(self):

            global atom_val_list
            current_atoms = []
           
            atom_input = self.atm_nam.text()
                      
            self.reply_log_object.append("Atoms added")
            for item in ranges_list["range1"]:
                if item["atomname"] == atom_input:
                    self.reply_log_object.append(str(item))
                    if not [point for point in atom_val_list if point == item['atomval']]:
                                atom_val_list.append( item['atomval'])
                                atom_val_list = sorted(atom_val_list, key=lambda item: item)
                                current_atoms.append( item['atomval'])
                                current_atoms = sorted(current_atoms, key=lambda item: item)
                

            atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order
            print('chosen atoms:')
            print(str(atom_input))
            print(current_atoms)
            print('[your_chosen_atoms]')
            print(atom_val_list_out)

            self.reply_log_object.append("chosen atoms:")
            self.reply_log_object.append(str(atom_input))
            self.reply_log_object.append(str(current_atoms))
            self.reply_log_object.append("full chosen atoms list:")
            self.reply_log_object.append(str(atom_val_list_out))

            main_window.selected_residues_list_object.redraw_res_list()

    def atom_deletion_clicked(self):

        global atom_val_list
        
        atom_input = self.atm_nam.text()

        for_deleting = []

        self.reply_log_object.append("Atoms deleted")
        for index, item in enumerate([]):
            if item["atomname"] == atom_input:
                self.reply_log_object.append(str(item))
                for_deleting.append([][index])


                for index, val in enumerate(atom_val_list):
                    for point in for_deleting:
                        if point['atomval'] == val:
                            del atom_val_list[index]



        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order
        print('chosen atoms:')
        print(str(atom_input))
        # print(current_atoms)
        print('[your_chosen_atoms]')
        print(atom_val_list_out)

        self.reply_log_object.append("chosen atoms:")
        self.reply_log_object.append(str(atom_input))
        self.reply_log_object.append("full chosen atoms list:")
        self.reply_log_object.append(str(atom_val_list_out))

        main_window.selected_residues_list_object.redraw_res_list()
    

    def default_atom_selection(self):
            
        self.default_atoms_button =  QtGui.QPushButton("Select")
        self.default_atoms_button.setFixedWidth(80)

        self.default_atoms_button.clicked.connect(self.default_button_clicked)

    def default_button_clicked(self):
        global selected_residues
        global atom_val_list

        # add default atoms to atom_val_list

        self.default_atoms = ["CA", "C", "N", "O"]

        # self.reply_log_object.append(self.default_atoms)

        self.reply_log_object.append("Atoms added")
        for atom in self.default_atoms:

            for item in selected_residues:
                # select automatically all defaults
                if item["atomname"] == atom:
                    self.reply_log_object.append(str(item))
                    # val.setTextColor(QtGui.QColor("red")) 

                    if not [point for point in atom_val_list if point == item['atomval']]:
                            atom_val_list.append( item['atomval'] )
                            atom_val_list = sorted(atom_val_list, key=lambda item: item)


        atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        self.reply_log_object.append("full chosen atoms list:")
        self.reply_log_object.append(str(atom_val_list_out))


        main_window.selected_residues_list_object.redraw_res_list()

    # layout of the entire window
    def layouts(self):

        #To allow only int
        min_res = 0 
        max_res = 999
        self.onlyInt = QtGui.QIntValidator(min_res, max_res)


        # residue range selection gui items:
        self.from_res =  QtGui.QLineEdit()
        self.from_res.setFixedWidth(50)
        self.from_res.setValidator(self.onlyInt)


            
        self.to_label =  QtGui.QLabel(" to ")
        self.to_label.setFixedWidth(30)

        self.to_res =  QtGui.QLineEdit()
        self.to_res.setFixedWidth(50)
        self.to_res.setValidator(self.onlyInt)

        self.atm_nam =  QtGui.QLineEdit()
        self.atm_nam.setFixedWidth(50)

        # object labels
        sel_point_label =  QtGui.QLabel("Selection of residues:")
        sel_res_label =  QtGui.QLabel("Selection of atoms:")
        range_sel_label =  QtGui.QLabel("Select a range of residues:")
        range_atom_label =  QtGui.QLabel("Select atom names to add:")


        # helper section
        button_d =  QtGui.QPushButton("This does nothing")

        help_info = QtGui.QLabel("Shortcuts: 'v' - select atoms ; 'b' - deselect atoms ; 'del' - delete selected residues ; 'p' - print selected atom numbers")

        # labelling for default atom selection
        default_atoms_label = QtGui.QLabel("Default atoms:")
        default_atoms_info = QtGui.QLabel("CA, N, O, C")
        # default_atoms_button =  QtGui.QPushButton("Select")


        
        # containers

        # helper bar (below graph)
        helper_bar = QtGui.QGridLayout()
        helper_bar.addWidget(button_d, 0,0)
        helper_bar.addWidget(help_info, 1, 0)
        helper_bar.addWidget(self.reply_log_object, 2, 0)


        # graph window
        graph_window_layout = QtGui.QVBoxLayout()
        graph_window_layout.addWidget(self.graph_object)
        graph_window_layout.addLayout(helper_bar)



        #selection of residues/points window
        points_window_layout = QtGui.QVBoxLayout()
        points_window_layout.addWidget(sel_point_label)
        points_window_layout.addWidget(self.selected_points_list_object)

        # selection of atoms window
        atoms_window_layout = QtGui.QVBoxLayout()
        atoms_window_layout.addWidget(sel_res_label)
        atoms_window_layout.addWidget(self.selected_residues_list_object)



        # range of residues gui
        range_layout_opt = QtGui.QHBoxLayout()
        range_layout_opt.addWidget(self.from_res)
        range_layout_opt.addWidget(self.to_label)
        range_layout_opt.addWidget(self.to_res)
        range_layout_opt.addWidget(self.select_button)


        # ranges list window
        ranges_window_layout = QtGui.QVBoxLayout()
        # ranges_window_layout.addWidget(sel_range_label)
        ranges_window_layout.addWidget(self.select_ranges_list_object)

        # atom selector for residue range
        range_atm_layout_opt = QtGui.QHBoxLayout()
        range_atm_layout_opt.addWidget(self.atm_nam)
        range_atm_layout_opt.addWidget(self.select_atm_button)
        range_atm_layout_opt.addWidget(self.delete_atm_button)

        # default atom gui + range of residues gui
        range_layout = QtGui.QVBoxLayout()
        range_layout.addLayout(ranges_window_layout)
        range_layout.addWidget(range_sel_label)
        range_layout.addLayout(range_layout_opt)
        range_layout.addWidget(range_atom_label)
        range_layout.addLayout(range_atm_layout_opt)
        range_layout.addWidget(default_atoms_label)
        range_layout.addWidget(default_atoms_info)
        range_layout.addWidget(self.default_atoms_button)
        
        


        # set the main layout
        sel_point_layout = QtGui.QGridLayout()

        sel_point_layout.addLayout(graph_window_layout, 0,0,6,6)
        sel_point_layout.addLayout(points_window_layout, 0, 6, 3, 2)
        sel_point_layout.addLayout(range_layout, 2, 8, 1, 2)
        sel_point_layout.addLayout(atoms_window_layout, 3, 6, 6, 4)
        

        self.setLayout(sel_point_layout)

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



# object containing the selected points list
class SelectedPointsList(QtGui.QListWidget):
    def __init__(self, selected_points):
        super(SelectedPointsList, self).__init__()

        self.setWindowTitle('Selected Points')
    

    # deleting of items in rows
    def keyPressEvent(self, event):

        global selected_residues
        global atom_val_list


        super(SelectedPointsList, self).keyPressEvent(event)
        # https://stackoverflow.com/questions/38507011/implementing-keypressevent-in-qwidget
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


# object responsible for handling gro vars list (the selected residues list)
class SelectedResiduesList(QtGui.QListWidget):
    def __init__(self, selected_residues):
        super(SelectedResiduesList, self).__init__()

        self.setWindowTitle('Selected Residues and atom selection')

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


        # delete desired atoms from the atom list by pressing 'b'
        if event.key() == QtCore.Qt.Key_B:
            for item in self.selectedItems():

                item.setTextColor(QtGui.QColor("black"))

                # update the selected atoms list when deleting
                for index, atm in enumerate(atom_val_list):
                    if( atm == item.my_res_atom['atomval']):
                        del atom_val_list[index]

        # print and save the atom values by pressing 'p'
        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list from atom selection window')
            main_window.reply_log_object.append("Saved atom list from atom selection window")

            saving_and_output()

        # quit the program by pressing 'q'
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')

            app.quit()

# object containing the selected points list
class SelectedRangeList(QtGui.QListWidget):
    def __init__(self, all_ranges):
        super(SelectedRangeList, self).__init__()

        self.setWindowTitle('Selected Ranges')
        self.redraw_range_list()

    def redraw_range_list(self):
        self.clear()

        global all_ranges

        for ran in all_ranges:
            range_item = QtGui.QListWidgetItem( ran )

            self.addItem( range_item )


    # deleting of items in rows
    def keyPressEvent(self, event):

        global all_ranges


        super(SelectedRangeList, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Delete:
            for item in self.selectedItems():

                # # update the selected points list when deleting
                # for index, point in enumerate(all_ranges):
                #     if( point['x'] == item.my_point['x']):
                #         del all_ranges[index]


                # temp_rang_list = []

                # # update the selected residues list when deleting
                # for index, rang in enumerate(all_ranges):
                #     if (rang['range'] != item.my_point['x']):
                        
                #         temp_rang_list.append( all_ranges[index] )
                    
                # all_ranges = temp_rang_list

                self.takeItem(self.row(item)) # delete the row visually

                # # clear corresponding atoms out of memory
                # temp_atom_list = []
                # for index, atom in enumerate(atom_val_list):
                #     for val in all_ranges:
                        
                #         if atom == val['atomval']:
                #             temp_atom_list.append(atom_val_list[index])

                # atom_val_list = temp_atom_list

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


#     def range_button_clicked(self):
#         global []
#         global gro_residue_val
#         from_input = self.from_res.text()
#         to_input = self.to_res.text()

#         min_res = min(gro_residue_val)
#         max_res = max(gro_residue_val)

#         print('min res, max res:')
#         print(min_res , max_res)


#         if (int(from_input)) < min_res or (int(to_input)) > max_res:

#             print("Error: number entered out of bounds")
#             self.reply_log_object.append("Error: number entered out of bounds")

#         else:
#             temp_res_range = list(range(int(from_input), int(to_input) + 1))


#             print(temp_res_range)

#             self.reply_log_object.append("residues range:")
#             self.reply_log_object.append(str(temp_res_range))

#             for i in temp_res_range:
#                 num = i
#                 for index, select_res in enumerate(gro_residue_val):
#                     if select_res == num: # check if residue number of our point is in .gro and add other variables to the list
#                         [].append(
#                             {
#                                 "resval":gro_residue_val[index], 
#                                 "resname":gro_residue_name[index], 
#                                 "atomname":gro_atom_name[index], 
#                                 "atomval":gro_atom_number[index]
#                             }
#                         )
#                 [] = sorted([], key=lambda item: item["atomval"])
        








app = QtGui.QApplication(sys.argv)

main_window = MainGuiWindow()
main_window.move(50, 60)
main_window.resize(1500, 1000)
main_window.show()
main_window.raise_()


sys.exit(app.exec_())