import re

# initilise lists and return vars
loc1 = []
loc2 = []
loc2_dict = {}

result = 0
similarity_score = 0

with open("inputs/day1.txt") as f:
    lines = f.readlines()

    for line in lines:
        # read list items
        locations = re.split(r"\s+", line.strip())

        loc1_number = int(locations[0])
        loc2_number = int(locations[1])
        loc1.append(loc1_number)
        loc2.append(loc2_number)

        # found a number in the first location which is not in the second
        # initilise the number in the dict
        if loc1_number not in loc2_dict:
            loc2_dict[loc1_number] = 0

        # found a number in the second location we haven't seen before,
        # add to the list and initilise with 1
        if loc2_number not in loc2_dict:
            loc2_dict[loc2_number] = 1
        else:
            loc2_dict[loc2_number] += 1

# sort both lists
loc1.sort()
loc2.sort()

for x in range(len(loc1)):
    # find the difference between the locations
    result += abs(loc1[x] - loc2[x])

   # calculate the similarity score for the number and add to the similarity score
    # variable
    similarity_score += loc1[x] * loc2_dict[loc1[x]]

print(f"Part 1: {result}")
print(f"Part 2: {similarity_score}")




