from PyQt4 import QtCore, QtGui

import global_vars as global_vars
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















# The window which contains everything - layouts included
class MainGuiWindow(QtGui.QWidget):
    def __init__(self):
        super(MainGuiWindow, self).__init__()

        # instantiate the required objects

        #classes
        # graph_object = GraphWindow(x_a_res, y_a_rmsf)
        # self.graph_object = graph_object



        graph_object = GraphWindow(x_a_res, y_a_rmsf)
        self.graph_object = graph_object


        # selected_points_list_object = SelectedPointsList(selected_points)
        # self.selected_points_list_object = selected_points_list_object

        # selected_residues_list_object = SelectedResiduesList(selected_residues)
        # self.selected_residues_list_object = selected_residues_list_object

        # select_ranges_list_object = SelectedRangeList(ranges_list)
        # self.select_ranges_list_object = select_ranges_list_object

        # reply_log_object = ReplyLog()
        # self.reply_log_object = reply_log_object

        

    #     # functions
    #     # RMSF
    #     self.default_atom_selection()
    #     self.default_atom_deletion()
    #     self.atom_radiobuttons()

    #     # Range
    #     self.range_selection()

    #     self.atom_selection()
    #     self.atom_deletion()

    #     self.atom_range_selection()
    #     self.atom_range_deletion()

    #     self.range_radiobuttons()

        # Layout of the program
        self.layouts()

    # ######################    
    # ## RMSF atom window ##
    # ######################

    # ## signalboard 
    
    # # radiobuttons
    # def atom_radiobuttons(self):

    #     # radiobutton titles
    #     self.default_button_title = u'Default Atoms'
    #     self.all_button_title = u'All Atoms'

    #     # radiobuttons
    #     self.default_atom_radiobutton = QtGui.QRadioButton(self.default_button_title)
    #     self.all_atom_radiobutton = QtGui.QRadioButton(self.all_button_title)

    # # button states
    # def select_atom_btnstate(self):

    #     if self.default_atom_radiobutton.isChecked() == True:
    #         self.default_button_clicked()

    #     if self.all_atom_radiobutton.isChecked() == True:
    #         self.all_button_clicked()

    # def delete_atom_btnstate(self):

    #     if self.default_atom_radiobutton.isChecked() == True:
    #         self.default_delete_button_clicked()

    #     if self.all_atom_radiobutton.isChecked() == True:
    #         self.all_delete_button_clicked()

    
    # ## default atom buttons 
    # def default_atom_selection(self):
            
    #     self.default_atoms_button =  QtGui.QPushButton("Select")
    #     self.default_atoms_button.setFixedWidth(80)

    #     self.default_atoms_button.clicked.connect(self.select_atom_btnstate)

    # def default_atom_deletion(self):
            
    #     self.default_atoms_button_delete =  QtGui.QPushButton("Delete")
    #     self.default_atoms_button_delete.setFixedWidth(80)

    #     self.default_atoms_button_delete.clicked.connect(self.delete_atom_btnstate)
    

    # # functions
    # # add default atoms
    # def default_button_clicked(self):
    #     global_vars.selected_residues
    #     global_vars.atom_val_list
    #     global_vars.default_atoms


    #     for atom in default_atoms:

    #         for item in selected_residues:

    #             if item["atomname"] == atom:

    #                 if not [point for point in atom_val_list if point == item['atomval']]:
    #                         atom_val_list.append( item['atomval'] )
    #                         atom_val_list = sorted(atom_val_list, key=lambda item: item)


    #     atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

    #     print('[your_chosen_atoms]')
    #     print(atom_val_list_out)
    #     self.reply_log_object.append("full chosen atoms list:")
    #     self.reply_log_object.append(str(atom_val_list_out))


    #     main_window.selected_residues_list_object.redraw_res_list()

    # # add all atoms
    # def all_button_clicked(self):
    #     global_vars.selected_residues
    #     global_vars.atom_val_list


    #     for item in selected_residues:

    #         if not [point for point in atom_val_list if point == item['atomval']]:
    #                 atom_val_list.append( item['atomval'] )
    #                 atom_val_list = sorted(atom_val_list, key=lambda item: item)


    #     atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

    #     print('[your_chosen_atoms]')
    #     print(atom_val_list_out)
    #     self.reply_log_object.append("full chosen atoms list:")
    #     self.reply_log_object.append(str(atom_val_list_out))


    #     main_window.selected_residues_list_object.redraw_res_list()


    # # delete default atoms
    # def default_delete_button_clicked(self):
    
    #     global_vars.atom_val_list
    #     global_vars.selected_residues
    #     global_vars.default_atoms


    #     for_deleting = []


    #     for atom in default_atoms:

    #         for item in selected_residues:

    #             if item["atomname"] == atom:
    #                 for_deleting.append(item['atomval'])


    #                 for index, val in enumerate(atom_val_list):
    #                     for point in for_deleting:
    #                         if point == val:
    #                             del atom_val_list[index]



    #     atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order


    #     print('[your_chosen_atoms]')
    #     print(atom_val_list_out)
    #     self.reply_log_object.append("full chosen atoms list:")
    #     self.reply_log_object.append(str(atom_val_list_out))


    #     main_window.selected_residues_list_object.redraw_res_list()


    # # delete all atoms
    # def all_delete_button_clicked(self):
    
    #     global_vars.atom_val_list
    #     global_vars.selected_residues

    #     for_deleting = []


    #     for item in selected_residues:

    #         for_deleting.append(item['atomval'])

    #         for index, val in enumerate(atom_val_list):
    #             for point in for_deleting:
    #                 if point == val:
    #                     del atom_val_list[index]


    #     atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

    #     print('[your_chosen_atoms]')
    #     print(atom_val_list_out)
    #     self.reply_log_object.append("full chosen atoms list:")
    #     self.reply_log_object.append(str(atom_val_list_out))


    #     main_window.selected_residues_list_object.redraw_res_list()



    # ###################
    # ## RANGES window ##
    # ###################

    # ## residue range selections

    # # button and function
    # def range_selection(self):
            
    #     self.select_button = QtGui.QPushButton("Select")
    #     self.select_button.setFixedWidth(80)

    #     self.select_button.clicked.connect(self.range_button_clicked)


    # def range_button_clicked(self):

    #     global_vars.ranges_list
    #     global_vars.gro_residue_val
    #     global_vars.n

        
    #     from_input = self.from_res.text()
    #     to_input = self.to_res.text()

    #     min_res = min(gro_residue_val)
    #     max_res = max(gro_residue_val)

   
    #     temp_list = []

    #     # input restrictions
    #     # try:
    #     #     from_input == ""
    #     # except ValueError:
    #     #     print("Error: ")      # or whatever

    #     if len(from_input) < 1 or len(to_input) < 1:
    #         print("Error: No range value(s) entered")
    #         self.reply_log_object.append("Error: No range value(s) entered")

    #     else:

    #         if (int(from_input)) < min_res or (int(to_input)) > max_res:

    #             print("Error: number entered out of bounds")
    #             self.reply_log_object.append("Error: number entered out of bounds")

    #         else:
    #             temp_res_range = list(range(int(from_input), int(to_input) + 1))


    #             # setting of the data structure for each range added
    #             for i in temp_res_range:
                    
    #                 num = i

    #                 for index, select_res in enumerate(gro_residue_val):
    #                     if select_res == num: # check if residue number of our point is in .gro and add other variables to the list
    #                         temp_list.append( {
    #                                 "resval":gro_residue_val[index], 
    #                                 "resname":gro_residue_name[index], 
    #                                 "atomname":gro_atom_name[index], 
    #                                 "atomval":gro_atom_number[index]
    #                                  } )

    #             ranges_list["range%s" % n] = {}
    #             ranges_list["range%s" % n]["range"] = temp_list
    #             ranges_list["range%s" % n]["current_atoms"] = []
    #             ranges_list["range%s" % n].update({
    #                                 "range_number":'range%s' % n,
    #                                 "from_val":from_input,
    #                                 "to_val":to_input
    #                                 })
               
    #             n += 1 



    #     main_window.select_ranges_list_object.redraw_range_list()

   

    # ## signalboard

    # # radiobuttons     
    # def range_radiobuttons(self):

    #     # titles
    #     self.default_button_title = u'Default Atoms'
    #     self.all_button_title = u'All Atoms'
    #     self.specific_atm_range_radiobutton_title = u'Specific Atoms'

    #     # radiobuttons
    #     self.default_range_radiobutton = QtGui.QRadioButton(self.default_button_title)
    #     self.all_range_radiobutton = QtGui.QRadioButton(self.all_button_title)
    #     self.specific_atm_range_radiobutton = QtGui.QRadioButton(self.specific_atm_range_radiobutton_title)
    #     self.specific_atm_range_radiobutton.toggled.connect(self.select_range_btnstate)


    # # buttons linking to the buttonstate of radiobuttons
    # def atom_range_selection(self):
           
    #     self.atoms_range_button =  QtGui.QPushButton("Select")
    #     self.atoms_range_button.setFixedWidth(80)

    #     self.atoms_range_button.clicked.connect(self.select_range_btnstate)



    # def atom_range_deletion(self):
           
    #     self.atoms_range_button_delete =  QtGui.QPushButton("Delete")
    #     self.atoms_range_button_delete.setFixedWidth(80)

    #     self.atoms_range_button_delete.clicked.connect(self.delete_range_btnstate)




    # # button states
    # def select_range_btnstate(self):
    #     if self.default_range_radiobutton.isChecked() == True:
    #         self.add_default_atoms_range()

    #     if self.all_range_radiobutton.isChecked() == True:
    #         main_window.select_ranges_list_object.add_all_atoms_by_range()

    #     if self.specific_atm_range_radiobutton.isChecked() == True:
    #         self.atm_nam.setDisabled(False)
    #         self.select_atm_button.setDisabled(False)
    #         self.delete_atm_button.setDisabled(False)

    #     else:
    #         self.atm_nam.setDisabled(True)
    #         self.select_atm_button.setDisabled(True)
    #         self.delete_atm_button.setDisabled(True)
            

    # def delete_range_btnstate(self):
    #     if self.default_range_radiobutton.isChecked() == True:
    #         main_window.select_ranges_list_object.delete_default_atoms_by_range()

    #     if self.all_range_radiobutton.isChecked() == True:
    #         main_window.select_ranges_list_object.delete_all_atoms_by_range()



    # ## functions for ranges

    # ## specific atoms
    # # individual atom selection buttons for ranges
    # def atom_selection(self):
            
    #     self.select_atm_button = QtGui.QPushButton("Submit")
    #     self.select_atm_button.setFixedWidth(80)
    #     self.select_atm_button.setDisabled(True)

    #     self.select_atm_button.clicked.connect(self.atom_button_clicked) 

    # def atom_deletion(self):
            
    #     self.delete_atm_button = QtGui.QPushButton("Delete")
    #     self.delete_atm_button.setFixedWidth(80)
    #     self.delete_atm_button.setDisabled(True)

    #     self.delete_atm_button.clicked.connect(self.atom_deletion_clicked)


    # # function for specific atom selection
    # def atom_button_clicked(self):

    #     global_vars.atom_val_list
    #     global_vars.ranges_list
    #     current_atoms = []
       
    #     atom_input = self.atm_nam.text()

    #     self.atom_input = atom_input


    #     main_window.select_ranges_list_object.add_atoms_by_range()

    #     main_window.selected_residues_list_object.redraw_res_list()

    
    # def atom_deletion_clicked(self):

    #     global_vars.atom_val_list
        
    #     atom_input = self.atm_nam.text()

    #     self.atom_input = atom_input

    #     for_deleting = []

    #     main_window.select_ranges_list_object.delete_atoms_by_range()

    #     main_window.selected_residues_list_object.redraw_res_list()



    # ## default atom selection functions

    # def add_default_atoms_range(self):

    #     global_vars.atom_val_list
    #     global_vars.default_atoms


    #     main_window.select_ranges_list_object.add_default_atoms_by_range()

    #     main_window.selected_residues_list_object.redraw_res_list()




    ## layout of the entire window

    def layouts(self):

        
        # ### residue range selection gui items: ###

        # #To allow only int
        # min_res = 0 
        # max_res = 999
        # self.onlyInt = QtGui.QIntValidator(min_res, max_res)

        # # line editor for 'from' input 
        # self.from_res =  QtGui.QLineEdit()
        # self.from_res.setFixedWidth(50)
        # self.from_res.setValidator(self.onlyInt)

        # # a label            
        # self.to_label =  QtGui.QLabel(" to ")
        # self.to_label.setFixedWidth(30)

        # # line edit for 'to' input
        # self.to_res =  QtGui.QLineEdit()
        # self.to_res.setFixedWidth(50)
        # self.to_res.setValidator(self.onlyInt)

        # # line editor for inputting specific atoms
        # self.atm_nam =  QtGui.QLineEdit()
        # self.atm_nam.setFixedWidth(60)
        # self.atm_nam.setPlaceholderText("e.g. CA")
        # self.atm_nam.setDisabled(True)



        # ### object labels ###

        # # RMSF
        # sel_point_label =  QtGui.QLabel("Selected residues:")
        # sel_res_label =  QtGui.QLabel("Selected atoms:")

        # # Ranges
        # range_sel_label =  QtGui.QLabel("Select a range of residues:")
        # range_atom_label =  QtGui.QLabel("Select atom names to add:")

        # default_range_label = QtGui.QLabel("Default atoms:")
        # default_atoms_label = QtGui.QLabel("Default atoms: CA, N, O, C")

        # all_atoms_range_label = QtGui.QLabel("All atoms:")

        # # window titles
        # range_window_label =  QtGui.QLabel("Ranges Selection Window:")
        # rmsf_selection_label =  QtGui.QLabel("Selection by RMSF Window:")

        # # helper section
        # help_info = QtGui.QLabel("Shortcuts: ")

        # help_info_2 = QtGui.QLabel("'v' - select atoms")
        # help_info_3 = QtGui.QLabel("'b' - deselect atoms ")
        # help_info_4 = QtGui.QLabel("'del' - delete selected residues") 
        # help_info_5 = QtGui.QLabel("'p' - print selected atom numbers")
        # help_info_6 = QtGui.QLabel("'s' - save session") 
        # help_info_7 = QtGui.QLabel("'l' - load session")

        # # description = QtGui.QLabel("  ")


        # log_label = QtGui.QLabel("Hamster Log: ")

        
        # ### containers ###

        # # info
        # info_box1 = QtGui.QVBoxLayout()

        # info_box1.addWidget(help_info_2)
        # info_box1.addWidget(help_info_3)

        # info_box2 = QtGui.QVBoxLayout()
        # info_box2.addWidget(help_info_4)
        # info_box2.addWidget(help_info_5)

        # info_box3 = QtGui.QVBoxLayout()
        # info_box3.addWidget(help_info_6)
        # info_box3.addWidget(help_info_7)



        # info_box = QtGui.QHBoxLayout()
        # info_box.addLayout(info_box1)
        # info_box.addLayout(info_box2)
        # info_box.addLayout(info_box3)


        # info_box_frame = QtGui.QGroupBox()
        # info_box_frame.setStyleSheet("QGroupBox { border: 1px solid gray; margin-top: 0.5em} QGroupBox::title {    subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}")
        
        # # sets the margins
        # left, top, right, bottom = 10, 10, 10, 10
        # info_box_frame.setContentsMargins(left, top, right, bottom)

        # info_box_frame.setTitle("Shortcuts")
        # info_box_frame.setLayout(info_box)



        # # box_with_label = QtGui.QVBoxLayout()
        # # box_with_label.addWidget(help_info)
        # # box_with_label.addLayout(info_box)

        # reply_log_layout = QtGui.QVBoxLayout()
        # reply_log_layout.addWidget(self.reply_log_object)

        # reply_log_box = QtGui.QGroupBox()
        # reply_log_box.setStyleSheet("QGroupBox { border: 1px solid gray; margin-top: 0.5em} QGroupBox::title {    subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}")
        
        # # sets the margins
        # left, top, right, bottom = 10, 10, 10, 10
        # reply_log_box.setContentsMargins(left, top, right, bottom)

        # reply_log_box.setTitle("Hamster Log")
        # reply_log_box.setLayout(reply_log_layout)

        # # helper bar (below graph)
        # helper_bar = QtGui.QGridLayout()
        
        # # helper_bar.addWidget(log_label, 0, 0, 1, 1)
        # # helper_bar.addWidget(self.reply_log_object, 2, 0, 3, 1)

        # helper_bar.addWidget(reply_log_box, 1, 0, 6, 1)

        # # helper_bar.addWidget(description, 5, 0, 1, 1)
        # helper_bar.addWidget(info_box_frame, 7 , 0, 2, 1)



        # # graph window
        # # graph_window_layout = QtGui.QVBoxLayout()

        graph_window_layout = QtGui.QGridLayout()

        graph_window_layout.addWidget(self.graph_object, 0, 0, 2, 1)

        # graph_window_layout.addLayout(helper_bar, 4, 0, 2, 1)




        # ### RMSF window ###

        # # RMSF add and delete buttons box
        # default_buttons = QtGui.QHBoxLayout()
        # default_buttons.addWidget(self.default_atoms_button)
        # default_buttons.addWidget(self.default_atoms_button_delete)

        # # RMSF radiobuttons
        # atom_radiobutton_layout = QtGui.QHBoxLayout()

        # atom_radiobutton_layout.addWidget(self.default_atom_radiobutton)
        # atom_radiobutton_layout.addWidget(self.all_atom_radiobutton)


        # # RMSF button container
        # atom_buttons = QtGui.QVBoxLayout()

        # atom_buttons.addWidget(default_atoms_label)

        # atom_buttons.addLayout(atom_radiobutton_layout)
        # atom_buttons.addLayout(default_buttons)



        # # selected residues window
        # selected_residues = QtGui.QVBoxLayout()

        # selected_residues.addWidget(sel_point_label)
        # selected_residues.addWidget(self.selected_points_list_object)

        # selected_residues.addLayout(atom_buttons)


        # # selected atoms window
        # selected_atoms = QtGui.QVBoxLayout()

        # selected_atoms.addWidget(sel_res_label)
        # selected_atoms.addWidget(self.selected_residues_list_object)


        # # RMSF layout
        # atom_layout = QtGui.QHBoxLayout()

        # atom_layout.addLayout(selected_residues)
        # atom_layout.addLayout(selected_atoms)




        # ### Ranges window ###

        # # ranges window
        # ranges_window = QtGui.QVBoxLayout()

        # ranges_window.addWidget(self.select_ranges_list_object)


        # # ranges selector objects
        # range_options = QtGui.QHBoxLayout()

        # range_options.addWidget(self.from_res)
        # range_options.addWidget(self.to_label)
        # range_options.addWidget(self.to_res)
        # range_options.addWidget(self.select_button)





        # # radiobutton layout
        # range_radiobutton_layout = QtGui.QVBoxLayout()

        # range_radiobutton_layout.addWidget(self.default_range_radiobutton)
        # range_radiobutton_layout.addWidget(self.all_range_radiobutton)
        # range_radiobutton_layout.addWidget(self.specific_atm_range_radiobutton)


        # # buttons for adding and deleting - relating to radiobuttons
        # button_options = QtGui.QVBoxLayout()

        # button_options.addWidget(self.atoms_range_button)
        # button_options.addWidget(self.atoms_range_button_delete)


        # # container for the radiobuttons, adding and deleting
        # selectors = QtGui.QHBoxLayout()

        # selectors.addLayout(range_radiobutton_layout)
        # selectors.addLayout(button_options)


        # # specific atom selector objects
        # specific_atoms_options = QtGui.QHBoxLayout()

        # specific_atoms_options.addWidget(self.atm_nam)
        # specific_atoms_options.addWidget(self.select_atm_button)
        # specific_atoms_options.addWidget(self.delete_atm_button)


        # ## container for all the buttons
        # ranges_buttons_sel = QtGui.QVBoxLayout()

        # # range selection
        # ranges_buttons_sel.addWidget(range_sel_label)
        # ranges_buttons_sel.addLayout(range_options)

        

        # ranges_buttons_specific = QtGui.QVBoxLayout()

        # # specific atom selection
        # ranges_buttons_specific.addWidget(range_atom_label)
        # ranges_buttons_specific.addLayout(specific_atoms_options)


        # ranges_buttons = QtGui.QGridLayout()

        # verticalSpacer = QtGui.QSpacerItem(10, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        # ranges_buttons.addItem(verticalSpacer)

        # ranges_buttons.addLayout(ranges_buttons_sel, 0, 0, 1, 1)

        
        # ranges_buttons.addItem(verticalSpacer)

        # # radiobuttons
        # ranges_buttons.addLayout(selectors, 3, 0, 1, 1)

        # ranges_buttons.addItem(verticalSpacer)

        # ranges_buttons.addLayout(ranges_buttons_specific, 7, 0, 1, 1)
        # ranges_buttons.addItem(verticalSpacer)




        # ## range layout
        # range_layout = QtGui.QHBoxLayout()

        # range_layout.addLayout(ranges_window)
        # range_layout.addLayout(ranges_buttons)
        


        # ### code for frames ##

        # atom_box_frame = QtGui.QGroupBox()
        # atom_box_frame.setStyleSheet("QGroupBox { border: 1px solid gray; margin-top: 0.5em} QGroupBox::title {    subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}")
        
        # # sets the margins
        # left, top, right, bottom = 10, 10, 10, 10
        # atom_box_frame.setContentsMargins(left, top, right, bottom)

        # atom_box_frame.setTitle("&Atom selection by RMSF")
        # atom_box_frame.setLayout(atom_layout)


        # range_box_frame = QtGui.QGroupBox()
        # range_box_frame.setStyleSheet("QGroupBox { border: 1px solid gray; margin-top: 0.5em} QGroupBox::title {    subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}")
        
        # # sets the margins
        # left, top, right, bottom = 10, 10, 10, 10

        # range_box_frame.setContentsMargins(left, top, right, bottom)
        # range_box_frame.setTitle("&Range Selection")
        # range_box_frame.setLayout(range_layout)



        # ### RMSF and Range window container ##
        # atom_and_range = QtGui.QVBoxLayout()

        # atom_and_range.addWidget(atom_box_frame)
        # atom_and_range.addWidget(range_box_frame)


        ### main layout ##

        # main_layout = QtGui.QHBoxLayout()
        main_layout = QtGui.QGridLayout()

        main_layout.addLayout(graph_window_layout, 0, 0 , 1, 3)
        # main_layout.addLayout(atom_and_range, 0, 4 , 1, 2)


        self.setLayout(main_layout)



    # # define the keyboard shortcuts
    # def keyPressEvent(self, event):

    #     super(MainGuiWindow, self).keyPressEvent(event)

    #     # atom output shortcut
    #     if event.key() == QtCore.Qt.Key_P:
            
    #         print('Saved atom list from Main Window')
    #         main_window.reply_log_object.append("Saved atom list from Graph-Window")

    #         saving_and_output()

    #     # quit the program shortcut
    #     if event.key() == QtCore.Qt.Key_Q:
            
    #         print('Hamster ran out!')
    #         app.quit()

    #     if event.key() == QtCore.Qt.Key_S:
    #         save_variables()


    #     if event.key() == QtCore.Qt.Key_L:
    #         open_variables()









