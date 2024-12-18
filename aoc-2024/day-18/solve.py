import argparse

import numpy as np
from numpy import ndarray, dtype

EMPTY = ord(' ')
WALL = ord('#')

class MazeGrid:
    start: tuple[int, int]
    end: tuple[int, int]
    size: tuple[int, int]
    walls: list[tuple[int, int]]

    def __init__(self, text: str, size: tuple[int, int]):
        self.size = size

        self.walls = []
        for line in text.splitlines():
            x, y = map(int, line.split(','))
            self.walls.append((x, y))

        self.start = (0, 0)
        self.end = (size[0] - 1, size[1] - 1)


def solve_maze(grid: MazeGrid, lines: int) -> int:
    previous: dict[tuple[int, int], list[tuple[int, int]]] = {}
    costs = {}
    w, h = grid.size

    walls = set(grid.walls[:lines])

    work: list[tuple[int, int, int]] = [(0, *grid.start)]
    while work:
        cost, cx, cy = work.pop(0)
        curr_node = cx, cy
        for x, y in ((cx + 1, cy), (cx, cy + 1,), (cx - 1, cy), (cx, cy - 1,)):
            if x < 0 or x >= w or y < 0 or y >= h:
                continue

            if (x, y) in walls:
                continue

            next_node: tuple[int, int] = (x, y)
            n_cost = cost + 1
            if next_node not in costs or n_cost < costs[next_node]:
                costs[next_node] = n_cost
                previous[next_node] = [curr_node]
                work.append((n_cost, x, y))
            elif n_cost == costs[next_node]:
                previous[next_node].append(curr_node)

    ex, ey = grid.end

    # Debug map
    # cost_board = np.zeros(grid.size, dtype=np.uint32)
    # cost_board.fill(999)
    # for ((x, y), cost) in costs.items():
    #     cost_board[x, y] = cost
    if (ex, ey) not in costs:
        return -1

    return costs[(ex, ey)]


def solve(input_path, verbose, lines, grid_size):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '')

    grid = MazeGrid(input_text, grid_size)
    steps = solve_maze(grid, lines)
    print(f"p1: {steps}")

    # p2 binary search
    left = 0
    right = len(grid.walls)
    mid: int = (left + right) // 2
    while left < right:
        mid = (left + right) // 2
        steps = solve_maze(grid, mid)
        if steps == -1:
            right = mid
        else:
            left = mid + 1

    for i in (mid - 1, mid, mid + 1):
        solved = solve_maze(grid, i)
        print(f'fall {i}: {solved} -> {grid.walls[i - 1]}')
    p2 = ','.join(map(str, grid.walls[mid]))
    print(f"p2: {p2}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-W", "--width", type=int, default=7)
    parser.add_argument("-H", "--height", type=int, default=7)
    parser.add_argument("-L", "--lines", type=int, default=12)
    # parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    solve(args.input, args.verbose, args.lines, (args.width, args.height))

    # solve real input:
    # -L 1024 -W 71 -H 71 input.txt


if __name__ == "__main__":
    main()
