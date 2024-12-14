import argparse
import math
import operator
import re
from functools import reduce

import numpy as np


def add_mod(a, b, m):
    return (a + b) % m


class Grid:
    w: int
    h: int
    mid_w: int
    mid_h: int

    def __init__(self, size: tuple[int, int]):
        w, h = size
        self.w, self.h = w, h
        self.mid_w, self.mid_h = math.floor(w / 2), math.floor(h / 2)

    def get_board(self, bots: list['Robot']):
        grid = [[0] * self.w for _ in range(self.h)]
        for bot in bots:
            grid[bot.y][bot.x] += 1

        return '\n'.join([''.join([np.base_repr(x, 36) if x else '.' for x in row]) for row in grid])

    def get_christmas_tree(self, bots: list['Robot']):
        grid = [[' '] * self.w for _ in range(self.h)]
        for bot in bots:
            grid[bot.y][bot.x] = '.'

        return '\n'.join([''.join(row) for row in grid])

    @staticmethod
    def all_unique(bots: list['Robot']):
        return len(set(map(lambda b: (b.x, b.y), bots))) == len(bots)

    def split_quad(self, bots: list['Robot']):
        result = [0] * 4
        for bot in bots:
            if bot.x == self.mid_w or bot.y == self.mid_h:
                continue # in the mid

            is_left = int(bot.x < self.mid_w)
            is_top = int(bot.y < self.mid_h)
            result[(is_left << 1) + is_top] += 1
        return result

class Robot:
    grid: Grid
    x: int
    y: int
    vx: int
    vy: int

    def __init__(self, grid: Grid, position: tuple[int, int], velocity: tuple[int, int]):
        x, y = position
        vx, vy = velocity
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.grid = grid

    def move(self):
        self.x = add_mod(self.x, self.vx, self.grid.w)
        self.y = add_mod(self.y, self.vy, self.grid.h)


def parse(text: str, grid: Grid):
    result = []
    for m in re.finditer(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', text):
        # position, velocity
        p = int(m.group(1)), int(m.group(2))
        v = int(m.group(3)), int(m.group(4))
        result.append(Robot(grid, p, v))
    return result


def solve(input_path, verbose, grid_size):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip()


    grid = Grid(grid_size)
    robots = parse(input_text, grid)

    for i in range(100):
        for bot in robots:
            bot.move()
        if grid.all_unique(robots):
            print(f'p2: {i} (early result)')

    verbose and print(grid.get_board(robots))
    bot_quads = grid.split_quad(robots)
    verbose and print(bot_quads)
    p1 = reduce(operator.mul, bot_quads, 1)
    print(f'p1: {p1}')


    p2 = 100
    while True:
        p2 += 1
        for bot in robots:
            bot.move()
        if grid.all_unique(robots):
            verbose and print(f'----- i: {p2} -----')
            verbose and print(grid.get_christmas_tree(robots))
            break
    print(f'p2: {p2}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-W", "--width", type=int, default=11)
    parser.add_argument("-H", "--height", type=int, default=7)
    # parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    solve(args.input, args.verbose, (args.width, args.height))


if __name__ == "__main__":
    main()
