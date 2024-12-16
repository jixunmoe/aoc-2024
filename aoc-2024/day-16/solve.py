import argparse
from typing import Any

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


class MazePath:
    x: int
    y: int
    direction: int
    grid: MazeGrid
    events: list[int]
    cost: int
    locations: list[tuple[int, int]]
    turns: int

    def __init__(self, grid: MazeGrid, x=0, y=0, direction=DIR_E, events=None, cost=0, locations=None, turns=0):
        self.direction = direction
        self.grid = grid
        self.x = x
        self.y = y
        self.events = [] if events is None else events.copy()
        self.locations = [(x, y)] if locations is None else locations.copy()
        self.cost = cost
        self.turns = turns

    def add_event(self, event: int):
        self.events.append(event)
        self.cost += POINT_MAPPING[event]
        if event != MOVE_FORWARD:
            self.turns += 1

    def clone(self):
        return MazePath(self.grid, self.x, self.y, self.direction, self.events, self.cost, self.locations, self.turns)

    def get_cost(self):
        return self.cost

    def at_goal(self):
        return (self.x, self.y) == self.grid.end

    def explore_move(self):
        for (next_dir, (dx, dy)) in enumerate(DELTAS):
            x, y = self.x + dx, self.y + dy
            if self.grid.grid[x, y] == WALL or (x, y) in self.locations:
                continue

            # Try to explore this direction
            p = self.clone()
            turned = p.direction != next_dir
            if turned:
                dir_delta = (next_dir - p.direction) % 4
                if dir_delta == 2:
                    p.add_event(EVT_TURN_RIGHT)
                    p.add_event(EVT_TURN_RIGHT)
                elif dir_delta == 1:
                    p.add_event(EVT_TURN_RIGHT)
                else:
                    p.add_event(EVT_TURN_LEFT)
                p.direction = next_dir
            p.add_event(MOVE_FORWARD)
            p.locations.append((x, y))
            p.x = x
            p.y = y
            yield p, turned


def solve_maze(grid: MazeGrid):
    xs, ys = grid.start
    w, h = grid.size

    max_cost = 200000
    cost_map: ndarray[tuple[int, int], dtype[np.int64]] = np.zeros((w, h), dtype=np.int64)
    cost_map.fill(max_cost)

    min_goal_cost = max_cost
    goal_paths = []
    goal_found = False
    paths = [MazePath(grid, xs, ys, DIR_E)]
    while len(paths) > 0:
        new_paths = []
        for path in paths:
            for p, turned in path.explore_move():
                x, y = p.x, p.y
                real_cost = p.turns
                # if real_cost <= cost_map[x, y]:
                if real_cost - cost_map[x, y] <= (0 if turned else 1):
                # if real_cost - cost_map[x, y] <= 1:
                    cost_map[x, y] = min(cost_map[x, y], real_cost)
                    if p.at_goal():
                        min_goal_cost = min(min_goal_cost, p.cost)
                        goal_paths.append(p)
                        if not goal_found:
                            print(f'goal path found with initial cost: {p.cost}')
                        goal_found = True
                    else:
                        new_paths.append(p)
        if goal_found:
            paths = [p for p in new_paths if p.cost <= min_goal_cost]
        else:
            paths = new_paths

    return list(filter(lambda pp: pp.cost == min_goal_cost, goal_paths))


def solve(input_path, verbose, grid_size):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '')
    maze = MazeGrid(input_text)
    # print(maze.grid)
    goal_paths = solve_maze(maze)
    assert len(goal_paths) > 0, "No solution found"

    print(f'p1: {goal_paths[0].get_cost()}')

    total_loc = {maze.start, maze.end}
    for p in goal_paths:
        # print(f'l: {len(p.locations)} / t={p.turns}')
        total_loc = total_loc.union(p.locations)
    print(f'p2: {len(total_loc)}')

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
