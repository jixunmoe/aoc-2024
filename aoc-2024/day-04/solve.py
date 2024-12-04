import argparse
import re
from enum import Enum
from itertools import islice
from typing import List, Generator


class SearchDirection(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    DIAGONAL = 2  # ↘
    DIAGONAL_REVERSE = 3  # ↙


class WordSearch:
    verbose: bool
    grid: List[List[str]]
    width: int
    height: int

    def __init__(self, puzzle: str, verbose=False):
        lines = puzzle.strip().splitlines(keepends=False)
        self.verbose = verbose
        self.grid = [list(line) for line in lines]
        self.width = len(self.grid[0])
        self.height = len(self.grid)

        for row in self.grid:
            assert len(row) == self.width, "All rows must have the same length"

    def get_word(self, pos: tuple[int, int], direction: SearchDirection) -> Generator[str, None, None]:
        (x, y) = pos
        match direction:
            case SearchDirection.HORIZONTAL:
                while x < self.width:
                    yield self.grid[y][x]
                    x += 1
            case SearchDirection.VERTICAL:
                while y < self.height:
                    yield self.grid[y][x]
                    y += 1
            case SearchDirection.DIAGONAL:
                while x < self.width and y < self.height:
                    yield self.grid[y][x]
                    x += 1
                    y += 1
            case SearchDirection.DIAGONAL_REVERSE:
                while x >= 0 and y < self.height:
                    yield self.grid[y][x]
                    x -= 1
                    y += 1

    def is_match(self, word: str, pos: tuple[int, int], direction: SearchDirection) -> bool:
        n = len(word)
        return ''.join(islice(self.get_word(pos, direction), n)) == word

    def search_all(self, word: str):
        result = 0
        for x in range(self.width):
            for y in range(self.height):
                for term in (word, word[::-1]):
                    for direction in SearchDirection:
                        if self.is_match(term, (x, y), direction):
                            if self.verbose:
                                print(f'{term} found at pos=({x}, {y}), dir={direction}')
                            result += 1
        return result

    def is_x_mas(self, x, y):
        if self.grid[y][x] != 'A':
            return False

        a = self.grid[y - 1][x - 1] + self.grid[y + 1][x + 1]
        b = self.grid[y - 1][x + 1] + self.grid[y + 1][x - 1]

        valid = ('MS', 'SM')
        return a in valid and b in valid

    def search_x_mas(self) -> int:
        result = 0
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if self.is_x_mas(x, y):
                    if self.verbose:
                        print(f'X-MAS found at pos=({x}, {y})')
                    result += 1
        return result


def part1(input_text: str, verbose: bool):
    ws = WordSearch(input_text, verbose)
    return ws.search_all('XMAS')


def part2(input_text: str, verbose: bool):
    ws = WordSearch(input_text, verbose)
    return ws.search_x_mas()


def solve(input_file: str, verbose: bool):
    with open(input_file, "r", encoding='utf-8') as file:
        input_text = file.read().strip()

    part1_result = part1(input_text, verbose)
    print(f"part1: {part1_result}")
    part2_result = part2(input_text, verbose)
    print(f"part2: {part2_result}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    solve(args.input, args.verbose)


if __name__ == "__main__":
    main()