# # The window which contains everything - layouts included
# class MainGuiWindow(QtGui.QWidget):
#     def __init__(self):
#         super(MainGuiWindow, self).__init__()

#         # instantiate the required objects

#         #classes
#         graph_object = GraphWindow(x_a_res, y_a_rmsf)
#         self.graph_object = graph_object

#         selected_points_list_object = SelectedPointsList(selected_points)
#         self.selected_points_list_object = selected_points_list_object

#         selected_residues_list_object = SelectedResiduesList(selected_residues)
#         self.selected_residues_list_object = selected_residues_list_object

#         select_ranges_list_object = SelectedRangeList(ranges_list)
#         self.select_ranges_list_object = select_ranges_list_object

#         reply_log_object = ReplyLog()
#         self.reply_log_object = reply_log_object

        

#         # functions
#         # RMSF
#         self.default_atom_selection()
#         self.default_atom_deletion()
#         self.atom_radiobuttons()

#         # Range
#         self.range_selection()

#         self.atom_selection()
#         self.atom_deletion()

#         self.atom_range_selection()
#         self.atom_range_deletion()

#         self.range_radiobuttons()

#         # Layout of the program
#         self.layouts()

#     ######################    
#     ## RMSF atom window ##
#     ######################

#     ## signalboard 
    
