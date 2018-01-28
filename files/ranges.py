from PyQt4 import QtCore, QtGui
import global_vars

# global_vars = global_vars.useMyVars(0)

# object containing the ranges functionality
class SelectedRangeList(QtGui.QListWidget):

    def __init__(self, ranges_list):
        super(SelectedRangeList, self).__init__()

        self.redraw_range_list()

    def redraw_range_list(self):
        self.clear()

        ranges_list = global_vars.ranges_list


        for range_name, range_list in ranges_list.items():

            range_item = QtGui.QListWidgetItem("%s : " " %s " "to" " %s " "atoms selected: " " %s"  % (range_name, range_list['from_val'], range_list['to_val'], range_list['current_atoms'] ))

            range_item.my_range = {'range_number': range_name}

            self.addItem( range_item )


    # adding specific atoms to a selected range
    def add_atoms_by_range(self):

        atom_val_list = global_vars.atom_val_list
        
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

        atom_val_list = global_vars.atom_val_list

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

        global_vars.atom_val_list
        global_vars.default_atoms

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




        atom_val_list_out = (' '.join(str(e) for e in global_vars.atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        
        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        main_window.reply_log_object.append("full chosen atoms list:")
        main_window.reply_log_object.append(str(atom_val_list_out))


        self.redraw_range_list()
        main_window.selected_residues_list_object.redraw_res_list()


    def delete_default_atoms_by_range(self):

        global_vars.atom_val_list
        global_vars.default_atoms

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
        
        global_vars.atom_val_list

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

        global_vars.atom_val_list

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

        global_vars.ranges_list
        global_vars.atom_val_list


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