from PyQt4 import QtCore, QtGui

from reply_log import ReplyLog
import app as app


# object responsible for handling gro vars list (the selected residues list)
class SelectedResiduesList(QtGui.QListWidget):
    def __init__(self, selected_residues):
        super(SelectedResiduesList, self).__init__()

        self.redraw_res_list()


    # populate the list window and keep it updated
    def redraw_res_list(self):
        self.clear()

        last_line = {'resval': None}


        for val in app.selected_residues:
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


            for item in app.atom_val_list:
                if item == val['atomval']:

                    brush = QtGui.QBrush()
                    brush.setColor(QtGui.QColor('red')) 
                    res_item.setForeground(brush)


            self.addItem( res_item )

    # add default atoms
    def default_button_clicked(self):

        for atom in app.default_atoms:

            for item in app.selected_residues:

                if item["atomname"] == atom:

                    if not [point for point in app.atom_val_list if point == item['atomval']]:
                            app.atom_val_list.append( item['atomval'] )
                            app.atom_val_list = sorted(app.atom_val_list, key=lambda item: item)


                # for range_name, range_list in app.ranges_list.items():

                #     if range_name == item['resval']:

                #         for atom_name in app.ranges_list[range_name]['range']:

                #             # for atom in app.default_atoms:

                #             if atom_name['atomname'] == atom:

                #                 if not [point for point in app.atom_val_list if point == atom_name['atomval']]:
                #                             app.atom_val_list.append( atom_name['atomval'])
                #                             app.atom_val_list = sorted(app.atom_val_list, key=lambda item: atom_name['atomval'])
                                   
                #                 if not [point for point in app.ranges_list[range_name]["current_atoms"] if point == atom_name['atomname']]:


                #                     app.ranges_list[range_name]["current_atoms"].append(atom_name['atomname'])


        app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order


        app.main_window.selected_residues_list_object.redraw_res_list()
        app.main_window.select_ranges_list_object.redraw_range_list()
        app.log_update()

    # add all atoms
    def all_button_clicked(self):

        for item in app.selected_residues:

            if not [point for point in app.atom_val_list if point == item['atomval']]:
                    app.atom_val_list.append( item['atomval'] )
                    app.atom_val_list = sorted(app.atom_val_list, key=lambda item: item)


        app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order


        app.main_window.selected_residues_list_object.redraw_res_list()
        app.main_window.select_ranges_list_object.redraw_range_list()
        app.log_update()


    # delete default atoms
    def default_delete_button_clicked(self):
    
        for_deleting = []


        for atom in app.default_atoms:

            for item in app.selected_residues:

                if item["atomname"] == atom:
                    for_deleting.append(item['atomval'])


                    for index, val in enumerate(app.atom_val_list):
                        for point in for_deleting:
                            if point == val:
                                del app.atom_val_list[index]



        app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order


        app.main_window.selected_residues_list_object.redraw_res_list()
        app.main_window.select_ranges_list_object.redraw_range_list()
        app.log_update()


    # delete all atoms
    def all_delete_button_clicked(self):
    
        for_deleting = []


        for item in app.selected_residues:

            for_deleting.append(item['atomval'])

            for index, val in enumerate(app.atom_val_list):
                for point in for_deleting:
                    if point == val:
                        del app.atom_val_list[index]


        app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order


        app.main_window.selected_residues_list_object.redraw_res_list()
        app.main_window.select_ranges_list_object.redraw_range_list()
        app.log_update()
        
    # define keyboard actions
    def keyPressEvent(self, event):

        super(SelectedResiduesList, self).keyPressEvent(event)
        
        # add desired atoms to app.atom_val_list by pressing 'v'
        if event.key() == QtCore.Qt.Key_V:
            
            for item in self.selectedItems():

                item.setTextColor(QtGui.QColor("red")) 

                if not [point for point in app.atom_val_list if point == item.my_res_atom['atomval']]:
                    app.atom_val_list.append( item.my_res_atom['atomval'] )
                    app.atom_val_list = sorted(app.atom_val_list, key=lambda item: item)

        app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order
        

        app.main_window.select_ranges_list_object.redraw_range_list()
        app.log_update()
        
       

        # delete desired atoms from the atom list by pressing 'b'
        if event.key() == QtCore.Qt.Key_B:
            for item in self.selectedItems():

                item.setTextColor(QtGui.QColor("black"))

                # update the selected atoms list when deleting
                for index, atm in enumerate(app.atom_val_list):
                    if( atm == item.my_res_atom['atomval']):
                        del app.atom_val_list[index]
        

        app.atom_val_list_out = (' '.join(str(e) for e in app.atom_val_list)) # exclude brackets, keep the list sorted in ascending order

        app.main_window.select_ranges_list_object.redraw_range_list()
        app.log_update()
        

        # print and save the atom values by pressing 'p'
        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list')
            app.main_window.reply_log_object.append("Saved atom list")

            app.saving_and_output()

        # quit the program by pressing 'q'
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')

            app.qapp.quit()

        if event.key() == QtCore.Qt.Key_S:
            app.save_variables()


        if event.key() == QtCore.Qt.Key_L:
            app.open_variables()