#     # radiobuttons
#     def atom_radiobuttons(self):

#         # radiobutton titles
#         self.default_button_title = u'Default Atoms'
#         self.all_button_title = u'All Atoms'

#         # radiobuttons
#         self.default_atom_radiobutton = QtGui.QRadioButton(self.default_button_title)
#         self.all_atom_radiobutton = QtGui.QRadioButton(self.all_button_title)

#     # button states
#     def select_atom_btnstate(self):

#         if self.default_atom_radiobutton.isChecked() == True:
#             self.default_button_clicked()

#         if self.all_atom_radiobutton.isChecked() == True:
#             self.all_button_clicked()

#     def delete_atom_btnstate(self):

#         if self.default_atom_radiobutton.isChecked() == True:
#             self.default_delete_button_clicked()

#         if self.all_atom_radiobutton.isChecked() == True:
#             self.all_delete_button_clicked()

    
#     ## default atom buttons 
#     def default_atom_selection(self):
            
#         self.default_atoms_button =  QtGui.QPushButton("Select")
#         self.default_atoms_button.setFixedWidth(80)

#         self.default_atoms_button.clicked.connect(self.select_atom_btnstate)

#     def default_atom_deletion(self):
            
#         self.default_atoms_button_delete =  QtGui.QPushButton("Delete")
#         self.default_atoms_button_delete.setFixedWidth(80)

