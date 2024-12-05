safe_count = 0

def negative(n):
    return 1 if n >= 0 else - 1

with open("inputs/day2.txt", 'r') as f:
    for line in f:
        levels = [int(level) for level in line.split()]

        multiplier = None
        safe = True

        for x in range(1, len(levels)):
            distance = levels[x] - levels[x-1]

            if multiplier is None:
                multiplier = negative(distance)
            else:
                if multiplier != negative(distance):
                    safe = False
                    break

            if distance * multiplier < 1 or distance * multiplier > 3:
                safe = False
                break

        if safe:
            safe_count += 1

    print (safe_count)

