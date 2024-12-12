import argparse
from itertools import combinations

import numpy as np
from numpy import ndarray


def count_lines(data: ndarray[tuple[int, int], np.uint8]):
    found = 0
    for row in data:
        should_count = True
        for item in row:
            if should_count and item == 1:
                should_count = False
                found += 1
            elif item != 1:
                should_count = True
    return found


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
    visited: ndarray[tuple[int, int], np.uint8]
    garden: Garden

    def __init__(self, garden: Garden):
        self.garden = garden

        w, h = garden.size
        self.visited = np.zeros(shape=(w, h), dtype=np.uint8)

    def find_regions(self):
        w, h = self.garden.size
        for y in range(h):
            for x in range(w):
                if self.visited[y, x]:
                    continue
                yield self.explore_region((x, y))

    def explore_region(self, pos: tuple[int, int]):
        x, y = pos
        w, h = self.garden.size
        value = self.garden.grid[y][x]

        self.visited[y, x] = 1
        pos_to_explore = {pos}

        area = 1
        perimeter = 4

        visited_in_session = {pos}
        scan_line_shape = (w + 1, h + 1)
        vertical_lines: ndarray[tuple[int, int], np.uint8] = np.zeros(shape=scan_line_shape, dtype=np.uint8)
        horizontal_lines: ndarray[tuple[int, int], np.uint8] = np.zeros(shape=scan_line_shape, dtype=np.uint8)

        min_x, max_x = x, x
        min_y, max_y = y, y

        vertical_lines[x, y] = 1
        vertical_lines[x + 1, y] = 1
        horizontal_lines[x, y] = 1
        horizontal_lines[x, y + 1] = 1

        while len(pos_to_explore) > 0:
            next_pos_set = set()
            for p in pos_to_explore:
                for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    next_pos, next_value = self.garden.get_with_delta(p, direction)
                    # invalid cord or not matching
                    if next_value != value:
                        continue
                    x, y = next_pos
                    if self.visited[y, x]:
                        perimeter -= 1
                        continue
                    # not visited
                    self.visited[y, x] = True
                    next_pos_set.add(next_pos)
                    visited_in_session.add(next_pos)
                    perimeter += 3
                    area += 1

                    vertical_lines[x, y] += 1
                    vertical_lines[x + 1, y] += 1
                    horizontal_lines[x, y] += 1
                    horizontal_lines[x, y + 1] += 1
                    min_x, min_y = min(min_x, x), min(min_y, y)
                    max_x, max_y = max(max_x, x), max(max_y, y)
            pos_to_explore = next_pos_set

        max_x += 2
        max_y += 2

        nh = horizontal_lines[min_x:max_x, min_y:max_y].transpose()
        nv = vertical_lines[min_x:max_x, min_y:max_y]
        sides = count_lines(nh) + count_lines(nv)

        for ((x1, y1), (x2, y2)) in combinations(visited_in_session, 2):
            dx = x2 - x1
            dy = y2 - y1

            # Check if the distance between two points is sqrt(2)
            if dx * dx + dy * dy == 2:
                p1 = (x1 + dx, y1)
                p2 = (x1, y1 + dy)

                # They break!
                if p1 not in visited_in_session and p2 not in visited_in_session:
                    sides += 2

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