#         self.default_atoms_button_delete.clicked.connect(self.delete_atom_btnstate)
    

#     # functions
#     # add default atoms
#     def default_button_clicked(self):
#         global selected_residues
#         global atom_val_list
#         global default_atoms


#         for atom in default_atoms:

#             for item in selected_residues:

#                 if item["atomname"] == atom:

#                     if not [point for point in atom_val_list if point == item['atomval']]:
#                             atom_val_list.append( item['atomval'] )
#                             atom_val_list = sorted(atom_val_list, key=lambda item: item)


#         atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

#         print('[your_chosen_atoms]')
#         print(atom_val_list_out)
#         self.reply_log_object.append("full chosen atoms list:")
#         self.reply_log_object.append(str(atom_val_list_out))


#         main_window.selected_residues_list_object.redraw_res_list()

#     # add all atoms
#     def all_button_clicked(self):
#         global selected_residues
#         global atom_val_list


#         for item in selected_residues:

#             if not [point for point in atom_val_list if point == item['atomval']]:
#                     atom_val_list.append( item['atomval'] )
#                     atom_val_list = sorted(atom_val_list, key=lambda item: item)


#         atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

#         print('[your_chosen_atoms]')
#         print(atom_val_list_out)
#         self.reply_log_object.append("full chosen atoms list:")
#         self.reply_log_object.append(str(atom_val_list_out))


