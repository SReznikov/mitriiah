# mitriiah

### About:

Mitriiah is a gui based program created to aid in the preparation of files for umbrella sampling in GROMACS. 

It accepts GRO files along with it's corresponding RMSF data, and writes index and positional restraint files to be used further in GROMACS. The program allows the user to choose both visually and in bulk which atoms are desired to be restrained. 

There are two ways of picking the atoms which are mostly compatible with each other - picking residues by lowest RMSF value and picking residues by range. 

The RMSF data is plotted which allows the user to pick lowest value rmsf residues to be used in the atom selection by right clicking on the graph. The range selection allows the user to input which range of residues is required to pick atoms from. Multiple ranges are allowed and are editable individually. 

Both the RMSF and ranges allow individual choice of atoms, default atoms (backbone atoms), and all atoms to be selected for output. The work can be saved at any point and retrieved later.

### Setup:

Before running the program make sure you have the pre-requisites installed. Below are some suggested ways of installing:

- PyQt4
```bash
sudo apt-get install python3-pyqt4
```

- matplotlib
```bash
sudo apt-get install python3-matplotlib
```

- python3 - check the version with 
```bash
 python3 --version```
 Install/update if required.


To run, the rmsf file along with the corresponding .gro file, are required and are specified with the -r and -c flags respecively e.g :

If you're in the mitriiah folder:

```bash
./__main__.py -r rmsf.xvg -c protein.gro
```

or if you're outside of it you can call the whole folder:

```bash
python3 mitriiah -r rmsf.xvg -c protein.gro
```


Please refer to the guide file for more detailed desciption and instructions.

### Contact:

To give feedback or report any bugs, please email s.renikov@newcastle.ac.uk