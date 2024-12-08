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
    """
        Day 3 of advent of code 2024: Mull it Over

        More info on the puzzle here: https://adventofcode.com/2024/day/3

        Some optimisations with some inspiration from mebeim too:
            https://github.com/mebeim/aoc/tree/master/2024#day-1---historian-hysteria
    """

    # regex to find valid multiplications
    regex_part1 = r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\)|don't\(\))"

    # code here
    part1 = 0
    part2 = 0

    logger = logging_setup()

    with open("inputs/day3.txt", 'r') as f:
        text = f.read()
        # results =

        # multiplication is switched on by default
        is_active = True

        # process results
        for no1, no2, do_dont in re.findall(regex_part1, text):
            if do_dont:
                is_active = False if do_dont=="don't()" else True
            else:
                # get the result
                mul_result = int(no1) * int(no2)

                if is_active:
                    # only record the second result if multiplication enabled
                    part2 += mul_result

                part1 += mul_result

        print(f"Part 1: {part1}; Part2: {part2}")

if __name__ == '__main__':
    main()