#         main_window.selected_residues_list_object.redraw_res_list()


#     # delete default atoms
#     def default_delete_button_clicked(self):
    
#         global atom_val_list
#         global selected_residues
#         global default_atoms


#         for_deleting = []


#         for atom in default_atoms:

#             for item in selected_residues:

#                 if item["atomname"] == atom:
#                     for_deleting.append(item['atomval'])


#                     for index, val in enumerate(atom_val_list):
#                         for point in for_deleting:
#                             if point == val:
#                                 del atom_val_list[index]



#         atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order


#         print('[your_chosen_atoms]')
#         print(atom_val_list_out)
#         self.reply_log_object.append("full chosen atoms list:")
#         self.reply_log_object.append(str(atom_val_list_out))


#         main_window.selected_residues_list_object.redraw_res_list()


#     # delete all atoms
#     def all_delete_button_clicked(self):
    
#         global atom_val_list
#         global selected_residues

#         for_deleting = []


#         for item in selected_residues:

#             for_deleting.append(item['atomval'])

#             for index, val in enumerate(atom_val_list):
#                 for point in for_deleting:
#                     if point == val:
#                         del atom_val_list[index]


#         atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order

#         print('[your_chosen_atoms]')
#         print(atom_val_list_out)
#         self.reply_log_object.append("full chosen atoms list:")
#         self.reply_log_object.append(str(atom_val_list_out))


#         main_window.selected_residues_list_object.redraw_res_list()



