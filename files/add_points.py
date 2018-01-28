

import sys
import os
from PyQt4 import QtCore, QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import global_vars
from collection import GraphWindow

# # Data from rmsf.xvg file
# x_a_res, y_a_rmsf = [], [] 
x_a_res = global_vars.x_a_res
y_a_rmsf = global_vars.y_a_rmsf
# # List of selected points
# selected_points = [] # residue value and rmsf value from graph selection
selected_points = global_vars.selected_points # residue value and rmsf value from graph selection

# selected_points_x = [] # residue value
# selected_points_y = [] # rmsf value

# # List of values from gro_file
# gro_residue_val, gro_residue_name, gro_atom_name, gro_atom_number = [], [], [], []
gro_residue_val = global_vars.gro_residue_val
gro_residue_name = global_vars.gro_residue_name
gro_atom_name = global_vars.gro_atom_name
gro_atom_number = global_vars.gro_atom_number


# Points selection on graph:
def add_point_by_mouse(event):

    # global_vars.selected_points
    # global_vars.selected_residues

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
        if not [point for point in global_vars.selected_points if point['x'] == x_of_lowest_point]:
            if x_of_lowest_point != None and lowest_point != None: 
                global_vars.selected_points.append({"x":x_of_lowest_point, "y":lowest_point}) # add our lowest point to list of selected points only if residue number isn't already present in the list
                global_vars.selected_points = sorted(global_vars.selected_points, key=lambda item: item["x"])

                # for every added point, add corresponding data from .gro file:
                for index, select_res in enumerate(gro_residue_val):
                    if select_res == x_of_lowest_point: # check if residue number of our point is in .gro and add other variables to the list

                        global_vars.selected_residues.append(
                            {
                                "resval":gro_residue_val[index], 
                                "resname":gro_residue_name[index], 
                                "atomname":gro_atom_name[index], 
                                "atomval":gro_atom_number[index]
                            }
                        )
                        global_vars.selected_residues = sorted(global_vars.selected_residues, key=lambda item: item["atomval"])
                    


        # add selected_points (residue value and rmsf value) to the selected_points_list (also displayed)
        
        # main_window.selected_points_list_object.add_points()


        #refresh the list display
        # main_window.selected_residues_list_object.redraw_res_list() 
        GraphWindow.redraw_graph()