import argparse
from os import cpu_count
from multiprocessing.pool import Pool

from tqdm import tqdm

DIR_UP = ord('^')
DIR_DOWN = ord('v')
DIR_LEFT = ord('<')
DIR_RIGHT = ord('>')
WALL = ord('#')
EMPTY = ord('.')
EXIT = 0

VALID_CHARS = (DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT, WALL, EMPTY)
VALID_USER_CHARS = (DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT)

DIR_ROTATE = (DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT, DIR_UP)


def next_direction(direction: int):
    return DIR_ROTATE[DIR_ROTATE.index(direction) + 1]


dir_delta = {
    DIR_UP: (0, -1),
    DIR_DOWN: (0, 1),
    DIR_LEFT: (-1, 0),
    DIR_RIGHT: (1, 0)
}


class Game:
    verbose: bool
    board: list[list[int]]
    size: tuple[int, int]
    pos: tuple[int, int] = (-1, -1)
    direction = DIR_UP
    wall_count: int
    empty_count: int

    walls: list[tuple[int, int]]

    def __init__(self, puzzle: str, verbose: bool = False):
        self.verbose = verbose
        self.board = []
        self.walls = []

        for (y, line) in enumerate(puzzle.splitlines()):
            row = []
            for (x, c) in enumerate(map(ord, line.strip())):
                if c not in VALID_CHARS:
                    raise ValueError(f"Invalid character: {c}")

                if c in VALID_USER_CHARS:
                    self.pos = (x, y)
                    self.direction = c
                    c = EMPTY
                elif c == WALL:
                    self.walls.append((x, y))

                row.append(c)
            self.board.append(row)
        w = len(self.board[0])
        h = len(self.board)
        self.size = (w, h)
        self.wall_count = len(self.walls)
        self.empty_count = w * h - self.wall_count

    def log(self, message: str):
        if self.verbose:
            print(message)

    def part1(self):
        pass

    def get_block(self, board: list[list[int]], pos: tuple[int, int]):
        x, y = pos
        w, h = self.size
        if x < 0 or y < 0 or x >= w or y >= h:
            return EXIT
        return board[y][x]

    def walk(self, board: list[list[int]], position: tuple[int, int], direction: int):
        if direction not in dir_delta:
            raise ValueError(f"Invalid direction: {direction}")

        x, y = position
        dx, dy = dir_delta[direction]
        new_pos = (x + dx, y + dy)
        item = self.get_block(board, new_pos)
        if item == EMPTY:
            return new_pos, False
        return None, item == EXIT

    def solve_part1(self):
        exit_path = self.get_exit_path(self.board)
        if exit_path is None:
            raise ValueError("Game does not exit")

        visited_pos = {pos for (pos, _) in exit_path}
        if self.verbose:
            self.print_path(visited_pos)
        return len(visited_pos)

    def solve_part2(self):
        loop_option = 0
        valid_points = {point for (point, _) in self.get_exit_path(self.board)}
        for pos in tqdm(valid_points):
            loop_option += self.check_loop_at(pos)
        return loop_option

    def check_loop_at(self, pos: tuple[int, int]):
        if pos in self.walls or pos == self.pos:
            return 0

        x, y = pos
        board = [row.copy() for row in self.board]
        board[y][x] = WALL
        exit_path = self.get_exit_path(board)
        return 1 if exit_path is None else 0

    def solve_part2_multithread(self, threads: int = 4):
        valid_points = {point for (point, _) in self.get_exit_path(self.board)}
        loop_option = 0

        with Pool(threads) as pool:
            for result in tqdm(pool.imap_unordered(self.check_loop_at, valid_points), total=len(valid_points)):
                loop_option += result
        return loop_option

    def get_exit_path(self, board: list[list[int]]):
        pos = self.pos
        direction = self.direction
        visited = {(pos, direction)}
        while pos is not None:
            next_pos, exit_board = self.walk(board, pos, direction)
            in_loop = (next_pos, direction) in visited

            if next_pos is not None:
                visited.add((next_pos, direction))
                self.log(f'move to: {next_pos}')
                pos = next_pos
            else:
                direction = next_direction(direction)

            if in_loop:
                return None

            if exit_board:
                return visited

        return None

    def print_path(self, visited: set[tuple[int, int]]):
        for (y, row) in enumerate(self.board):
            for (x, c) in enumerate(row):
                if (x, y) in visited:
                    if (x, y) in self.walls:
                        raise ValueError("Visited wall")
                    print('X', end='')
                else:
                    print(chr(c), end='')
            print()

    def iterate_board_pos(self):
        w, h = self.size
        for y in range(h):
            for x in range(w):
                yield x, y


def part1(game: Game):
    return game.solve_part1()


def part2(game: Game, threads: int):
    match threads:
        case 0 | 1:
            return game.solve_part2()
        case _:
            return game.solve_part2_multithread(threads)


def solve(input_file: str, verbose: bool, threads: int):
    with open(input_file, "r", encoding='utf-8') as file:
        input_text = file.read().strip()

    part1_result = part1(Game(input_text, verbose))
    print(f"part1: {part1_result}")
    part2_result = part2(Game(input_text, verbose), threads)
    print(f"part2: {part2_result}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    solve(args.input, args.verbose, args.threads)


if __name__ == "__main__":
    main()