#     ###################
#     ## RANGES window ##
#     ###################

#     ## residue range selections

#     # button and function
#     def range_selection(self):
            
#         self.select_button = QtGui.QPushButton("Select")
#         self.select_button.setFixedWidth(80)

#         self.select_button.clicked.connect(self.range_button_clicked)


#     def range_button_clicked(self):

#         global ranges_list
#         global gro_residue_val
#         global n

        
#         from_input = self.from_res.text()
#         to_input = self.to_res.text()

#         min_res = min(gro_residue_val)
#         max_res = max(gro_residue_val)

   
#         temp_list = []

#         # input restrictions
#         # try:
#         #     from_input == ""
#         # except ValueError:
#         #     print("Error: ")      # or whatever

#         if len(from_input) < 1 or len(to_input) < 1:
#             print("Error: No range value(s) entered")
#             self.reply_log_object.append("Error: No range value(s) entered")

#         else:

#             if (int(from_input)) < min_res or (int(to_input)) > max_res:

#                 print("Error: number entered out of bounds")
#                 self.reply_log_object.append("Error: number entered out of bounds")

#             else:
#                 temp_res_range = list(range(int(from_input), int(to_input) + 1))


#                 # setting of the data structure for each range added
#                 for i in temp_res_range:
                    
#                     num = i

#                     for index, select_res in enumerate(gro_residue_val):
#                         if select_res == num: # check if residue number of our point is in .gro and add other variables to the list
#                             temp_list.append( {
#                                     "resval":gro_residue_val[index], 
#                                     "resname":gro_residue_name[index], 
#                                     "atomname":gro_atom_name[index], 
#                                     "atomval":gro_atom_number[index]
#                                      } )

#                 ranges_list["range%s" % n] = {}
#                 ranges_list["range%s" % n]["range"] = temp_list
#                 ranges_list["range%s" % n]["current_atoms"] = []
#                 ranges_list["range%s" % n].update({
#                                     "range_number":'range%s' % n,
#                                     "from_val":from_input,
#                                     "to_val":to_input
#                                     })
               
#                 n += 1 



#         main_window.select_ranges_list_object.redraw_range_list()

   

#     ## signalboard

#     # radiobuttons     
#     def range_radiobuttons(self):

#         # titles
#         self.default_button_title = u'Default Atoms'
#         self.all_button_title = u'All Atoms'
#         self.specific_atm_range_radiobutton_title = u'Specific Atoms'

#         # radiobuttons
#         self.default_range_radiobutton = QtGui.QRadioButton(self.default_button_title)
#         self.all_range_radiobutton = QtGui.QRadioButton(self.all_button_title)
#         self.specific_atm_range_radiobutton = QtGui.QRadioButton(self.specific_atm_range_radiobutton_title)
#         self.specific_atm_range_radiobutton.toggled.connect(self.select_range_btnstate)


#     # buttons linking to the buttonstate of radiobuttons
#     def atom_range_selection(self):
           
#         self.atoms_range_button =  QtGui.QPushButton("Select")
#         self.atoms_range_button.setFixedWidth(80)

#         self.atoms_range_button.clicked.connect(self.select_range_btnstate)



#     def atom_range_deletion(self):
           
#         self.atoms_range_button_delete =  QtGui.QPushButton("Delete")
#         self.atoms_range_button_delete.setFixedWidth(80)

#         self.atoms_range_button_delete.clicked.connect(self.delete_range_btnstate)




#     # button states
#     def select_range_btnstate(self):
#         if self.default_range_radiobutton.isChecked() == True:
#             self.add_default_atoms_range()

#         if self.all_range_radiobutton.isChecked() == True:
#             main_window.select_ranges_list_object.add_all_atoms_by_range()

#         if self.specific_atm_range_radiobutton.isChecked() == True:
#             self.atm_nam.setDisabled(False)
#             self.select_atm_button.setDisabled(False)
#             self.delete_atm_button.setDisabled(False)

#         else:
#             self.atm_nam.setDisabled(True)
#             self.select_atm_button.setDisabled(True)
#             self.delete_atm_button.setDisabled(True)
            

#     def delete_range_btnstate(self):
#         if self.default_range_radiobutton.isChecked() == True:
#             main_window.select_ranges_list_object.delete_default_atoms_by_range()

#         if self.all_range_radiobutton.isChecked() == True:
#             main_window.select_ranges_list_object.delete_all_atoms_by_range()



#     ## functions for ranges

#     ## specific atoms
#     # individual atom selection buttons for ranges
#     def atom_selection(self):
            
#         self.select_atm_button = QtGui.QPushButton("Submit")
#         self.select_atm_button.setFixedWidth(80)
#         self.select_atm_button.setDisabled(True)

#         self.select_atm_button.clicked.connect(self.atom_button_clicked) 

#     def atom_deletion(self):
            
#         self.delete_atm_button = QtGui.QPushButton("Delete")
#         self.delete_atm_button.setFixedWidth(80)
#         self.delete_atm_button.setDisabled(True)

#         self.delete_atm_button.clicked.connect(self.atom_deletion_clicked)


#     # function for specific atom selection
#     def atom_button_clicked(self):

#         global atom_val_list
#         global ranges_list
#         current_atoms = []
       
#         atom_input = self.atm_nam.text()

#         self.atom_input = atom_input


#         main_window.select_ranges_list_object.add_atoms_by_range()

#         main_window.selected_residues_list_object.redraw_res_list()

    
#     def atom_deletion_clicked(self):

#         global atom_val_list
        
#         atom_input = self.atm_nam.text()

#         self.atom_input = atom_input

#         for_deleting = []

#         main_window.select_ranges_list_object.delete_atoms_by_range()

#         main_window.selected_residues_list_object.redraw_res_list()



#     ## default atom selection functions

#     def add_default_atoms_range(self):

#         global atom_val_list
#         global default_atoms


