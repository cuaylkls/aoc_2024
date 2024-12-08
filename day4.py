import logging
from typing import List, Tuple
from enum import Enum

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


class Direction(Enum):
    """
    Directional transformations for the grid
    """
    U = (0, -1)
    UR = (1, -1)
    UL = (-1, -1)
    D = (0, 1)
    DR = (1, 1)
    DL = (-1, 1)
    L = (-1, 0)
    R = (1, 0)

class WordSearch:
    """
    WordSearch helper class
    """

    def __init__(self, grid: List[str]):
        self._grid = grid
        self._width = len(grid[0])
        self._height = len(grid)

    def read_grid(self, start_pos: Tuple[int, int], direction: Direction, total_chars: int) -> str:
        """
            Read characters from a start position in a specified direction.

            Returns:
                str: string of the characters read

            Args:
                start_pos: starting position to read from
                direction: the direction to read in
                total_chars: total number of characters to read
        """
        ret = self.get_grid_ref(start_pos)
        total_chars -= 1

        # get the new position based on the direction transformation
        new_pos = self.translate_position(start_pos, direction)

        while self.position_is_valid(new_pos) and total_chars > 0:
            # read each character until the end of the grid is encountered or
            # total_chars is reached

            ret += self.get_grid_ref(new_pos)
            new_pos = self.translate_position(new_pos, direction)
            total_chars -= 1

        return ret

    def get_grid_ref(self, pos: Tuple[int, int]) -> str:
        """
            Gets a character from a specific grid position

            Args:
                pos: position in the grid to read the character from

            Returns:
                str: character at the specified position in the grid
        """
        return self._grid[pos[1]][pos[0]]


    def position_is_valid(self, pos: Tuple[int, int]) -> bool:
        """
            Checks is the given position is within the bounds of the grid

            Args:
                pos: position in the grid to check

            Returns:
                bool: True of the position is within the grid, False otherwise
        """
        return 0 <= pos[0] < self._width and 0 <= pos[1] < self._height

    def count_word_occurrences(self, word: str) -> int:
        """
            Counts the number of occurrences of a word

            The function checks for the word in all 8 directions

            Args:
                word: word to find in the grid

            Returns:
                int: Total occurrences of the word
        """
        count = 0
        word_length = len(word) # get word length

        # find all occurrences of the first letter of the word
        for x, y in self.find_char_occurrences(word[0]):
            # search in all directions for the word
            for direction in Direction:
                search = self.read_grid((x, y), direction, word_length)

                if search == word:
                    count += 1

        return count

    def find_char_occurrences(self, char, clip=0) -> Tuple[int, int]:
        """
            Find all occurrences of a character in the grid

            Args:
                char: character to find
                clip: clip all four sides of the grid by this amount

            Returns:
                The position of occurrence of the character
        """
        for y in range(clip, self._height - clip):
            for x in range(clip, self._width - clip):
                if  self.get_grid_ref((x, y)) == char:
                    yield x,y

    def traverse_grid(self, clip=0) -> Tuple[str, Tuple[int, int]]:
        """
            Return each character in the grid and it's position

            Args:
                clip: clip all four sides of the grid by this amount

            Returns:
                Each the character and its position in the grid
        """
        for y in range(clip, self._height - clip):
            for x in range(clip, self._width - clip):
                yield self.get_grid_ref((x, y)), (x,y)

    @staticmethod
    def translate_position(pos: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
        return pos[0] + direction.value[0], pos[1] + direction.value[1]

    @staticmethod
    def translate_position_offset(pos: Tuple[int, int], offset: Tuple[int, int]) -> Tuple[int, int]:
        return pos[0] + offset[0], pos[1] + offset[1]

def main():
    """
        Day 4 of advent of code 2024: [title]

        More info on the puzzle here: https://adventofcode.com/2024/day/4

    """

    # these are the position translations for part 2
    part2_directions = [
        (
            (Direction.DR, (-1, -1)), (Direction.DL, (1, -1))
        ),
        (
            (Direction.DR, (-1, -1)), (Direction.UR, (-1, 1))
        ),
        (
            (Direction.DR, (-1, -1)), (Direction.UL, (1, 1))
        ),
        (
            (Direction.UL, (1, 1)), (Direction.DL, (1, -1))
        ),
        (
            (Direction.UR, (-1, 1)), (Direction.UL, (1, 1))
        ),
    ]

    part2 = 0

    logger = logging_setup()
    grid_list = []

    # open file and read the grid
    with open("inputs/day4.txt", 'r') as f:
        for line in f:
            grid_list.append(line.strip())

    # load into the WordSearch helper
    word_search = WordSearch(grid_list)
    part1 = word_search.count_word_occurrences("XMAS")

    # for part 2 find all positions of the middle character 'A'
    for pos in word_search.find_char_occurrences('A', clip=1):
        logger.debug(f"Found A: {pos}")

        for searches in part2_directions:
            # search in all directions around the A
            for search in searches:
                search_start = word_search.translate_position_offset(pos, search[1])
                search_text = word_search.read_grid(search_start, search[0], 3)

                if search_text != "MAS":
                    break
            else:
                # when found, increment and continue to the next
                part2 += 1
                logger.debug(f"Found X-MAS: {pos}, {searches[0]}, {searches[1]}")

                # once found move to the next A
                break

    print(f"part 1: {part1}, part 2: {part2}")

if __name__ == '__main__':
    main()
