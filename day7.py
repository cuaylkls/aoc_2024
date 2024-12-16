import itertools
import logging
import time
from threading import Lock


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

def test_result(target, numbers, combinations):
    for combination in combinations:
        result = numbers[0]

        for x in range(len(combination)):
            operator = combination[x]

            if operator == "+":
                result += numbers[x + 1]
            elif operator == "*":
                result *= numbers[x + 1]
            elif operator == "|":
                result = int(str(result) + str(numbers[x+1]))

            if result > target:
                # stop checking if result is bigger than target
                break

        if result == target:
            return result

    return 0


def main():
    """
        Day [x] of advent of code 2024: [title]

        More info on the puzzle here: https://adventofcode.com/2024/day/[x]

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

            # generate all possible combinations
            combinations1 = get_combinations(len(numbers) - 1, "*+")
            combinations2 = get_combinations(len(numbers) - 1, "*+|")

            # logger.debug(f"{target}: {numbers}; trying {2 ** (len(numbers) - 1)} and {3 ** (len(numbers) - 1)} combinations")

            result1 = test_result(target, numbers, combinations1)

            if result1 == 0:
                result2 = test_result(target, numbers, combinations2)
            else:
                result2 = result1

            part1 += result1
            part2+= result2

            # logger.debug(f"result {result1}, {result2}")


    print(f"part 1: {part1}, part 2: {part2}")

    # Record the end time
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time = end_time - start_time

    # Output the time taken
    logger.info(f"Time taken: {elapsed_time:.2f} seconds")


if __name__ == '__main__':
    main()
