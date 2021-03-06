import shelve
# import __main__ as main

main_window = None
args = None


chain_num = 0 
chain_num_rmsf = 0
chain_list = {} # list of chains from the gro file
chain_list["chain_%s" % chain_num] = {}

for i in range(15):
    chain_list["chain_%s" % i] = {}



chain_list["chain_%s" % chain_num]["rmsf_data"] = {}
chain_list["chain_%s" % chain_num]["rmsf_data"]["rmsf_val"] = []
chain_list["chain_%s" % chain_num]["rmsf_data"]["rmsf_res"] = []

# chain_list["chain_%s" % chain_num] = {}
chain_list["chain_%s" % chain_num]["gro_data"] = {}
chain_list["chain_%s" % chain_num]["gro_data"]["resval"] = []
chain_list["chain_%s" % chain_num]["gro_data"]["resname"] = []
chain_list["chain_%s" % chain_num]["gro_data"]["atomval"] = []
chain_list["chain_%s" % chain_num]["gro_data"]["atomname"] = []
chain_list["chain_%s" % chain_num]["min"] = {}
chain_list["chain_%s" % chain_num]["max"] = {}


chosen_chain = 1

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
atom_val_list_out = ()

## ranges
ranges_list = {} # dict containing all the chosen ranges
# from_vals = []
# to_vals = []
# min_res = None
# max_res = None

n = 1 # range counter


to_vals = []
from_vals = []
numbers_in_ranges = []

default_atoms = ["CA", "C", "N", "O"]


# Points selection on graph:
def add_point_by_mouse(event):

	# selected_points = selected_points
    global selected_points
    global selected_residues
    global x_a_res
    global y_a_rmsf
    global ranges_list
    global chain_list

    if event.button == 3: # right mouse button (1 = LMB, 2 = wheel, 3 = RMB)


        if event.xdata == None:
            return

        mx_l = event.xdata - 5 # 5 residues either side from where the mouse was clicked to consider for lowest rmsf
        mx_h = event.xdata + 5
        lowest_point = None # lowest rmsf value 
        x_of_lowest_point = None


        # check if point is within range, set lowest point. 
        for index, curr_point in enumerate(x_a_res):
        # for index, curr_point in enumerate(chain_list["chain%s" % chain_num]["rmsf_data"]["x_a_res"]):
            
            if curr_point > mx_l and curr_point < mx_h: # is it within the range?
                
                if lowest_point is None: # did we set the lowest point?
                    lowest_point = y_a_rmsf[index] # just use the first one
                    # lowest_point = chain_list["chain%s" % chain_num]["rmsf_data"]["y_a_rmsf"][index]
                    x_of_lowest_point = x_a_res[index]
                    # x_of_lowest_point = chain_list["chain%s" % chain_num]["rmsf_data"]["x_a_res"][index]

                    
                
                if y_a_rmsf[index] < lowest_point: # look for the lowest point
                    lowest_point = y_a_rmsf[index]
                    x_of_lowest_point = x_a_res[index]



                # if chain_list["chain%s" % chain_num]["rmsf_data"]["y_a_rmsf"][index] < lowest_point: # look for the lowest point
                #     lowest_point = chain_list["chain%s" % chain_num]["rmsf_data"]["y_a_rmsf"][index]
                #     x_of_lowest_point = chain_list["chain%s" % chain_num]["rmsf_data"]["x_a_res"][index]


        # add the selected lowest point to the list of selected points   
        if not [point for point in selected_points if point['x'] == x_of_lowest_point]:

            z = 0

            for a_range in ranges_list:

                if x_of_lowest_point < ranges_list[a_range]["from_val"] or x_of_lowest_point > ranges_list[a_range]["to_val"]:
                    
                    z = 0

                else:
            
                    z = 1
                    print("Error: Residue(s) already in another range")
                    main_window.reply_log_object.append("Error: Residue(s) already in another range")
                    break

            if z == 0:
                

                if x_of_lowest_point != None and lowest_point != None: 
                    selected_points.append({"x":x_of_lowest_point, "y":lowest_point}) # add our lowest point to list of selected points only if residue number isn't already present in the list
                    selected_points = sorted(selected_points, key=lambda item: item["x"])

                    # for every added point, add corresponding data from .gro file:
                    for index, select_res in enumerate(gro_residue_val):
                        if select_res == x_of_lowest_point: # check if residue number of our point is in .gro and add other variables to the list

                            selected_residues.append(
                                {
                                    "resval":gro_residue_val[index], 
                                    "resname":gro_residue_name[index], 
                                    "atomname":gro_atom_name[index], 
                                    "atomval":gro_atom_number[index]
                                }
                            )
                            selected_residues = sorted(selected_residues, key=lambda item: item["atomval"])
                        

        # add selected_points (residue value and rmsf value) to the selected_points_list (also displayed)
        
        main_window.selected_points_list_object.add_points()


        #refresh the list display
        main_window.selected_residues_list_object.redraw_res_list() 
        main_window.graph_object.redraw_graph()


