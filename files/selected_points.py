from PyQt4 import QtCore, QtGui

from reply_log import ReplyLog
import app as app


# object containing the selected points from the graph list
class SelectedPointsList(QtGui.QListWidget):
    def __init__(self, selected_points):
        super(SelectedPointsList, self).__init__()
    

    def add_points(self):

        self.clear()
        for point in app.selected_points:
            list_item = QtGui.QListWidgetItem("res: %d rmsf: %s" % (point['x'], point['y']))
            list_item.my_point = point # keep 'point' info for reference
              
            self.addItem( list_item ) # add visually line by line



    # deleting of items in rows
    def keyPressEvent(self, event):

        super(SelectedPointsList, self).keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_Delete:
            
            for item in self.selectedItems():

                # update the selected points list when deleting
                for index, point in enumerate(app.selected_points):
                    if( point['x'] == item.my_point['x']):
                        del app.selected_points[index]


                temp_res_list = []

                # update the selected residues list when deleting
                for index, vals in enumerate(app.selected_residues):
                    if (vals['resval'] != item.my_point['x']):
                        
                        temp_res_list.append( app.selected_residues[index] )
                    
                app.selected_residues = temp_res_list
                self.takeItem(self.row(item)) # delete the row visually

                # clear corresponding atoms out of memory
                temp_atom_list = []
                for index, atom in enumerate(app.atom_val_list):
                    for val in app.selected_residues:
                        
                        if atom == val['atomval']:
                            temp_atom_list.append(app.atom_val_list[index])

                app.atom_val_list = temp_atom_list


        atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order


        print('[your_chosen_atoms]')
        print(atom_val_list_out)
        app.main_window.reply_log_object.append("full chosen atoms list:")
        app.main_window.reply_log_object.append(str(atom_val_list_out))

        app.main_window.graph_object.redraw_graph()
        app.main_window.selected_residues_list_object.redraw_res_list()

        
        # atom numbers printing and saving shortcut
        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list from selction window')
            app.main_window.reply_log_object.append("Saved atom list from selection window")

            app.saving_and_output()

        # quit the program shortcut
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')

            app.qapp.quit()

        if event.key() == QtCore.Qt.Key_S:
            app.save_variables()


        if event.key() == QtCore.Qt.Key_L:
            app.open_variables()