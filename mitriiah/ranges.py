from PyQt4 import QtCore, QtGui

from reply_log import ReplyLog
import app as app


# object containing the ranges functionality
class SelectedRangeList(QtGui.QListWidget):


    def __init__(self, ranges_list):
        super(SelectedRangeList, self).__init__()

        self.redraw_range_list()

    def redraw_range_list(self):
        self.clear()

        for range_name, range_list in app.ranges_list.items():

            range_item = QtGui.QListWidgetItem("range : " " %s " "-" " %s " " | " "atoms selected: " " %s"  % ( range_list['from_val'], range_list['to_val'], range_list['current_atoms'] ))

            range_item.my_range = {'range_number': range_name}

            self.addItem( range_item )


    # adding specific atoms to a selected range
    def add_atoms_by_range(self):

        current_atoms = []


        for item in self.selectedItems():

            for range_name, range_list in app.ranges_list.items():

                if range_name == item.my_range['range_number']:

                    for atom_name in app.ranges_list[range_name]['range']:

                        if atom_name['atomname'] == app.main_window.atom_input:

                            if not [point for point in app.atom_val_list if point == atom_name['atomval']]:
                                        app.atom_val_list.append( atom_name['atomval'])
                                        app.atom_val_list = sorted(app.atom_val_list, key=lambda item: atom_name['atomval'])
                                        current_atoms.append( atom_name['atomval'])

                            if not [point for point in app.ranges_list[range_name]["current_atoms"] if point == atom_name['atomname']]:

                                app.ranges_list[range_name]["current_atoms"].append(atom_name['atomname'])

                    

            app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order
            

            self.redraw_range_list()
            app.main_window.selected_residues_list_object.redraw_res_list()
            app.main_window.graph_object.redraw_graph()
            app.log_update()

    # deleting specific atoms
    def delete_atoms_by_range(self):

        for_deleting = []


        for item in self.selectedItems():

            for range_name, range_list in app.ranges_list.items():

                if range_name == item.my_range['range_number']:

                    for atom_name in app.ranges_list[range_name]['range']:

                        if atom_name['atomname'] == app.main_window.atom_input:
                            for_deleting.append(atom_name['atomval'])

                            for index, val in enumerate(app.atom_val_list):
                                for point in for_deleting:

                                    if point == val:
                                        del app.atom_val_list[index]

                    for index, atom in enumerate(app.ranges_list[range_name]['current_atoms']):
                        if atom == app.main_window.atom_input:
                            del app.ranges_list[range_name]['current_atoms'][index]
                        

        app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        


        self.redraw_range_list()
        app.main_window.selected_residues_list_object.redraw_res_list()
        app.main_window.graph_object.redraw_graph()
        app.log_update()

    
    def add_default_atoms_by_range(self):

        for item in self.selectedItems():

            for range_name, range_list in app.ranges_list.items():

                if range_name == item.my_range['range_number']:

                    for atom_name in app.ranges_list[range_name]['range']:

                        for atom in app.default_atoms:

                            if atom_name['atomname'] == atom:

                                if not [point for point in app.atom_val_list if point == atom_name['atomval']]:
                                            app.atom_val_list.append( atom_name['atomval'])
                                            app.atom_val_list = sorted(app.atom_val_list, key=lambda item: atom_name['atomval'])
                                   
                                if not [point for point in app.ranges_list[range_name]["current_atoms"] if point == atom_name['atomname']]:


                                    app.ranges_list[range_name]["current_atoms"].append(atom_name['atomname'])




        app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order


        self.redraw_range_list()
        app.main_window.selected_residues_list_object.redraw_res_list()
        app.log_update()


    def delete_default_atoms_by_range(self):

        for_deleting = []


        for item in self.selectedItems():

            for range_name, range_list in app.ranges_list.items():

                if range_name == item.my_range['range_number']:

                    for atom_name in app.ranges_list[range_name]['range']:

                        for atom in app.default_atoms:

                            if atom_name['atomname'] == atom:

                                for_deleting.append(atom_name['atomval'])

                                for index, val in enumerate(app.atom_val_list):
                                    for point in for_deleting:
                                        if point == val:
                                            del app.atom_val_list[index]

                        for index, atom in enumerate(app.ranges_list[range_name]['current_atoms']):
                            del app.ranges_list[range_name]['current_atoms'][index]



        app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        
        self.redraw_range_list()
        app.main_window.selected_residues_list_object.redraw_res_list()
        app.log_update()


    def add_all_atoms_by_range(self):
        
        for item in self.selectedItems():

            for range_name, range_list in app.ranges_list.items():

                if range_name == item.my_range['range_number']:

                    for atom_name in app.ranges_list[range_name]['range']:

                        if not [point for point in app.atom_val_list if point == atom_name['atomval']]:
                            app.atom_val_list.append( atom_name['atomval'])
                            app.atom_val_list = sorted(app.atom_val_list, key=lambda item: atom_name['atomval'])

                        if not [point for point in app.ranges_list[range_name]["current_atoms"] if point == atom_name['atomname']]:
                            app.ranges_list[range_name]["current_atoms"].append(atom_name['atomname'])



        app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order


        self.redraw_range_list()
        app.main_window.selected_residues_list_object.redraw_res_list()
        app.log_update()



    def delete_all_atoms_by_range(self):

        for_deleting = []


        for item in self.selectedItems():

            for range_name, range_list in app.ranges_list.items():

                if range_name == item.my_range['range_number']:

                    for atom_name in app.ranges_list[range_name]['range']:

                        for_deleting.append(atom_name['atomval'])

                        for index, val in enumerate(app.atom_val_list):
                            for point in for_deleting:
                                if point == val:
                                    del app.atom_val_list[index]

                        for index, atom_name in enumerate(app.ranges_list[range_name]['current_atoms']):
                            del app.ranges_list[range_name]['current_atoms'][index]



        app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        
        self.redraw_range_list()
        app.main_window.selected_residues_list_object.redraw_res_list()
        app.log_update()



    # deleting of items in rows
    def keyPressEvent(self, event):

        super(SelectedRangeList, self).keyPressEvent(event)

        for_deleting = []

        if event.key() == QtCore.Qt.Key_Delete:

            for item in self.selectedItems():
               
                # update the selected ranges list when deleting
                for range_name, range_list in app.ranges_list.items():

                    if range_name == item.my_range['range_number']:

                        for atom_name in app.ranges_list[range_name]['range']:

                            for_deleting.append(atom_name['atomval'])

                            for index, val in enumerate(app.atom_val_list):

                                for point in for_deleting:
                                    print(point)
                            
                                    if point == val:
                                        del app.atom_val_list[index]

                                print(app.atom_val_list)
                        
                        # print(for_deleting)
                        del app.ranges_list[range_name]
                

                self.takeItem(self.row(item)) # delete the row visually


            app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order

            

        self.redraw_range_list()
        app.main_window.graph_object.redraw_graph()
        app.main_window.selected_residues_list_object.redraw_res_list()
        app.log_update()

        # atom numbers printing and saving shortcut
        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list')
            app.main_window.reply_log_object.append("Saved atom list")

            app.saving_and_output()

        # quit the program shortcut
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')

            app.qapp.quit()

        if event.key() == QtCore.Qt.Key_S:
            app.save_variables()


        if event.key() == QtCore.Qt.Key_L:
            app.open_variables()