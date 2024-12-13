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


def main():
    """
        Day [x] of advent of code 2024: [title]

        More info on the puzzle here: https://adventofcode.com/2024/day/[x]

    """
    day = 0 # enter day here
    use_sample = True

    part1 = 0
    part2 = 0

    logger = logging_setup()

    with open(f"inputs/day{day}{'-sample' if use_sample else ''}.txt", 'r') as f:
        pass

    print(f"part 1: {part1}, part 2: {part2}")

if __name__ == '__main__':
    main()
