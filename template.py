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


def main():
    # code here
    part1 = 0
    part2 = 0

    logger = logging_setup()

    with open("inputs/path_to_input.txt", 'r') as f:
        pass

    print(f"part 1: {part1}, part 2: {part2}")

if __name__ == '__main__':
    main()
