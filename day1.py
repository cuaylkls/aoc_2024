import re

# initilise lists and return vars
loc1 = []
loc2 = []
result = 0

with open("inputs/day1.txt") as f:
    lines = f.readlines()

    for line in lines:
        # read list items
        locations = re.split(r"\s+", line.strip())
        loc1.append(int(locations[0]))
        loc2.append(int(locations[1]))

# sort both lists
loc1.sort()
loc2.sort()

for x in range(len(loc1)):
    # find the maximum and minimum locations
    no1 = max(loc1[x], loc2[x])
    no2 = min(loc1[x], loc2[x])

    # find the difference between the locations
    result += no1 - no2

print(f"Part 1: {result}")




