# mitriiah

### About:

Mitriiah is a gui based program created to aid in the preparation of files for umbrella sampling in GROMACS. 

It accepts GRO files along with it's corresponding RMSF data, and writes index and positional restraint files to be used further in GROMACS. The program allows the user to choose both visually and in bulk which atoms are desired to be restrained. 

There are two ways of picking the atoms which are mostly compatible with each other (more on that later) - picking residues by lowest RMSF value and picking residues by range. 

The RMSF data is plotted which allows the user to pick lowest value rmsf residues to be used in the atom selection. The range selection allows the user to input which range of residues is required to pick atoms from. Multiple ranges are allowed and are editable individually. 

Both the RMSF and ranges allow individual choice of atoms, default atoms (backbone atoms), and all atoms to be selected for output. The work can be saved at any point and retrieved later

### Contact:

To give feedback or report any bugs, please email s.renikov@newcastle.ac.uk