import argparse
from collections import defaultdict
from typing import Generator
from itertools import chain

# down, right, up, left
MOVEMENTS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class Board:
    data: list[list[int]] = []
    size: tuple[int, int]
    verbose: bool

    def __init__(self, board_map: str, verbose: bool):
        self.verbose = verbose
        self.data = []
        for line in board_map.splitlines():
            self.data.append(list(map(int, line.strip())))

        width = len(self.data[0])
        height = len(self.data)
        self.size = width, height

    def in_bound(self, x: int, y: int):
        width, height = self.size
        return 0 <= x < width and 0 <= y < height

    def find_surrounding_node(self, pos: tuple[int, int], target: int) -> Generator[tuple[int, int], None, None]:
        for movement in MOVEMENTS:
            x, y = pos
            dx, dy = movement
            x += dx
            y += dy
            if self.in_bound(x, y) and self.data[y][x] == target:
                yield x, y

    def solve(self, dedup: bool):
        w, h = self.size

        cache = defaultdict(list)
        for y in range(h):
            for x in range(w):
                key = self.data[y][x]
                cache[key].append((x, y))

        heads = cache[0]
        total_trails = 0
        container = set if dedup else list
        for head in heads:
            trails: set[tuple[int, int]] | list[tuple[int, int]] = container([head])
            self.verbose and print(f'trails={trails}', end='')

            # Search for 1, 2, ..., 9
            for i in range(1, 10):
                trails = container(chain.from_iterable([self.find_surrounding_node(t, i) for t in trails]))
                self.verbose and print(f' > {i}{trails}', end='')
            self.verbose and print('')
            total_trails += len(trails)
        return total_trails


def solve(input_path, verbose):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip()

    board = Board(input_text, verbose)

    p1 = board.solve(dedup=True)
    verbose and print('-*' * 20 + '-')
    p2 = board.solve(dedup=False)

    print(f'p1 = {p1}')
    print(f'p2 = {p2}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    # parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    solve(args.input, args.verbose)


if __name__ == "__main__":
    main()
