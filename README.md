# mitriiah

### Prerequisites:

- PyQt4
- matplotlib

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

Priority

- fix ranges functionality (deleting atoms from list, merging the temp.var to the current working var, putting restrictions on values entered, approperiate labelling and placement in the program)

- selection of default/desired atom all at once in the list
- generation of posres.itp along with .ndx files
- fix column selection


Nice to have

- splitting a column in .gro into two separate ones
- menu bar allowing to open multiple rmsf/gro in new tabs
- ability to delete points from graph by clicking on them
- possibly use table view instead of list view
- add rectangle selector for conveniance

Maybe will get there one day

- calling gromacs as an option to create a full index file
- path selection + save button for outputting the atom list
- Fix the zoom function (currently resets the view once a point is chosen on the graph)


### Known bugs

- Atom window not showing results. This is if the number of columns in the .gro file is less than 9; sometimes this is the case pre-simulation. In the script need to change the column number to be maching the amount in the gro file.

- For large systems the atom name and atom number lose space separation. The program will not be able to separate this into two columns and will not work. To fix this a space has to be added between the two merged columns. This can be done relatively quickly in a text editor like emacs or sublime.


# ranges

### About

A script which allows selection of atoms within a range. 


### Usage 

The input from/to asks for residue number to get the range from and to (including the entered residues).

Type in which atoms to select by name i.e. if you want all CA atoms within the range etc.


