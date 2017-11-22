# mitriiah

### Prerequisites:

PyQt4
matplotlib

### Running:

To run, the rmsf file along with the corresponding .gro file, are required and are specified with the -r and -c flags respecively e.g :

```bash
./mitriiah.py -r rmsf.xvg -c protein.gro
```

### Usage:

To select residues with the lowest rmsf, right click on the graph in the area you want the selection. The lowest point within the click will be added to the selected residues list/window.

You can delete unwanted points by selecting them in the selections window and pressing 'delete'.

In order to select desired atoms to be outputted as an index, select the atom in the atoms selection window and press 'v'. To remove from your selections press 'b'.

To output the atom seletionspress 'p'. A new .ndx file containing only the group of selected atoms will also be created. You can copy and paste the contents to your already existing index file. 

### Quick Guide:

'delete key' - delete the selected residue (use in the selections window)
'v' - add currently selected atom to your atoms list
'b' - remove currently selected atom from your atoms list
'p' - output all your selections into a .ndx file and print the list in the terminal


### To do list:

- Fix the zoom function (currently resets the view once a point is chosen on the graph)
- add rectangle selector for conveniance
- possibly use table view instead of list view
- ability to delete points from graph by clicking on them
- path selection + save button for outputting the atom list
- calling gromacs as an option to create a full index file
