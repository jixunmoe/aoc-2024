import argparse
from os import cpu_count

BIT_UP = 1
BIT_RIGHT = 2
BIT_DOWN = 4
BIT_LEFT = 8

DIR_UP = ord('^')
DIR_DOWN = ord('v')
DIR_LEFT = ord('<')
DIR_RIGHT = ord('>')
WALL = ord('#')
EMPTY = ord('.')
EXIT = 0

DIR_TO_BITS = {
    DIR_UP: BIT_UP,
    DIR_RIGHT: BIT_RIGHT,
    DIR_DOWN: BIT_DOWN,
    DIR_LEFT: BIT_LEFT,
}

DIR_ROTATE = {
    BIT_UP: BIT_RIGHT,
    BIT_RIGHT: BIT_DOWN,
    BIT_DOWN: BIT_LEFT,
    BIT_LEFT: BIT_UP
}

dir_delta = {
    BIT_UP: (0, -1),
    BIT_DOWN: (0, 1),
    BIT_LEFT: (-1, 0),
    BIT_RIGHT: (1, 0)
}


def rotate_dir(direction: int):
    return DIR_ROTATE[direction]


class Game:
    verbose: bool
    board: list[list[int]]
    size: tuple[int, int]
    pos: tuple[int, int] = (-1, -1)
    direction = DIR_UP

    def __init__(self, puzzle: str, verbose: bool = False):
        self.verbose = verbose
        self.board = []

        for (y, line) in enumerate(puzzle.splitlines()):
            row = []
            for (x, c) in enumerate(map(ord, line.strip())):
                if c in (DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT):
                    self.pos = (x, y)
                    self.direction = DIR_TO_BITS[c]
                    row.append(EMPTY)
                else:
                    row.append(c)
            self.board.append(row)

        w = len(self.board[0])
        h = len(self.board)
        self.size = (w, h)

    def log(self, message: str):
        if self.verbose:
            print(message)

    def get_block(self, board: list[list[int]], pos: tuple[int, int]):
        x, y = pos
        w, h = self.size
        if x < 0 or y < 0 or x >= w or y >= h:
            return EXIT
        return board[y][x]

    def walk(self, board: list[list[int]], position: tuple[int, int], direction: int):
        if direction not in dir_delta:
            raise ValueError(f"Invalid direction: {direction}")

        w, h = self.size
        x, y = position
        dx, dy = dir_delta[direction]
        x += dx
        y += dy

        if x < 0 or y < 0 or x >= w or y >= h:
            return (x, y), EXIT
        return (x, y), board[y][x]

    def solve(self):
        exit_path = self.get_exit_path(self.board)
        if exit_path is None:
            raise ValueError("Game does not exit")

        x, y = self.pos
        exit_path[y][x] = 0

        p1 = 1  # include initial player position
        p2 = 0
        for (y, row) in enumerate(exit_path):
            for (x, visit) in enumerate(row):
                if visit == 0:
                    continue
                p1 += 1

                board_copy = [row.copy() for row in self.board]
                board_copy[y][x] = WALL
                if self.get_exit_path(board_copy) is None:
                    p2 += 1

        return p1, p2

    def get_exit_path(self, board: list[list[int]]):
        w, h = self.size
        pos = self.pos
        direction = self.direction
        visited = [[0] * w for _ in board]
        while True:
            (x, y), block = self.walk(board, pos, direction)

            if block == WALL:
                direction = rotate_dir(direction)
                x, y = pos  # reset position
            elif block == EXIT:
                return visited
            else:
                pos = (x, y)

            if visited[y][x] & direction != 0:
                return None
            visited[y][x] |= direction


def solve(input_file: str, verbose: bool):
    with open(input_file, "r", encoding='utf-8') as file:
        input_text = file.read().strip()

    game = Game(input_text, verbose)
    p1, p2 = game.solve()
    print(f"part1: {p1}")
    print(f"part2: {p2}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    solve(args.input, args.verbose)


if __name__ == "__main__":
    main()
