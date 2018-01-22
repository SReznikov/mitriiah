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