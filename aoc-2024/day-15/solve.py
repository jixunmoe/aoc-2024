import argparse

UP = ord('^')
DOWN = ord('v')
LEFT = ord('<')
RIGHT = ord('>')

dir_mapping = {
    UP: (0, -1),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    RIGHT: (1, 0),
}

EMPTY = ord('.')
WALL = ord('#')
GOOD = ord('O')
GOOD_LEFT = ord('[')
GOOD_RIGHT = ord(']')
ROBOT = ord('@')

widen_map = {
    GOOD: (GOOD_LEFT, GOOD_RIGHT),
    WALL: (WALL, WALL),
    EMPTY: (EMPTY, EMPTY),
}


class Grid:
    data: list[list[int]]
    position: tuple[int, int] = (-1, -1)
    size: tuple[int, int] = (0, 0)
    verbose: bool = False

    def __init__(self, grid: str, wide=False, verbose=False):
        self.verbose = verbose
        self.data = []
        for y, row in enumerate(grid.split('\n')):
            grid_row: list[int] = []
            for x, cell in enumerate(map(ord, row)):
                if cell in (WALL, GOOD, EMPTY):
                    if wide:
                        grid_row.extend(widen_map[cell])
                    else:
                        grid_row.append(cell)
                elif cell == ROBOT:
                    self.position = x * (2 if wide else 1), y
                    grid_row.append(EMPTY)
                    wide and grid_row.append(EMPTY)
                elif cell in (GOOD_LEFT, GOOD_RIGHT):
                    grid_row.append(cell)
                else:
                    raise ValueError(f"Invalid cell: {chr(cell)}")
            self.data.append(grid_row)
        self.size = len(self.data[0]), len(self.data)

    def get_goods_at(self, x, y):
        cell = self.data[y][x]
        if cell == WALL:
            return False
        if cell == EMPTY:
            return [] # no more goods to find
        if cell == GOOD:
            return [(x, y)]
        if cell == GOOD_LEFT:
            return [(x, y), (x + 1, y)]
        if cell == GOOD_RIGHT:
            return [(x, y), (x - 1, y)]

    def move(self, direction: int):
        self.verbose and print(f'---------- Move   {chr(direction)}')

        x, y = self.position
        dx, dy = dir_mapping[direction]
        next_robot_pos = x + dx, y + dy

        discovered = set()
        layers = []
        search_nodes = {(x, y)}
        while len(search_nodes) > 0:
            next_search_nodes = set()
            layer = []
            for (x, y) in search_nodes:
                match self.get_goods_at(x + dx, y + dy):
                    case False:
                        return # found wall
                    case goods:
                        for good in goods:
                            if good not in discovered:
                                discovered.add(good)
                                layer.append(good)
                                next_search_nodes.add(good)
            layers.append(layer)
            search_nodes = next_search_nodes

        self.position = next_robot_pos
        for layer in reversed(layers):
            for (gx, gy) in sorted(layer, key=lambda p: p[0], reverse=dx > 0):
                nx, ny = gx + dx, gy + dy
                self.verbose and print(f'Good {gx, gy} -> {nx, ny}')
                self.data[gy][gx], self.data[ny][nx] = self.data[ny][nx], self.data[gy][gx]

    def find_goods_on_path(self, cache: set[tuple[int, int]], x, y, dx, dy):
        if (x, y) in cache:
            return

        cell = self.data[y][x]
        if cell == WALL:
            # raise ValueError("Can't walk due to wall on the way")
            yield False
            return

        if cell == EMPTY:
            return

        assert cell in (GOOD, GOOD_LEFT, GOOD_RIGHT), f"Invalid cell on path: {chr(cell)}"

        nx, ny = x + dx, y + dy
        # Good or moving left/right
        if cell == GOOD or dy == 0:
            yield x, y
            yield from self.find_goods_on_path(cache, nx, ny, dx, dy)
            return

        # Special case: good with left/right parts, and we are moving up/down
        adj_x_delta = 1 if cell == GOOD_LEFT else -1
        nnx = nx + adj_x_delta

        yield x, y
        yield nnx, y

        yield from self.find_goods_on_path(cache, nx, ny, dx, dy)

        if self.data[ny][nx] != cell:
            yield from self.find_goods_on_path(cache, nnx, ny, dx, dy)

    def try_to_move(self, x, y, dx, dy, callbacks: list[callable]):
        # Can we move this block?
        cell = self.data[y][x]
        if cell == WALL:
            return False
        if cell == EMPTY:
            return True

        assert cell in (GOOD, GOOD_LEFT, GOOD_RIGHT), f"Invalid cell on path: {chr(cell)}"

        def move_block():
            self.data[y + dy][x + dx], self.data[y][x] = self.data[y][x], self.data[y + dy][x + dx]

        if cell == GOOD or dy == 0:
            if self.try_to_move(x + dx, y + dy, dx, dy, callbacks):
                callbacks.append(move_block)
                return True
            return False

        # Special case: good with left/right parts, and we are moving up/down
        if self.try_to_move(x + (1 if cell == GOOD_LEFT else -1), y, dx, dy, callbacks):
            callbacks.append(move_block)
            return True
        return False

    @staticmethod
    def gps_to_score(x: int | float, y: int | float):
        return y * 100 + x

    def get_gps(self):
        w, h = self.size

        result = 0
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if cell == GOOD or cell == GOOD_LEFT:
                    result += self.gps_to_score(x, y)
                elif cell == GOOD_LEFT:
                    # result += self.gps_to_score(x=min(x, w - x - 2), y=min(y, h - y - 2))
                    pass

        return result

    def print(self):
        grid = [row.copy() for row in self.data]
        x, y = self.position
        grid[y][x] = ROBOT
        return '\n'.join([''.join(map(chr, row)) for row in grid])


def parse(grid: str, moves: str):
    return grid, [ord(c) for c in moves if c in '<>v^']


def solve(input_path, verbose):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '')

    grid_text, moves = parse(*input_text.split('\n\n', maxsplit=1))
#
#     gg = Grid('''
# ##########
# ##...[]...
# ##........
# '''.strip())
#     print(gg.print())
#     print(gg.get_gps())
#     return

    g = Grid(grid_text, wide=False, verbose=verbose)
    verbose and print(g.print())
    for m in moves:
        g.move(m)
        verbose and print(g.print())
    p1 = g.get_gps()
    print(g.print())
    print('-------------------')

    g = Grid(grid_text, wide=True, verbose=verbose)
    verbose and print(g.print())
    for m in moves:
        g.move(m)
        verbose and print(g.print())
    p2 = g.get_gps()
    print(g.print())

    print(f'p1: {p1}')
    print(f'p2: {p2}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    # parser.add_argument("-W", "--width", type=int, default=11)
    # parser.add_argument("-H", "--height", type=int, default=7)
    # parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    # , (args.width, args.height)
    solve(args.input, args.verbose)


if __name__ == "__main__":
    main()
