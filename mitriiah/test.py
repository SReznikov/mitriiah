my_list = [1, 2, 3, 10, 11, 12]

list_1 = []
list_2 = []

groups = {}


prev_item = 0
group = 1

groups["group_%s" % group] = {}
groups["group_%s" % group]["list"] = []

for n in my_list:
	# diff = abs(1 - (my_list[n-1])
	diff = abs(n - prev_item)
	
	print("diff", diff)
	if diff == 1:
		print("current num", n)
		groups["group_%s" % group]["list"].append(n)
		print("the list", groups["group_%s" % group]["list"])
		prev_item = n
	

		if diff > 1:
			print("gap")
	# 		print(groups["group_%s" % group]["list"])
	# 		prev_item = n
			group = group+1
	# 	# 	print(my_list[n-1])
			