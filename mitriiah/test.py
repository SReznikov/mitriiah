my_list = [1, 2, 3, 10, 11, 12, 15,16, 30, 31, 32]


list_1 = []
list_2 = []

groups = {}


prev_item = 0
group = 1
current_item = 0

groups["group_%s" % group] = {}
groups["group_%s" % group]["list"] = []

# while n == 20:


# 	for n in my_list:
# 		# diff = abs(1 - (my_list[n-1])
# 		diff = abs(n - prev_item)
		
# 		print("diff", diff)
# 		if diff == 1:
# 			print("current num", n)
# 			groups["group_%s" % group]["list"].append(n)
# 			print("the list%s" % group, groups["group_%s" % group]["list"])
# 			prev_item = n
# 		else:

# 			if diff > 1:
# 				print("gap")
# 		# 		print(groups["group_%s" % group]["list"])
# 		# 		prev_item = n
# 				group = group+1
# 		# 	# 	print(my_list[n-1])
# 				print(group)


# 				#break

# 	n == 1
# 				

diff = abs(current_item - prev_item)
index_counter = 0 

def start():
	global prev_item
	global group
	global current_item
	global index_counter
	# global diff

	current_list = []


	for n in my_list[index_counter::]:
		current_item = n
		print("current_item", current_item)
		print("prev_item", prev_item)
		# diff = abs(1 - (my_list[n-1])
		# diff = abs(n - prev_item)
		diff = abs(current_item - prev_item)
		print("diff", diff)
		if diff == 1:
			# print("current num", n)
			current_list.append(n)
			print("current list", current_list)
			# groups["group_%s" % group]["list"].append(n)
			# print("the list%s" % group, groups["group_%s" % group]["list"])
			prev_item = n
			index_counter += 1
			print("index", index_counter)
			
			groups["group_%s" % group] = {}
			groups["group_%s" % group]["list"] = current_list
			print(groups.keys())
		if diff > 1:
			# groups["group_%s" % group] = {}
			# groups["group_%s" % group]["list"] = current_list
			prev_item = current_item-1
			print("prev_item", prev_item)
			# switch()
			print("gap")
		# 		print(groups["group_%s" % group]["list"])
		# 		prev_item = n
			group += 1
		# 	# 	print(my_list[n-1])
			print(group)
			print(groups.keys())
			start()
			break

# def adding():
# 	global prev_item
# 	global group
# 	global current_item
# 	# global diff

# 	current_list = []

# 	for n in my_list:
# 		print(n)
# 		if current_item == n:
# 			current_item = n
# 			# current_item = n
# 			print(n)
# 			print("current_item", current_item)
# 			# diff = abs(1 - (my_list[n-1])
# 			print("prev_item", prev_item)
# 			diff = abs(current_item - prev_item)
# 			print("diff", diff)
# 			if diff == 1:
# 				current_list.append(n)
# 				print("current list", current_list)
# 				# print("current num", n)
# 				# groups["group_%s" % group]["list"].append(n)
# 				# print("the list%s" % group, groups["group_%s" % group]["list"])
# 				groups["group_%s" % group] = {}
# 				groups["group_%s" % group]["list"] = current_list
# 				print(groups.keys())

# 				prev_item = n
# 			if diff > 1:
# 				prev_item = current_item-1
# 				print("prev_item", prev_item)
# 				print(groups.keys())
# 				switch()
# 				break


start()
print(groups.keys())
print(groups.values())


# def switch():
# 	global group

# 	print("gap")
# # 		print(groups["group_%s" % group]["list"])
# # 		prev_item = n
# 	group += 1
# # 	# 	print(my_list[n-1])
# 	print(group)
# 	print(groups.keys())
# 	adding()

	

				#break

