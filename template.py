import logging
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


def main():
    """
        Day [x] of advent of code 2024: [title]

        More info on the puzzle here: https://adventofcode.com/2024/day/[x]

    """
    day = 0 # enter day here
    use_sample = True

    part1 = 0
    part2 = 0

    logger = SingleLogging.logging_setup()

    with open(f"inputs/day{day}{'-sample' if use_sample else ''}.txt", 'r') as f:
        pass

    print(f"part 1: {part1}, part 2: {part2}")

if __name__ == '__main__':
    main()