# save the chosen atom numbers to a new .ndx file and generate a posres.itp file. Also prints the values in the terminal. 
def saving_and_output():

    atom_val_list_2 = sorted(int(e) for e in atom_val_list)

    atom_val_list_out_2 = (' '.join(str(e) for e in atom_val_list_2)) # exclude brackets, keep the list sorted in ascending order

    atom_val_list_split = atom_val_list_out_2.split(' ')

    for s, value in enumerate(atom_val_list_split):
        if s != 0 and s % 14 == 0:
            atom_val_list_split[s] = value + '\n'

    atom_val_list_split_2 = (' '.join(atom_val_list_split))
    #save index
    # atom_val_list_out = (' '.join(str(e) for e in atom_val_list)) # exclude brackets, keep the list sorted in ascending order
    gro_filename = args.my_gro_filename

    print('[your_chosen_atoms]')
    print(atom_val_list_out)
    main_window.reply_log_object.append("[your_chosen_atoms]")
    main_window.reply_log_object.append(atom_val_list_out_2)

    with open(gro_filename[:-4] + "_atoms_index.ndx", 'wt') as out:
        out.write( "[ chosen_atoms ]" + '\n')
        out.write( '\n' )
        out.write((atom_val_list_split_2) + '\n')
     
    with open(gro_filename[:-4] + "_posres.itp", 'w') as out:
        out.write( "[ position_restraints ]" + '\n')
        out.write( "; atom  type      fx      fy      fz" + '\n')
        
        '''
            1
           40
          808     1  1000  1000  1000
         1549     1  1000  1000  1000
        23904

        '''

        posre_list = [] # list of renumbered atoms corresponding to selected atoms

        # gro_atom_number_out = (' '.join(str(g) for g in gro_atom_number)) 
        total_atoms = len(gro_atom_number) # total number of atoms in the file
        renum_vals = range(1, total_atoms+1) # new numbering from 1 for posres
        posre_dict = zip(renum_vals, gro_atom_number) # dictionary containing original atom numbers and the corresponding renumbered ones

        # create a new renumbered selected atom list
        for renum, atmnum in posre_dict:
            for atom_val in atom_val_list_2:
                if atom_val == atmnum:
                    posre_list.append(renum)


        for s in posre_list:
            if s >= 0 and s < 10:
                out.write("     %s     1  1000  1000  1000\n" % s)

            if s >= 10 and s < 100:
                out.write("    %s     1  1000  1000  1000\n" % s)

            if s >= 100 and s < 1000:
                out.write("   %s     1  1000  1000  1000\n" % s)

            if s >= 1000 and s < 10000:
                out.write("  %s     1  1000  1000  1000\n" % s)

            if s >= 10000:
                out.write(" %s     1  1000  1000  1000\n" % s)




def save_variables():
    atom_val_list_2 = sorted(int(e) for e in atom_val_list)

    atom_val_list_out_2 = (' '.join(str(e) for e in atom_val_list_2)) # exclude brackets, keep the list sorted in ascending order

    
    saved_vars = {}
    saved_vars['x_a_res'] = x_a_res
    saved_vars['y_a_rmsf'] = y_a_rmsf
    saved_vars['selected_points'] = selected_points 
    saved_vars['selected_points_x'] = selected_points_x 
    saved_vars['selected_points_y'] = selected_points_y 
    saved_vars['gro_residue_val'] = gro_residue_val
    saved_vars['gro_residue_name'] = gro_residue_name
    saved_vars['gro_atom_name'] = gro_atom_name
    saved_vars['gro_atom_number '] = gro_atom_number 
    saved_vars['selected_residues'] = selected_residues 
    saved_vars['atom_val_list'] = atom_val_list 
    saved_vars['atom_val_list_2'] = atom_val_list_2 
    saved_vars['ranges_list'] = ranges_list 
    saved_vars['n'] = n 


    gro_filename = args.my_gro_filename
    my_shelf = shelve.open(gro_filename[:-4] + "_saved_session.out", 'n')

    for key, value in saved_vars.items():

        if not key.startswith('__'):
            try:
                my_shelf[key] = value
            except Exception:
                print('ERROR saving: "%s"' % key)
            
    my_shelf.close()

    print('saved session')
    main_window.reply_log_object.append("session saved")


def open_variables():

    gro_filename = args.my_gro_filename
    my_shelf = shelve.open(gro_filename[:-4] + "_saved_session.out")
    for key in my_shelf:
        globals()[key]=my_shelf[key]

    main_window.graph_object.redraw_graph()
    main_window.selected_points_list_object.add_points()
    main_window.selected_residues_list_object.redraw_res_list() 
    main_window.select_ranges_list_object.redraw_range_list()

    my_shelf.close()

    print("previous session loaded")
    main_window.reply_log_object.append("previous session loaded")


def log_update():

    atom_val_list_2 = sorted(int(e) for e in atom_val_list)

    atom_val_list_out_2 = (' '.join(str(e) for e in atom_val_list_2)) # exclude brackets, keep the list sorted in ascending order

    print('[your_chosen_atoms]')
    if atom_val_list_out:

        print(atom_val_list_out_2)

    else:
        print("None")    

    main_window.reply_log_object.append("full chosen atoms list:")
    if atom_val_list_out:
        main_window.reply_log_object.append(str(atom_val_list_out_2))
    else:
        main_window.reply_log_object.append("None")