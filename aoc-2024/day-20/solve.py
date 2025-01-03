import argparse

EMPTY = ord(' ')
WALL = ord('#')

type Grid = list[list[int]]
type Cord = tuple[int, int]  # x, y
type Size = tuple[int, int]  # width, height
type DijkstraCosts = dict[Cord, int]
type DijkstraNodes = dict[Cord, list[Cord]]


def parse_grid(input_text: str) -> tuple[Grid, Cord, Cord, Size]:
    grid = []
    start = (-1, -1)
    end = (-1, -1)
    for (y, line) in enumerate(input_text.split('\n')):
        row = []
        for (x, c) in enumerate(line):
            if c == '.':
                row.append(EMPTY)
            elif c == '#':
                row.append(WALL)
            elif c == 'S':
                row.append(EMPTY)
                start = (x, y)
            elif c == 'E':
                row.append(EMPTY)
                end = (x, y)
            else:
                raise ValueError(f"Invalid character {c}")
        grid.append(row)
    size = len(grid[0]), len(grid)
    return grid, start, end, size


def dijkstra(grid: Grid, start: Cord, /, size: Size = None) -> tuple[DijkstraNodes, DijkstraCosts]:
    previous: DijkstraNodes = {}
    costs: DijkstraCosts = {}
    w, h = size if size else (len(grid[0]), len(grid))

    work: list[tuple[int, int, int]] = [(0, *start)]
    costs[start] = 0

    while work:
        prev_cost, cx, cy = work.pop(0)
        prev_node = cx, cy
        for x, y in ((cx + 1, cy), (cx, cy + 1,), (cx - 1, cy), (cx, cy - 1,)):
            if not (0 <= x < w and 0 <= y < h):
                continue

            if grid[y][x] == WALL:
                continue

            cost = prev_cost + 1
            node: Cord = (x, y)

            if node not in costs or cost < costs[node]:
                costs[node] = cost
                previous[node] = [prev_node]
                work.append((cost, x, y))
            elif cost == costs[node]:
                previous[node].append(prev_node)

    return previous, costs


def iter_cross(n: int):
    """
    Only scan in this pattern (where x is)
    ...o...
    ..oop..
    .ooooo.
    oooCxxx
    .xxxxx.
    ..xxx..
    ...x...
    """

    # y is 0
    for x in range(1, n + 1):
        yield x, 0

    # Other cases:
    for y in range(1, n + 1):
        # when n = 3:
        # y  x
        # 1  [-2, 2]
        # 2  [-1, 1]
        # 3  [0]
        for x in range(y - n, n - y + 1):
            yield x, y


def calc_steps_saved(steps: int, cost_start: int, cost_end: int) -> int:
    """
    Always go from low cost point to high cost point
    """
    if cost_start > cost_end:
        return cost_start - (cost_end + steps)
    else:
        return cost_end - (cost_start + steps)


def solve_ex(grid: Grid, costs: DijkstraCosts, /, verbose: bool, threshold: int, time: int) -> int:
    print(f'solve for {time=} {threshold=}')
    good = 0

    search_window = set(iter_cross(time))
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == WALL: continue

            # Find 2 free space within the search window
            cost_start = costs[x, y]
            for (dx, dy) in search_window:
                if (cost_exit := costs.get((x + dx, y + dy), None)) is not None:
                    steps = abs(dx) + abs(dy)

                    # Check if we actually make some "good" savings
                    steps_saved = calc_steps_saved(steps, cost_start, cost_exit)
                    if steps_saved >= threshold:
                        good += 1

    return good


def solve(input_path, verbose, p2_threshold):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '')

    grid, start, end, size = parse_grid(input_text)
    _, costs = dijkstra(grid, start, size=size)
    assert end in costs, f"Can't reach end {end}"

    p1 = solve_ex(grid, costs, verbose=verbose, threshold=100, time=2)
    print(f'p1: {p1}')
    p2 = solve_ex(grid, costs, verbose=verbose, threshold=p2_threshold, time=20)
    print(f'p2: {p2}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--threshold", type=int, default=50, help="Threshold (p2)")
    args = parser.parse_args()
    solve(args.input, args.verbose, args.threshold)


if __name__ == "__main__":
    main()
