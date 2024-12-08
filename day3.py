import logging
import re


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
    # regex to find valid multiplications
    regex_part1 = r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\)|don't\(\))"

    # code here
    part1 = 0
    part2 = 0

    logger = logging_setup()

    with open("inputs/day3.txt", 'r') as f:
        text = f.read()
        results = re.findall(regex_part1, text)

        is_active = True

        # process results
        for result in results:
            if result[2] == "do()":
                is_active = True
                continue
            elif result[2] == "don't()":
                is_active = False
                continue

            mul_result = int(result[0]) * int(result[1])

            if is_active:
                part2 += mul_result

            part1 += mul_result

        print(f"Part 1: {part1}; Part2: {part2}")

if __name__ == '__main__':
    main()
