import argparse

UP = ord('^')
DOWN = ord('v')
LEFT = ord('<')
RIGHT = ord('>')

type Grid = list[list[int]]
type Cord = tuple[int, int]  # x, y
type Size = tuple[int, int]  # width, height
type DijkstraCosts = dict[Cord, int]
type DijkstraNodes = dict[Cord, list[Cord]]

def default_cost_fn(d: int) -> int:
    return 1

def dijkstra(grid: Grid, start: Cord, /, size: Size = None, cost_fn: callable = default_cost_fn) -> tuple[DijkstraNodes, DijkstraCosts]:
    previous: DijkstraNodes = {}
    costs: DijkstraCosts = {}
    w, h = size if size else (len(grid[0]), len(grid))

    work: list[tuple[int, int, int]] = [(0, *start)]
    costs[start] = 0

    while work:
        prev_cost, cx, cy = work.pop(0)
        prev_node = cx, cy
        for d, dx, dy in ((RIGHT, 1, 0), (DOWN, 0, 1), (LEFT, -1, 0), (UP, 0, -1)):
            x, y = cx + dx, cy + dy
            if not (0 <= x < w and 0 <= y < h):
                continue

            if grid[y][x] & 0x80:
                continue

            cost = prev_cost + cost_fn(d)
            node: Cord = (x, y)

            if node not in costs or cost < costs[node]:
                costs[node] = cost
                previous[node] = [prev_node]
                work.append((cost, x, y))
            elif cost == costs[node]:
                previous[node].append(prev_node)

    return previous, costs

def dijkstra_cost(grid: Grid, start: Cord, end: Cord, /, size: Size = None, cost_fn: callable = default_cost_fn) -> int:
    _, costs = dijkstra(grid, start, size=size, cost_fn=cost_fn)
    return costs[end]


def build_path(nodes: DijkstraNodes, start: Cord, end: Cord) -> list[Cord]:
    path = []
    node = end
    while node != start:
        path.append(node)
        node = nodes[node][0]
    path.append(start)
    path.reverse()
    return path

def solve_ex(codes: list[str]) -> int:
    num_pad = [
        [0x37, 0x38, 0x39],
        [0x34, 0x35, 0x36],
        [0x31, 0x32, 0x33],
        [0xff, 0x30, 0x41]
    ]
    num_pad_start = 2, 3
    num_pad_size = len(num_pad[0]), len(num_pad)
    num_pad_mapping = {num: (x, y) for y, row in enumerate(num_pad) for x, num in enumerate(row) if
                       num & 0x80 == 0}

    arrow_pad = [
        [0xff, UP, 0x41],
        [LEFT, DOWN, RIGHT],
    ]
    arrow_pad_start = 2, 0
    arrow_pad_size = len(arrow_pad[0]), len(arrow_pad)
    arrow_pad_mapping = {num: (x, y) for y, row in enumerate(arrow_pad) for x, num in enumerate(row) if
                         num & 0x80 == 0}

    def do_cost_calc_bot_2(d: int) -> int:
        total_cost = 0
        target = arrow_pad_mapping[d]
        total_cost += dijkstra_cost(arrow_pad, arrow_pad_start, target, size=arrow_pad_size)
        # press the button
        total_cost += 1
        # move back
        total_cost += dijkstra_cost(arrow_pad, target, arrow_pad_start, size=arrow_pad_size)
        # press the button
        total_cost += 1
        return total_cost

    def do_cost_calc_bot_1(d: int) -> int:
        total_cost = 0
        assert d in arrow_pad_mapping
        target = arrow_pad_mapping[d]
        total_cost += dijkstra_cost(arrow_pad, arrow_pad_start, target, size=arrow_pad_size, cost_fn=do_cost_calc_bot_2)
        # press the button
        total_cost += 1
        # move back
        total_cost += dijkstra_cost(arrow_pad, target, arrow_pad_start, size=arrow_pad_size, cost_fn=do_cost_calc_bot_2)
        # press the button
        total_cost += 1
        return total_cost

    for code in codes:
        # Inputs at lowest layer
        prev_pos = num_pad_mapping[0x41] # Start at A
        cost_for_code = 0
        for single_code in map(ord, code):
            nodes, costs = dijkstra(num_pad, prev_pos, size=num_pad_size, cost_fn=do_cost_calc_bot_1)
            current_cost =  costs[num_pad_mapping[single_code]]
            cost_for_code += current_cost
            print(f"  cost for {chr(single_code)}: {current_cost}")

            prev_pos = num_pad_mapping[single_code]
        print(f"Cost for code {code}: {cost_for_code}")
        # break

    return -1

def solve(input_path: str, /, **_kwargs):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '').splitlines()

    solve_ex(input_text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--threshold", type=int, default=50, help="Threshold (p2)")
    args = parser.parse_args()
    solve(args.input)


if __name__ == "__main__":
    main()
