my_list = [1, 2, 3, 10, 11, 12, 15,16, 30, 31, 32]


groups = {}
prev_item = 0
group = 1
current_item = 0
index_counter = 0 

def start():
	global prev_item
	global group
	global current_item
	global index_counter


	current_list = []


	for n in my_list[index_counter::]:
		current_item = n
		diff = abs(current_item - prev_item)

		if diff == 1:

			current_list.append(n)
			prev_item = n
			index_counter += 1

			groups["group_%s" % group] = {}
			groups["group_%s" % group]["list"] = current_list

		if diff > 1:

			prev_item = current_item-1

			group += 1

			start()
			break


start()

print(groups.keys())
print(groups.values())


for chain in range(group+1):
	if chain != 0:
		first_res = min(groups["group_%s" % chain]["list"])
		last_res = max(groups["group_%s" % chain]["list"])

		print(chain,":", "chain %s" % chain, "- residues", first_res, "to", last_res)


var = input("chain to load: ")

## restrict the input
## link it to the group (print the values from the selected group)

print("loading " + str(var))