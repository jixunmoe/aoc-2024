import argparse
from collections import Counter
from itertools import chain, combinations
import re


class Garden:
    def __init__(self, input_text: str):
        self.grid = [list(map(ord, x)) for x in input_text.splitlines()]
        self.size = len(self.grid[0]), len(self.grid)

    def get_with_delta(self, pos, delta):
        x, y = pos
        dx, dy = delta
        x += dx
        y += dy

        w, h = self.size
        if x < 0 or x >= w or y < 0 or y >= h:
            return None, None
        return (x, y), self.grid[y][x]


class GardenExplorer:
    garden: Garden

    def __init__(self, garden: Garden):
        self.garden = garden

        w, h = garden.size

        self.visited = [[False] * w for _ in range(h)]

    def find_regions(self):
        w, h = self.garden.size
        for y in range(h):
            for x in range(w):
                if self.visited[y][x]:
                    continue
                yield self.explore_region((x, y))

    def explore_region(self, pos: tuple[int, int]):
        x, y = pos
        w, h = self.garden.size
        value = self.garden.grid[y][x]

        self.visited[y][x] = True
        pos_to_explore = {pos}

        area = 1
        perimeter = 4

        all_visited = {pos}
        vertical_lines = [[0] * (w + 1) for _ in range(h + 1)]
        horizontal_lines = [[0] * (w + 1) for _ in range(h + 1)]

        vertical_lines[x][y] = 1
        vertical_lines[x + 1][y] = 1
        horizontal_lines[y][x] = 1
        horizontal_lines[y + 1][x] = 1

        while len(pos_to_explore) > 0:
            next_pos_set = set()
            for p in pos_to_explore:
                for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    next_pos, next_value = self.garden.get_with_delta(p, direction)
                    # invalid cord or not matching
                    if next_value != value:
                        continue
                    x, y = next_pos
                    if self.visited[y][x]:
                        perimeter -= 1
                        continue
                    # not visited
                    self.visited[y][x] = True
                    next_pos_set.add(next_pos)
                    all_visited.add(next_pos)
                    perimeter += 3
                    area += 1

                    vertical_lines[x][y] += 1
                    vertical_lines[x + 1][y] += 1

                    horizontal_lines[y][x] += 1
                    horizontal_lines[y + 1][x] += 1
            pos_to_explore = next_pos_set

        # Transpose vertical lines
        # vertical_lines_t = [[vertical_lines[x][y] for x in range(w + 1)] for y in range(w + 1)]
        vertical_lines_t = vertical_lines
        temp = '\n'.join([''.join(map(str, row)) for row in chain.from_iterable([vertical_lines_t, horizontal_lines])])
        sides = len(list(re.findall(r'1+', temp)))  # greedy match

        for ((x1, y1), (x2, y2)) in combinations(all_visited, 2):
            dx = x2 - x1
            dy = y2 - y1

            if dx * dx + dy * dy == 2:
                p1 = (x1 + dx, y1)
                p2 = (x1, y1 + dy)

                if p1 not in all_visited and p2 not in all_visited:
                    sides += 2

        # for y in range(h - 1):
        #     for x in range(w - 1):
        #         a, b, c, d = map(lambda p: p in all_visited, ((y, x), (y, x + 1), (y + 1, x), (y + 1, x + 1)))
        #         if (a, b, c, d) in ((False, True, True, False), (True, False, False, True)):
        #             print(f"Checking: {(x, y)}: {a} {b} {c} {d}")
        #             sides += 2
        #             continue

        return value, area, perimeter, sides


def solve(input_path, verbose):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip()

    garden = Garden(input_text)
    p1 = 0
    p2 = 0
    for (value, a, p, s) in GardenExplorer(garden).find_regions():
        verbose and print(f"Region {chr(value)}: area={a}, perimeter={p}, sides={s}")
        p1 += a * p
        p2 += a * s
    print(f'p1: {p1}')
    print(f'p2: {p2}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    # parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    solve(args.input, args.verbose)


if __name__ == "__main__":
    main()