#         main_window.select_ranges_list_object.add_default_atoms_by_range()

#         main_window.selected_residues_list_object.redraw_res_list()




#     ## layout of the entire window

#     def layouts(self):

        
#         ### residue range selection gui items: ###

#         #To allow only int
#         min_res = 0 
#         max_res = 999
#         self.onlyInt = QtGui.QIntValidator(min_res, max_res)

#         # line editor for 'from' input 
#         self.from_res =  QtGui.QLineEdit()
#         self.from_res.setFixedWidth(50)
#         self.from_res.setValidator(self.onlyInt)

#         # a label            
#         self.to_label =  QtGui.QLabel(" to ")
#         self.to_label.setFixedWidth(30)

#         # line edit for 'to' input
#         self.to_res =  QtGui.QLineEdit()
#         self.to_res.setFixedWidth(50)
#         self.to_res.setValidator(self.onlyInt)

#         # line editor for inputting specific atoms
#         self.atm_nam =  QtGui.QLineEdit()
#         self.atm_nam.setFixedWidth(60)
#         self.atm_nam.setPlaceholderText("e.g. CA")
#         self.atm_nam.setDisabled(True)



#         ### object labels ###

#         # RMSF
#         sel_point_label =  QtGui.QLabel("Selected residues:")
#         sel_res_label =  QtGui.QLabel("Selected atoms:")

#         # Ranges
#         range_sel_label =  QtGui.QLabel("Select a range of residues:")
#         range_atom_label =  QtGui.QLabel("Select atom names to add:")

#         default_range_label = QtGui.QLabel("Default atoms:")
#         default_atoms_label = QtGui.QLabel("Default atoms: CA, N, O, C")

#         all_atoms_range_label = QtGui.QLabel("All atoms:")

#         # window titles
#         range_window_label =  QtGui.QLabel("Ranges Selection Window:")
#         rmsf_selection_label =  QtGui.QLabel("Selection by RMSF Window:")

#         # helper section
#         help_info = QtGui.QLabel("Shortcuts: ")

#         help_info_2 = QtGui.QLabel("'v' - select atoms")
#         help_info_3 = QtGui.QLabel("'b' - deselect atoms ")
#         help_info_4 = QtGui.QLabel("'del' - delete selected residues") 
#         help_info_5 = QtGui.QLabel("'p' - print selected atom numbers")
#         help_info_6 = QtGui.QLabel("'s' - save session") 
#         help_info_7 = QtGui.QLabel("'l' - load session")

#         # description = QtGui.QLabel("  ")


#         log_label = QtGui.QLabel("Hamster Log: ")

        
#         ### containers ###

#         # info
#         info_box1 = QtGui.QVBoxLayout()

#         info_box1.addWidget(help_info_2)
#         info_box1.addWidget(help_info_3)

#         info_box2 = QtGui.QVBoxLayout()
#         info_box2.addWidget(help_info_4)
#         info_box2.addWidget(help_info_5)

#         info_box3 = QtGui.QVBoxLayout()
#         info_box3.addWidget(help_info_6)
#         info_box3.addWidget(help_info_7)



#         info_box = QtGui.QHBoxLayout()
#         info_box.addLayout(info_box1)
#         info_box.addLayout(info_box2)
#         info_box.addLayout(info_box3)


#         info_box_frame = QtGui.QGroupBox()
#         info_box_frame.setStyleSheet("QGroupBox { border: 1px solid gray; margin-top: 0.5em} QGroupBox::title {    subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}")
        
#         # sets the margins
#         left, top, right, bottom = 10, 10, 10, 10
#         info_box_frame.setContentsMargins(left, top, right, bottom)

#         info_box_frame.setTitle("Shortcuts")
#         info_box_frame.setLayout(info_box)



#         # box_with_label = QtGui.QVBoxLayout()
#         # box_with_label.addWidget(help_info)
#         # box_with_label.addLayout(info_box)

#         reply_log_layout = QtGui.QVBoxLayout()
#         reply_log_layout.addWidget(self.reply_log_object)

#         reply_log_box = QtGui.QGroupBox()
#         reply_log_box.setStyleSheet("QGroupBox { border: 1px solid gray; margin-top: 0.5em} QGroupBox::title {    subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}")
        
#         # sets the margins
#         left, top, right, bottom = 10, 10, 10, 10
#         reply_log_box.setContentsMargins(left, top, right, bottom)

#         reply_log_box.setTitle("Hamster Log")
#         reply_log_box.setLayout(reply_log_layout)

#         # helper bar (below graph)
#         helper_bar = QtGui.QGridLayout()
        
#         # helper_bar.addWidget(log_label, 0, 0, 1, 1)
#         # helper_bar.addWidget(self.reply_log_object, 2, 0, 3, 1)

#         helper_bar.addWidget(reply_log_box, 1, 0, 6, 1)

#         # helper_bar.addWidget(description, 5, 0, 1, 1)
#         helper_bar.addWidget(info_box_frame, 7 , 0, 2, 1)



#         # graph window
#         # graph_window_layout = QtGui.QVBoxLayout()

#         graph_window_layout = QtGui.QGridLayout()

#         graph_window_layout.addWidget(self.graph_object, 0, 0, 2, 1)

#         graph_window_layout.addLayout(helper_bar, 4, 0, 2, 1)




#         ### RMSF window ###

#         # RMSF add and delete buttons box
#         default_buttons = QtGui.QHBoxLayout()
#         default_buttons.addWidget(self.default_atoms_button)
#         default_buttons.addWidget(self.default_atoms_button_delete)

#         # RMSF radiobuttons
#         atom_radiobutton_layout = QtGui.QHBoxLayout()

#         atom_radiobutton_layout.addWidget(self.default_atom_radiobutton)
#         atom_radiobutton_layout.addWidget(self.all_atom_radiobutton)


#         # RMSF button container
#         atom_buttons = QtGui.QVBoxLayout()

