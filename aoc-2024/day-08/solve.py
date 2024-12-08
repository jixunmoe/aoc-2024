import argparse
import re
from itertools import product



class Game:
    freqs: dict[str, list[tuple[int, int]]]
    antinodes: set[tuple[int, int]]

    def __init__(self, board: str):
        self.board = board
        self.freqs = {}
        self.antinodes = set()
        lines = board.splitlines()
        for (y, line) in enumerate(lines):
            # freq: single lowercase letter, uppercase letter, or digit.
            for m in re.finditer(r"[a-zA-Z0-9#]", line):
                x = m.span()[0]
                freq = m.group(0)

                if freq == '#':
                    self.antinodes.add((x, y))
                else:
                    if freq not in self.freqs:
                        self.freqs[freq] = []
                    self.freqs[freq].append((x, y))
        self.size = (len(lines[0]), len(lines))

    def find_antinodes(self, is_part_2: bool = False):
        antinodes = self.antinodes.copy()
        for (key, freq) in self.freqs.items():
            for ((x1, y1), (x2, y2)) in product(freq, repeat=2):
                # ignore repeated node
                if x1 == x2 and y1 == y2:
                    continue

                dx = x2 - x1
                dy = y2 - y1
                # p2 + (dx, dy) => another point
                # p1 - (dx, dy) => another point
                self.add_antinodes(antinodes, (x1, y1), (-dx, -dy), is_part_2)
                self.add_antinodes(antinodes, (x2, y2), (dx, dy), is_part_2)
        return antinodes

    def __str__(self):
        return str(self.freqs)

    def __repr__(self):
        return str(self)

    def add_annotate(self, antinodes: set[tuple[int, int]], x: int, y: int):
        w, h = self.size
        if x < 0 or x >= w or y < 0 or y >= h:
            return False
        antinodes.add((x, y))
        return True

    def add_antinodes(self, antinodes: set[tuple[int, int]], point: tuple[int, int], delta: tuple[int, int],
                      is_part_2: bool):
        x, y = point
        dx, dy = delta

        # Add start point as well.
        if is_part_2:
            self.add_annotate(antinodes, x, y)

        while self.add_annotate(antinodes, x + dx, y + dy) and is_part_2:
            x += dx
            y += dy

    def merge_to_str(self, antinodes: set[tuple[int, int]]):
        w, h = self.size
        board = [['.'] * w for _ in range(h)]
        for (x, y) in antinodes:
            board[y][x] = '#'
        for freq, points in self.freqs.items():
            for (x, y) in points:
                board[y][x] = freq
        return '\n'.join(map(''.join, board))


def solve(input_path, verbose):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip()
    game = Game(input_text)

    p1 = game.find_antinodes()
    if verbose:
        print(game.merge_to_str(p1))
        print('-' * 80)
    print(f'part 1: {len(p1)}')

    p2 = game.find_antinodes(True)
    if verbose:
        print("")
        print(game.merge_to_str(p2))
        print('-' * 80)
    print(f'part 2: {len(p2)}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    # parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    solve(args.input, args.verbose)


if __name__ == "__main__":
    main()
