import argparse

import numpy as np
from numpy import ndarray, dtype

WALL = 1
EMPTY = 0

DIR_N = 0
DIR_E = 1
DIR_S = 2
DIR_W = 3

MOVE_FORWARD = 4
EVT_TURN_LEFT = 8
EVT_TURN_RIGHT = 16
POINT_MAPPING = {
    MOVE_FORWARD: 1,
    EVT_TURN_LEFT: 1000,
    EVT_TURN_RIGHT: 1000
}

DELTAS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def dir_rotate_right(d: int):
    return (d + 1) % 4


def dir_rotate_left(d: int):
    return (d + 3) % 4


class MazeGrid:
    grid: ndarray[tuple[int, int], dtype[np.uint8]]
    start: tuple[int, int]
    end: tuple[int, int]
    size: tuple[int, int]

    def __init__(self, text: str):
        lines = text.splitlines()

        w = len(lines[0])
        h = len(lines)
        self.size = (w, h)

        board = np.zeros((w, h), dtype=np.uint8)
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    board[x, y] = 1
                elif c == '.':
                    board[x, y] = 0
                elif c == 'S':
                    self.start = (x, y)
                elif c == 'E':
                    self.end = (x, y)
        self.grid = board


def solve_maze(grid: MazeGrid):
    previous = {}
    costs = {}

    work = [(0, *grid.start, DIR_E)]
    while work:
        cost, cx, cy, direction = work.pop(0)
        node = cx, cy, direction
        dx, dy = DELTAS[direction]
        for x, y, n_dir, n_cost in (cx + dx, cy + dy, direction, cost + 1), \
                (cx, cy, dir_rotate_right(direction), cost + 1000), \
                (cx, cy, dir_rotate_left(direction), cost + 1000):
            if grid.grid[x, y] == WALL:
                continue

            key = (x, y, n_dir)
            if key not in costs or n_cost < costs[key]:
                costs[key] = n_cost
                previous[key] = [node]
                work.append((n_cost, x, y, n_dir))
            elif n_cost == costs[key]:
                previous[key].append(node)

    ex, ey = grid.end

    # Find a list of keys from costs that are at the end
    work = [k for k in [(ex, ey, d) for d in range(4)] if k in costs]
    min_cost = min(costs[k] for k in work)  # take minimum cost
    work = [k for k in work if costs[k] == min_cost]  # filter out non-optimal cost ones

    nodes = {grid.start, grid.end}
    while work:
        x, y, d = work.pop(0)
        key = (x, y, d)
        work.extend(previous[key])
        previous[key] = []  # Don't bother with this node again
        nodes = nodes.union({(x, y)})
    seats = len(nodes)
    return min_cost, seats


def solve(input_path, verbose, grid_size):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '')
    maze = MazeGrid(input_text)
    p1, p2 = solve_maze(maze)
    print("p1:", p1)
    print("p2:", p2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    # parser.add_argument("-W", "--width", type=int, default=11)
    # parser.add_argument("-H", "--height", type=int, default=7)
    # parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    # , (args.width, args.height)
    solve(args.input, args.verbose, None)


if __name__ == "__main__":
    main()
