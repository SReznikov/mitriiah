# mitriiah

### Introduction:

Mitriiah is a gui based program created to aid in the preparation of files for umbrella sampling in GROMACS. It accepts GRO files along with it's corresponding RMSF data, and writes index and positional restraint files to be used further in GROMACS. The program allows the user to choose both visually and in bulk which atoms are desired to be restrained. There are two ways of picking the atoms which are mostly compatible with each other (more on that later) - picking residues by lowest RMSF value and picking residues by range. The RMSF data is plotted which allows the user to pick lowest value rmsf residues to be used in the atom selection. The range selection allows the user to input which range of residues is required to pick atoms from. Multiple ranges are allowed and are editable individually. Both the RMSF and ranges allow individual choice of atoms, default atoms (backbone atoms), and all atoms to be selected for output. The work can be saved at any point and retrieved later. 


### Tutorial:

### Setup and Usage:


To run, the rmsf file along with the corresponding .gro file, are required and are specified with the -r and -c flags respecively e.g :

```bash
./mitriiah.py -r rmsf.xvg -c protein.gro
```


For multi chain systems, each chain/model has to be worked on separately. In the end .ndx file and posres.itp file will be produced. 
1. Run normal simulation. get rmsf for each model/chain in the simulation.
2. follow standard umbrella preparation to get the gro file, .itp and topol.itp files (after pdb2gmx) - for each model/chain a separate posres + topol.
3. cut your new gro file into separate files containing one chain/model each.
4. in the program use the new gro file along with its corresponding rmsf. 

To select residues with the lowest rmsf, right click on the graph in the area you want the selection. The lowest point within the click will be added to the selected residues list/window.

You can delete unwanted points by selecting them in the selections window and pressing 'delete'.

In order to select desired atoms to be outputted as an index, select the atom in the atoms selection window and press 'v'. To remove from your selections press 'b'.

Atoms can also be selected by chosing the wanted option ('default' or 'all') and clicking 'select'.

To output the atom seletionspress 'p'. A new .ndx and posres.itp file containing only the group of selected atoms will also be created. You can copy and paste the contents of the new .ndx to your already existing index file. 

The selection by range and RMSF is linked - deletion or selection in one method will affect the atoms selected/deleted in the other method. 

### Quick Guide:

'delete key' - delete the selected residue (use in the selections window)

'v' - add currently selected atom to your atoms list

'b' - remove currently selected atom from your atoms list

'p' - output all your selections into a .ndx file and print the list in the terminal

's' - save current state

'l' - load previous session

'q' - quit
 
### Known bugs

- For large systems the atom name and atom number lose space separation. The program will not be able to separate this into two columns and will not work. To fix this a space has to be added between the two merged columns. This can be done relatively quickly in a text editor like emacs or sublime.




