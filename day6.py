import logging
from enum import Enum
from typing import Set, Tuple


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

class InvalidGuardPositionError(Exception):
    pass

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class PatrolGrid:
    @property
    def obstacles(self) -> Set[Tuple[int, int]]:
        return self._obstacles

    @property
    def guard_position(self) -> Tuple[int, int]:
        return self._guard_position

    def is_obstacle(self, position: Tuple[int, int]) -> bool:
        return position in self._obstacles

    def valid_position(self, position: Tuple[int ,int]) -> bool:
        x,y = position

        return (0 <= x <= self._x_max) and (0 <= y <= self._x_max)

    def __init__(self, grid_file: str):
        self._obstacles: Set[Tuple[int, int]] = set()
        self._direction = Direction.UP
        self._guard_position = (-1, -1)
        self._x_max : int = -1

        with open(grid_file, 'r') as f:
            y_pos = 0
            guard_pos = None

            for line in f:
                if y_pos == 0:
                    self._x_max = len(line.strip()) - 1
                self._find_obstacles(line, y_pos)

                # check if the guard is at this position
                if guard_pos is None:
                    pos = line.find("^")

                    if pos != -1:
                        self._guard_position = (pos, y_pos)

                y_pos += 1

        self._y_max = y_pos - 1

    def _find_obstacles(self, grid_line: str, y_pos: int) -> None:
        pos = grid_line.find('#')

        while pos != -1:
            self._obstacles.add((pos, y_pos))
            pos = grid_line.find("#", pos + 1)

class GuardPatrol:
    @property
    def all_positions(self) -> Set[Tuple[int, int]]:
        return self._all_positions

    def __init__(self, patrol_gird: PatrolGrid, initial_position: Tuple[int, int], direction = Direction.UP):
        self._patrol_grid = patrol_gird
        self._direction = direction
        self._current_position = initial_position
        self._all_positions : Set[Tuple[int, int]] = {initial_position}

    def turn_right_90(self) -> None:
        mapping = {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP
        }

        self._direction = mapping[self._direction]

    @staticmethod
    def translate_pos(pos: Tuple[int, int], offset: Tuple[int, int]) -> Tuple[int, int]:
        """
            Translates the position using an offset

        :param pos: x,y co-ordinates of the initial position
        :param offset: x,y offset to adjust the position by
        :return: translated x,y co-ordinates
        """
        return pos[0] + offset[0], pos[1] + offset[1]

    def move_to_next_pos(self) -> bool:
        new_pos = self.translate_pos(self._current_position, self._direction.value)

        if self._patrol_grid.is_obstacle(new_pos):
            # check if this is next to an obstruction
            # if it is, turn right 90o and move in that direction
            self.turn_right_90()
            new_pos = self.translate_pos(self._current_position, self._direction.value)

        # check the co-ordinates of the new position are on the grid
        if self._patrol_grid.valid_position(new_pos):
            self._current_position = new_pos
            self._all_positions.add(new_pos)

            return True
        else:
            # we are at the end of the grid, so cannot move
            return False

    def walk(self):
        while self.move_to_next_pos():
            pass


def main():
    """
        Day 6 of advent of code 2024: Guard Gallivant

        More info on the puzzle here: https://adventofcode.com/2024/day/6

    """
    day = 6  # enter day here
    use_sample = False

    part1 = 0
    part2 = 0

    logger = logging_setup()

    grid = PatrolGrid(f"inputs/day{day}{'-sample' if use_sample else ''}.txt")
    guard = GuardPatrol(grid, grid.guard_position)

    # walk the guard
    guard.walk()

    logger.debug(grid.obstacles)
    logger.debug(grid.guard_position)
    logger.debug(guard.all_positions)

    part1 = len(guard.all_positions)

    print(f"part 1: {part1}, part 2: {part2}")


if __name__ == '__main__':
    main()
