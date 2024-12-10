import logging
from http.cookiejar import debug


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


def main():
    """
        Day [x] of advent of code 2024: [title]

        More info on the puzzle here: https://adventofcode.com/2024/day/[x]

    """
    part1 = 0
    part2 = 0

    rules = {}
    updates = []
    parsing_rules = True

    logger = logging_setup()

    with open("inputs/day5.txt", 'r') as f:
        for line in f:
            if line.strip() == "":
                # next lines are updates
                parsing_rules = False
                continue

            if parsing_rules:
                parts = line.strip().split("|")
                parts_tuple = (int(parts[0]), int(parts[1]))

                if parts_tuple[0] in rules:
                    rules[parts_tuple[0]].append(parts_tuple[1])
                else:
                    rules[parts_tuple[0]] = [parts_tuple[1], ]
            else:
                updates_str = line.strip().split(",")

                updates.append([int(update) for update in updates_str])

    #rules.sort()

    logger.debug(rules)
    logger.debug(updates)

    for update in updates:
        valid = True

        for x in range(len(update)):
            # get the ruleset for this number
            if not update[x] in rules:
                continue

            rule_set = rules[update[x]]

            #  preceding updates
            preceding_updates = update[:x]

            for rule in rule_set:
                # the page number appears in a preceding update,
                # it is not valid
                if rule in preceding_updates:
                    valid = False
                    logger.debug(f"Update not valid: {update}")
                    break

            if not valid:
                break
        else:
            logger.debug(f"Update valid: {update}")

            # add the middle number in the valid update to part1
            part1 += update[int(len(update)/2)]

    print(f"part 1: {part1}, part 2: {part2}")

if __name__ == '__main__':
    main()
