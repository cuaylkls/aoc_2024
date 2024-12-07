import logging
from netrc import netrc

# Create and configure the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Add a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)


def negative(n):
    return 1 if n >= 0 else - 1


def check_pair(n1, n2, direction):
    distance = n1 - n2

    if direction is None:
        direction = negative(distance)
    else:
        if direction != negative(distance):
            return False, direction

    if distance * direction < 1 or distance * direction > 3:
        return False, direction

    return True, direction


def is_level_report_safe_with_tolerance(levels):
    if is_level_report_safe(levels):
        return  True

    for x in range(0, len(levels)):
        if is_level_report_safe(levels[:x] + levels[x+1:]):
            return True

    return False


def is_level_report_safe(levels, tolerance = 0):
    direction = None
    total_levels = len(levels)

    x = 1

    while x < total_levels:
        result, direction = check_pair(levels[x], levels[x - 1], direction)

        if not result:
            tolerance -= 1

            check1 = levels[:x - 1] + levels[x:x + 3]
            check2 = levels[:x] + levels[x+1:x+3]
            passing_levels = None

            # remove 1st number and re-check
            if not is_level_report_safe(check1):
                # remove 2nd number and re-check
                if not is_level_report_safe(check2):
                    # if at the beginning of the list, try removing the first element
                    if x == 2:
                        check3 = levels[1:4]

                        if is_level_report_safe(check3):
                            passing_levels = check3
                else:
                    passing_levels = check2
            else:
                passing_levels = check1

            if passing_levels is not None:
                # reset the direction if not at end
                if len(check2) > 1:
                    _, direction = check_pair(passing_levels[1], passing_levels[0], None)
                x += 1 # skip the next number as already tested
            else:
                # reduce the tolerance again as there is a second failing pair
                tolerance -= 1

            if tolerance < 0:
                return False

        x+= 1

    return True

def main():
    part1 = 0
    part2 = 0
    part3 = 0

    with open("inputs/day2.txt", 'r') as f:
        for line in f:
            levels = [int(level) for level in line.split()]

            result1= is_level_report_safe(levels)
            result2 = is_level_report_safe_with_tolerance(levels)

            result3 = is_level_report_safe(levels, 1)

            if result1:
                part1 += 1

            if result2:
                part2 += 1

            if result3:
                part3 += 1

            if result2 != result3:
                logger.debug(levels)


        print (f"part 1: {part1}, part 2: {part2}, part 3: {part3}")


main()
