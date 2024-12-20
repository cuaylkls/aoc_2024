import itertools
import logging
import time
from threading import Lock
from typing import List


class SingleLogging:
    logger = None
    _lock = Lock()

    @classmethod
    def logging_setup(cls, level=logging.DEBUG):
        if cls.logger is not None:
            return cls.logger

        with cls._lock:
            if cls.logger is not None:  # Double-check inside the lock
                return cls.logger

            # Create and configure the logger
            logger = logging.getLogger('SingleLogging_logger')  # Use a specific name
            logger.setLevel(level)

            # Check if handlers already exist
            if not logger.handlers:
                # Add a console handler
                console_handler = logging.StreamHandler()
                console_handler.setLevel(level)

                # Create a formatter and set it for the handler
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                console_handler.setFormatter(formatter)

                # Add the handler to the logger
                logger.addHandler(console_handler)

            cls.logger = logger

        return logger

def get_combinations(slots, options):
    return itertools.product(options, repeat=slots)

def evaluate(target: int, numbers: List[int], ops: List[str], index: int =0, current_result: int=0):
    """
    Evaluates operator combinations.

    Generated by GPT4o

    :param target: target number
    :param numbers: numbers for operator evaluation
    :param ops: operators to evaluate
    :param index: index to start at
    :param current_result: current computed results from earlier calculations
    :return: True if valid, false if not
    """
    if index == 0:
        current_result = numbers[0]

    if index == len(numbers) - 1:
        return current_result == target

    new_result = current_result

    for op in ops:
        if op == "+":
            new_result = current_result + numbers[index + 1]
        elif op == "*":
            new_result = current_result * numbers[index + 1]
        elif op == "|":
            new_result = int(str(current_result) + str(numbers[index + 1]))

        if new_result > target:
            continue  # Prune this branch
        if evaluate(target, numbers, ops, index + 1, new_result):
            return True

    return False

def main():
    """
        Day 7 of advent of code 2024: Bridge Repair

        More info on the puzzle here: https://adventofcode.com/2024/day/7

    """

    # Record the start time
    start_time = time.time()

    day = 7 # enter day here
    use_sample = False

    part1 = 0
    part2 = 0

    logger = SingleLogging.logging_setup()

    with open(f"inputs/day{day}{'-sample' if use_sample else ''}.txt", 'r') as f:
        logger.info("Start")

        for line in f:
            pos = line.find(":") # find the colon
            target = int(line[0:pos]) # get the target value

            # load the numbers
            numbers = [int(number) for number in line[pos+1:].strip().split()]

            result1 = target if evaluate(target, numbers, ["+", "*"]) else 0

            if result1 == 0:
                result2 = target if evaluate(target, numbers, ["+", "*", "|"]) else 0
            else:
                result2 = result1

            part1 += result1
            part2+= result2

    print(f"part 1: {part1}, part 2: {part2}")

    # Record the end time
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time = end_time - start_time

    # Output the time taken
    logger.info(f"Time taken: {elapsed_time:.2f} seconds")


if __name__ == '__main__':
    main()
