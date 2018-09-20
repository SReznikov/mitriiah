import itertools 

my_list = [1, 2, 3, 10, 11, 12, 15,16, 5, 6, 7]
my_list_data = ["a","b","c","d","e","f","g","h","i","j","k"]

rmsf_list = [1, 2, 3, 10, 11, 12, 15,16, 30, 31, 32]

groups = {}
prev_item = 0
prev_rmsf_item = 0
group = 1
current_item = 0
current_rmsf_item = 0 
index_counter = 0 
index_rmsf_counter = 0 

def chain_splitter():
	global prev_item
	global group
	global current_item
	global index_counter



	current_list = []
	current_data_list = []
	current_rmsf_list = []


	for n, d, r in zip(my_list[index_counter::], my_list_data[index_counter::], rmsf_list[index_counter::]):
		current_item = n
		diff = abs(current_item - prev_item)

		if diff == 1:

			current_list.append(n)
			current_data_list.append(d)
			current_rmsf_list.append(r)
			prev_item = n
			index_counter += 1

			groups["group_%s" % group] = {}
			groups["group_%s" % group]["gro_data"] = {}
			groups["group_%s" % group]["group"] = group
			groups["group_%s" % group]["gro_data"]["list"] = current_list
			groups["group_%s" % group]["gro_data"]["data"] = current_data_list
			groups["group_%s" % group]["gro_data"]["rmsf"] = current_rmsf_list

		if diff > 1:

			prev_item = current_item-1

			group += 1

			chain_splitter()
			break


def user_select():

	for chain in range(group+1):
		if chain != 0:
			first_res = min(groups["group_%s" % chain]["gro_data"]["list"])
			last_res = max(groups["group_%s" % chain]["gro_data"]["list"])

			print(chain,":", "chain %s" % chain, "- residues", first_res, "to", last_res)


	chain_to_load = int(input("chain to load: "))

	## restrict the input
	## link it to the group (print the values from the selected group)

	print("loading " + str(chain_to_load))

	# for chain_loading in groups["group_%s" % chain]:
	# 	if chain_to_load == groups["group_%s" % chain_to_load] :
	# 		print("chain 1")


	for chain in range(group+1):
		if chain != 0:	
			if chain_to_load == groups["group_%s" % chain]["group"] :
				print(groups["group_%s" % chain])
				break


chain_splitter()

print(groups.keys())
print(groups.values())

user_select()

