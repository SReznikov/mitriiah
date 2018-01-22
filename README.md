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

For bigger systems, each chain/model has to be worked on separately. In the end .ndx file and posres.itp file will be produced. 
1. Run normal simulation. get rmsf for each model/chain in the simulation.
2. for umbrella prepare the gro file to get .itp and topol.itp files (after pdb2gmx) - for each model/chain a separate posres + topol.
3. cut your new gro file into separate files containing one chain/model each.
4. in the program use the new gro file along with its corresponding rmsf. 

To select residues with the lowest rmsf, right click on the graph in the area you want the selection. The lowest point within the click will be added to the selected residues list/window.

You can delete unwanted points by selecting them in the selections window and pressing 'delete'.

In order to select desired atoms to be outputted as an index, select the atom in the atoms selection window and press 'v'. To remove from your selections press 'b'.

To output the atom seletionspress 'p'. A new .ndx file containing only the group of selected atoms will also be created. You can copy and paste the contents to your already existing index file. 

The ranges feature is linked to 'by point' feature; if you have points chosen already, and you select range so that the points are within the range, the atoms will be affected - e.g. deleting CA in a range will delete CA from list if the point is falling within. 

### Quick Guide:

'delete key' - delete the selected residue (use in the selections window)

'v' - add currently selected atom to your atoms list

'b' - remove currently selected atom from your atoms list

'p' - output all your selections into a .ndx file and print the list in the terminal


### To do list:

Priority

- allow for multiple ranges work - done, need to tidy
- track of which atoms are selected - done, need to tidy

- sorting of ranges in the window
- visual feedback in the hamster log
- re-designing window wiew for clarity
- adding selections of 'default' and 'all' atoms for ranges
- prevent range duplicates and overlapping ranges
- sorting of atoms for ranges

-general debugging


- generation of posres.itp along with .ndx files -> done, tidying stage

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


