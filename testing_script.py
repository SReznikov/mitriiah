main_dict = []
d = {}
n = 1
# n = 0
atom_info_dict = []
full_list = []
# atom_info_dict = []

my_range = []

a_from_res = 10
a_to_res = 11
a_resval = 14
a_atmval = 1305
a_atmnam = 'C'
a_gro_residue_val = [1, 2]

a_atom_info_dict = []

a_res_range_a = range(a_from_res, a_to_res)
a_res_range = list(range(int(a_from_res), int(a_to_res) + 1))

# print(a_res_range)
# print(a_gro_residue_val)

for i in a_res_range:
    num = i
    for index, res in enumerate(a_gro_residue_val):
        # if res == num: # check if residue number of our point is in .gro and add other variables to the list
        # atom_info_dict.append(
        #     {
        #         "a_resval":a_resval, 
        #         "a_atomname":a_atmnam, 
        #         # "a_atomval":a_atmval
        #     }
        # )
        d["range%s" % n] = {
                "a_resval":a_resval, 
                "a_atomname":a_atmnam, 
                # "a_atomval":a_atmval
            }
n += 1        
print(d)
print(d['range1'])

# print(full_list)
# print(atom_info_dict)
# main_dict = full_list + [atom_info_dict]
# print('main dict')
# print(main_dict)
# full_list = main_dict
# print('full list')
# print(full_list)
# atom_info_dict = []
# # print(a_atom_info_dict)
#     # atom_info_dict = sorted(atom_info_dict, key=lambda item: item["atomval"])

b_from_res = 13
b_to_res = 14
b_resval = 20
b_atmval = 4305
b_atmnam = 'N'
b_gro_residue_val = [4, 5]


b_atom_info_dict = []

b_res_range_a = range(b_from_res, b_to_res)
b_res_range = list(range(int(b_from_res), int(b_to_res) + 1))

# print(b_res_range)
# print(b_gro_residue_val)

for i in b_res_range:
    num = i
    for index, res in enumerate(b_gro_residue_val):
        d["range%s" % n] = {
                "a_resval":a_resval, 
                "a_atomname":a_atmnam, 
                # "a_atomval":a_atmval
            }
n += 1       
print(d)
print(d['range2'])

        # if res == num: # check if residue number of our point is in .gro and add other variables to the list
        # atom_info_dict.append(
        #     {
        #         "b_resval":b_resval, 
        #         "b_atomname":b_atmnam, 
        #         # "b_atomval":b_atmval
        #     }
        # )
# main_dict = full_list + [atom_info_dict]
# # full_list = main_dict

# print('main_dict')
# print(main_dict)

# # print(b_atom_info_dict[0]['a_atomval'])
# print('selection')
# print(main_dict[1][1])

# # print(main_dict.my_range[0]['a_atomval'])