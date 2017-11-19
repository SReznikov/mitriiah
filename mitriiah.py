import sys
import argparse

from PyQt4 import QtCore, QtGui
import re

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure



parser = argparse.ArgumentParser()

parser.add_argument("-r", "--rmsf", dest = 'rmsf_filename', default = "rmsf.xvg", help="rmsf file")
parser.add_argument("-c", "--coords", dest = 'my_gro_filename', default = "protein.gro", help=".gro file used for rmsf")

args = parser.parse_args()



# Data from rmsf.xvg file
x_a_res, y_a_rmsf = [], [] 

# List of selected points
selected_points = []

selected_points_x = []
selected_points_y = []

# List of values from gro_file
gro_residue_val, gro_residue_name, gro_atom_name, gro_atom_number = [], [], [], []

selected_residues = []

atom_val_list = []



# Open the rmsf.xvg file
with open(args.rmsf_filename) as rmsf:

    rmsf_lines = [line.strip() for line in rmsf if not line.startswith(('#', '@'))]

    for line in rmsf_lines:

        cols = line.split()

        if len(cols) == 2:
            x_a_res.append(float(cols[0]))
            y_a_rmsf.append(float(cols[1]))


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


def saving_and_output():
    atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

    print('[your_chosen_atoms]')
    print(atom_val_list_out)
    with open("sel_atoms_index.ndx", 'wt') as out:
        out.write( "[ chosen_atoms ]" + '\n')
        out.write( '\n' )
        out.write((atom_val_list_out) + '\n')



# Points selection on graph
def add_point_by_mouse(event):

    global selected_points
    global selected_residues

    if event.button == 3:

        if event.xdata == None:
            return

        mx_l = event.xdata - 5
        mx_h = event.xdata + 5
        lowest_point = None # lowest y value
        x_of_lowest_point = None

        # print('you pressed', event.button, event.xdata, mx_l, mx_h)
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
                selected_points.append({"x":x_of_lowest_point, "y":lowest_point})
                selected_points = sorted(selected_points, key=lambda item: item["x"])


        for index, select_res in enumerate(gro_residue_val):
            if select_res == x_of_lowest_point:

                selected_residues.append(
                    {
                        "resval":gro_residue_val[index], 
                        "resname":gro_residue_name[index], 
                        "atomname":gro_atom_name[index], 
                        "atomval":gro_atom_number[index]
                    }
                )
                selected_residues = sorted(selected_residues, key=lambda item: item["atomval"])
                



        # add selected points to the window list
        win2.clear()
        for point in selected_points:
            list_item = QtGui.QListWidgetItem("res: %d rmsf: %s" % (point['x'], point['y']))
            list_item.my_point = point # keep 'point' info for reference
              
            win2.addItem( list_item )

          



        win3.redraw_res_list()
        win1.redraw_graph()

        # add the selected lowest point to the list of selected points
    


class GraphWindow(QtGui.QDialog):
    def __init__(self, x_a_res, y_a_rmsf):
        super(GraphWindow, self).__init__()

        self.setWindowTitle('RMSF plot')

        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)


        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        
        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # plot the rmsf.xvg

        # create an axis
        ax = self.figure.add_subplot(111)
        self.ax = ax

        ax.set_title("RMSF")    
        ax.set_xlabel('Residue number')
        ax.set_ylabel('rmsf (nm)')

        # use the selecter on graph
        cid = self.figure.canvas.mpl_connect('button_press_event', add_point_by_mouse)

        self.redraw_graph()



    def redraw_graph(self):

        # discards the old graph
        self.ax.clear()

        # plot the rmsf graph
        self.ax.plot(x_a_res,y_a_rmsf, c='k')

        # plot every selected point
        for point in selected_points:
            self.ax.plot(point['x'],point['y'], c='r', marker='o')

        self.ax.set_title("RMSF")    
        self.ax.set_xlabel('Residue number')
        self.ax.set_ylabel('rmsf (nm)')

        # refresh canvas
        self.canvas.draw()


    def keyPressEvent(self, event):

        super(GraphWindow, self).keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list from Graph-Window')

            saving_and_output()




class SelectedPointsListWindow(QtGui.QListWidget):
    def __init__(self, selected_points):
        super(SelectedPointsListWindow, self).__init__()

        self.setWindowTitle('Selected Points')
    

    # deleting of items in rows
    def keyPressEvent(self, event):

        global selected_residues

        super(SelectedPointsListWindow, self).keyPressEvent(event)
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

        win1.redraw_graph()
        win3.redraw_res_list()

        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list from selction window')

            saving_and_output()


# def gruppe(d):                                  # function for sorting the itemlist
#     return str(d['resval'])



class SelectedResiduesListWindow(QtGui.QListWidget):
    def __init__(self, selected_residues):
        super(SelectedResiduesListWindow, self).__init__()

        self.setWindowTitle('Selected Residues and atom selection')

        self.redraw_res_list()

#working script
    def redraw_res_list(self):
        self.clear()
        
        last_line = {'resval': None}

        # if last_line['resval'] != current_line['resval']:
        #     self.addItem(line_break)


        for val in selected_residues:
            res_item = QtGui.QListWidgetItem("resval: %s resname: %s " "atomname: %s " "atomval: %s " % (val['resval'], val['resname'], val['atomname'], val['atomval']))
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

            self.addItem( res_item )




    def keyPressEvent(self, event):

        global selected_residues
        global atom_val_list



        super(SelectedResiduesListWindow, self).keyPressEvent(event)
        
        # add desired atoms to atom_val_list
        if event.key() == QtCore.Qt.Key_V:
            
            for item in self.selectedItems():

                item.setTextColor(QtGui.QColor("red")) 

                if not [point for point in atom_val_list if point == item.my_res_atom['atomval']]:
                    atom_val_list.append( item.my_res_atom['atomval'] )
                    atom_val_list = sorted(atom_val_list, key=lambda item: item)


        # delete desired atoms from the atom list
        if event.key() == QtCore.Qt.Key_B:
            for item in self.selectedItems():

                item.setTextColor(QtGui.QColor("black"))

                # update the selected atoms list when deleting
                for index, atm in enumerate(atom_val_list):
                    if( atm == item.my_res_atom['atomval']):
                        del atom_val_list[index]

        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list from atom selection window')

            saving_and_output()




app = QtGui.QApplication(sys.argv)


win1 = GraphWindow(x_a_res, y_a_rmsf)
win1.move(50, 20)
win1.resize(800, 600)
win1.show()
win1.raise_()


win2 = SelectedPointsListWindow(selected_points)
win2.move(870, 60)
win2.resize(300, 150)
win2.show()
win2.raise_()

win3 = SelectedResiduesListWindow(selected_residues)
win3.move(870, 250)
win3.resize(490, 480)
win3.show()
win3.raise_()


sys.exit(app.exec_())