#         atom_buttons.addWidget(default_atoms_label)

#         atom_buttons.addLayout(atom_radiobutton_layout)
#         atom_buttons.addLayout(default_buttons)



#         # selected residues window
#         selected_residues = QtGui.QVBoxLayout()

#         selected_residues.addWidget(sel_point_label)
#         selected_residues.addWidget(self.selected_points_list_object)

#         selected_residues.addLayout(atom_buttons)


#         # selected atoms window
#         selected_atoms = QtGui.QVBoxLayout()

#         selected_atoms.addWidget(sel_res_label)
#         selected_atoms.addWidget(self.selected_residues_list_object)


#         # RMSF layout
#         atom_layout = QtGui.QHBoxLayout()

#         atom_layout.addLayout(selected_residues)
#         atom_layout.addLayout(selected_atoms)




#         ### Ranges window ###

#         # ranges window
#         ranges_window = QtGui.QVBoxLayout()

#         ranges_window.addWidget(self.select_ranges_list_object)


#         # ranges selector objects
#         range_options = QtGui.QHBoxLayout()

#         range_options.addWidget(self.from_res)
#         range_options.addWidget(self.to_label)
#         range_options.addWidget(self.to_res)
#         range_options.addWidget(self.select_button)





#         # radiobutton layout
#         range_radiobutton_layout = QtGui.QVBoxLayout()

#         range_radiobutton_layout.addWidget(self.default_range_radiobutton)
#         range_radiobutton_layout.addWidget(self.all_range_radiobutton)
#         range_radiobutton_layout.addWidget(self.specific_atm_range_radiobutton)


#         # buttons for adding and deleting - relating to radiobuttons
#         button_options = QtGui.QVBoxLayout()

#         button_options.addWidget(self.atoms_range_button)
#         button_options.addWidget(self.atoms_range_button_delete)


#         # container for the radiobuttons, adding and deleting
#         selectors = QtGui.QHBoxLayout()

#         selectors.addLayout(range_radiobutton_layout)
#         selectors.addLayout(button_options)


#         # specific atom selector objects
#         specific_atoms_options = QtGui.QHBoxLayout()

#         specific_atoms_options.addWidget(self.atm_nam)
#         specific_atoms_options.addWidget(self.select_atm_button)
#         specific_atoms_options.addWidget(self.delete_atm_button)


#         ## container for all the buttons
#         ranges_buttons_sel = QtGui.QVBoxLayout()

#         # range selection
#         ranges_buttons_sel.addWidget(range_sel_label)
#         ranges_buttons_sel.addLayout(range_options)

        

#         ranges_buttons_specific = QtGui.QVBoxLayout()

#         # specific atom selection
#         ranges_buttons_specific.addWidget(range_atom_label)
#         ranges_buttons_specific.addLayout(specific_atoms_options)


#         ranges_buttons = QtGui.QGridLayout()

#         verticalSpacer = QtGui.QSpacerItem(10, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

#         ranges_buttons.addItem(verticalSpacer)

#         ranges_buttons.addLayout(ranges_buttons_sel, 0, 0, 1, 1)

        
#         ranges_buttons.addItem(verticalSpacer)

#         # radiobuttons
#         ranges_buttons.addLayout(selectors, 3, 0, 1, 1)

#         ranges_buttons.addItem(verticalSpacer)

#         ranges_buttons.addLayout(ranges_buttons_specific, 7, 0, 1, 1)
#         ranges_buttons.addItem(verticalSpacer)




#         ## range layout
#         range_layout = QtGui.QHBoxLayout()

#         range_layout.addLayout(ranges_window)
#         range_layout.addLayout(ranges_buttons)
        


#         ### code for frames ##

#         atom_box_frame = QtGui.QGroupBox()
#         atom_box_frame.setStyleSheet("QGroupBox { border: 1px solid gray; margin-top: 0.5em} QGroupBox::title {    subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}")
        
#         # sets the margins
#         left, top, right, bottom = 10, 10, 10, 10
#         atom_box_frame.setContentsMargins(left, top, right, bottom)

#         atom_box_frame.setTitle("&Atom selection by RMSF")
#         atom_box_frame.setLayout(atom_layout)


#         range_box_frame = QtGui.QGroupBox()
#         range_box_frame.setStyleSheet("QGroupBox { border: 1px solid gray; margin-top: 0.5em} QGroupBox::title {    subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}")
        
#         # sets the margins
#         left, top, right, bottom = 10, 10, 10, 10

#         range_box_frame.setContentsMargins(left, top, right, bottom)
#         range_box_frame.setTitle("&Range Selection")
#         range_box_frame.setLayout(range_layout)



#         ### RMSF and Range window container ##
#         atom_and_range = QtGui.QVBoxLayout()

#         atom_and_range.addWidget(atom_box_frame)
#         atom_and_range.addWidget(range_box_frame)


#         ### main layout ##

#         # main_layout = QtGui.QHBoxLayout()
#         main_layout = QtGui.QGridLayout()

#         main_layout.addLayout(graph_window_layout, 0, 0 , 1, 3)
#         main_layout.addLayout(atom_and_range, 0, 4 , 1, 2)


#         self.setLayout(main_layout)



#     # define the keyboard shortcuts
#     def keyPressEvent(self, event):

#         super(MainGuiWindow, self).keyPressEvent(event)

#         # atom output shortcut
#         if event.key() == QtCore.Qt.Key_P:
            
#             print('Saved atom list from Main Window')
#             main_window.reply_log_object.append("Saved atom list from Graph-Window")

#             saving_and_output()

#         # quit the program shortcut
#         if event.key() == QtCore.Qt.Key_Q:
            
#             print('Hamster ran out!')
#             app.quit()

#         if event.key() == QtCore.Qt.Key_S:
#             save_variables()


#         if event.key() == QtCore.Qt.Key_L:
#             open_variables()

