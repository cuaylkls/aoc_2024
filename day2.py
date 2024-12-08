import logging

def logging_setup():
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

    return logger


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


def is_level_report_safe(levels, with_tolerance=False):
    def tolerance_check(tmp_levels):
        tmp_direction = None

        for j in range(len(tmp_levels) - 1):
            tmp_result, tmp_direction = check_pair(tmp_levels[j], tmp_levels[j + 1], tmp_direction)

            if not tmp_result:
                return False

        return True

    direction = None
    total_levels = len(levels)

    x = 0

    while x < total_levels -1:
        result, direction = check_pair(levels[x], levels[x + 1], direction)

        if not result:
            if not with_tolerance:
                return False

            # remove no 1
            alt_levels = levels[:x] + levels[x+1:]

            if tolerance_check(alt_levels):
                return True

            # remove no 2
            alt_levels = levels[:x+1] + levels[x+2:]

            if  tolerance_check(alt_levels):
                return True

            # if we are on the second pair, try removing the first no as
            # this may fix it
            if x == 1:
                alt_levels = levels[x:]

                if tolerance_check(alt_levels):
                    return True

            return False


        x+= 1

    return True

def main():
    part1 = 0
    part2 = 0

    logger = logging_setup()

    with open("inputs/day2.txt", 'r') as f:
        for line in f:
            levels = [int(level) for level in line.split()]

            result1 = is_level_report_safe(levels)
            result2 = is_level_report_safe(levels,  True)

            if result1:
                part1 += 1

            if result2:
                part2 += 1


        print (f"part 1: {part1}, part 2: {part2}")


if __name__ == '__main__':
    main()
