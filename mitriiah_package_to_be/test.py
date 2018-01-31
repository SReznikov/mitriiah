test_item = {"from_": 50, "to": 60,}

user_from = 30
user_to = 90

# 30 - 40 vs 50 - 60 = false

# 30 - 55 vs 50 - 60 = true
# 30 - 90 vs 50 - 60 = true
# 55 - 56 vs 50 - 60 = true
# 55 - 70 vs 50 - 60 = true

# 70 - 90 vs 50 - 60 = false

if user_to < test_item["from_"] or user_from > test_item["to"]:
	print("False")
else:
	print("True")


# if user_from >= test_item["from_"] and user_from <= test_item["to"] or user_to <= test_item["to"] and user_to >= test_item["from_"]:
# 	print("True")
# else:
# 	print("False")
