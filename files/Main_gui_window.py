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
        global selected_range
        global gro_residue_val
        from_input = self.from_res.text()
        to_input = self.to_res.text()

        min_res = min(gro_residue_val)
        max_res = max(gro_residue_val)

        print('min res, max res:')
        print(min_res , max_res)


        if (int(from_input)) < min_res or (int(to_input)) > max_res:

            print("Error: number entered out of bounds")
            self.reply_log_object.append("Error: number entered out of bounds")

        else:
            res_range = list(range(int(from_input), int(to_input) + 1))


            print(res_range)

            self.reply_log_object.append("residues range:")
            self.reply_log_object.append(str(res_range))

            for i in res_range:
                num = i
                for index, select_res in enumerate(gro_residue_val):
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
 

    def atom_selection(self):
            
        self.select_atm_button = QtGui.QPushButton("Submit")
        self.select_atm_button.setFixedWidth(80)

        self.select_atm_button.clicked.connect(self.atom_button_clicked) 

    def atom_deletion(self):
            
        self.delete_atm_button = QtGui.QPushButton("Delete")
        self.delete_atm_button.setFixedWidth(80)

        self.delete_atm_button.clicked.connect(self.atom_deletion_clicked)

    def atom_button_clicked(self):
            global selected_range
            global atom_val_list
            current_atoms = []
           
            atom_input = self.atm_nam.text()
                      
            self.reply_log_object.append("Atoms added")
            for item in selected_range:
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
        global selected_range
        global atom_val_list
        
        atom_input = self.atm_nam.text()

        for_deleting = []

        self.reply_log_object.append("Atoms deleted")
        for index, item in enumerate(selected_range):
            if item["atomname"] == atom_input:
                self.reply_log_object.append(str(item))
                for_deleting.append(selected_range[index])


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

        # atom selector for residue range
        range_atm_layout_opt = QtGui.QHBoxLayout()
        range_atm_layout_opt.addWidget(self.atm_nam)
        range_atm_layout_opt.addWidget(self.select_atm_button)
        range_atm_layout_opt.addWidget(self.delete_atm_button)

        # default atom gui + range of residues gui
        range_layout = QtGui.QVBoxLayout()
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