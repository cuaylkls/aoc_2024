import logging


def logging_setup(level=logging.DEBUG):
    # Create and configure the logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Add a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger


def return_middle_value(list):
    return list[len(list) // 2]


def main():
    """
        Day 5 of advent of code 2024: Print Queue

        More info on the puzzle here: https://adventofcode.com/2024/day/5

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

    logger.debug(rules)
    logger.debug(updates)

    for update in updates:
        original_update = update.copy()

        valid = True

        x = 0
        while x < len(update):
            # get the ruleset for this number
            if not update[x] in rules:
                x += 1
                continue

            rule_set = rules[update[x]]

            #  preceding updates
            preceding_updates = update[:x]

            for rule in rule_set:
                # the page number appears in a preceding update,
                # it is not valid
                if rule in preceding_updates:
                    valid = False
                    logger.debug(f"Update not valid: {update}; {update[x]}|{rule}")

                    # find where in the list the rule is
                    y = 0
                    while y < len(preceding_updates):
                        if preceding_updates[y] == rule:
                            break

                        y += 1

                    # create a new list and move the pointer back to the position other number moved to
                    update = preceding_updates[:y] + [update[x], rule] +  preceding_updates[y+1:] + update[x+1:]
                    x = y

                    break
            else:
                x += 1
        else:
            logger.debug(f"Update valid: {update}")

            # add the middle number in the valid update to part1
            if valid: # this is a part 1 list
                part1 += return_middle_value(original_update)
            else:
                # part two list, so use the new onw
                part2 += return_middle_value(update)

    print(f"part 1: {part1}, part 2: {part2}")

if __name__ == '__main__':
    main()
