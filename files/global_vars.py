# Data from rmsf.xvg file
x_a_res, y_a_rmsf = [], [] 

# List of selected points
selected_points = [] # residue value and rmsf value from graph selection

selected_points_x = [] # residue value
selected_points_y = [] # rmsf value

# List of values from gro_file
gro_residue_val, gro_residue_name, gro_atom_name, gro_atom_number = [], [], [], []


##RMSF
selected_residues = [] # residue name+value and atom name+value derived from selected_points

atom_val_list = [] # list of atom numbers obtained from user selection

## ranges
ranges_list = {} # dict containing all the chosen ranges
n = 1 # range counter

default_atoms = ["CA", "C", "N", "O"]
