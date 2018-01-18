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