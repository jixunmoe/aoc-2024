import argparse
from itertools import product

# Inspired from: https://github.com/oshlern/adventofcode/blob/main/advent24/2024/python/18/concise.py

g_verbose = False

BOARD_NUMPAD = {c: (x, y) for y, row in enumerate(["789", "456", "123", " 0A"]) for x, c in enumerate(row)}
BOARD_DIRPAD = {c: (x, y) for y, row in enumerate([" ^A", "<v>"]) for x, c in enumerate(row)}

INFINITY = float('inf')


def solve_code(code: str, count: int) -> int:
    cache = {(src, dst): 1 for (src, dst) in product(BOARD_DIRPAD, repeat=2)}

    def get_cost(move: str):
        # Each layer of controller start from "A", ends in "A" as well.
        return sum([cache[a, b] for (a, b) in zip('A' + move[:-1], move)])

    # Build layers
    for i, board in enumerate([BOARD_DIRPAD] * count + [BOARD_NUMPAD]):
        next_cache = {}

        for (key_start, (x1, y1)), (key_end, (x2, y2)) in product(board.items(), repeat=2):
            if key_start == ' ' or key_end == ' ': continue

            hor_move = ('>' if (x1 < x2) else '<') * abs(x1 - x2)
            ver_move = ('v' if (y1 < y2) else '^') * abs(y1 - y2)

            cost_hor_first = INFINITY if (x2, y1) == board[' '] else get_cost(hor_move + ver_move + 'A')
            cost_ver_first = INFINITY if (x1, y2) == board[' '] else get_cost(ver_move + hor_move + 'A')
            min_cost = min(cost_hor_first, cost_ver_first)
            next_cache[key_start, key_end] = min_cost
        cache = next_cache

    final_cost = get_cost(code)
    g_verbose and print(f'{code=} {final_cost=}')
    return final_cost


def solve_ex(codes: list[str], count: int) -> int:
    return sum([solve_code(code, count) * int(code[:-1]) for code in codes])


def solve(input_path: str, /, **_kwargs):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '').splitlines()

    p1 = solve_ex(input_text, 2)
    print(f'p1: {p1}')
    p2 = solve_ex(input_text, 25)
    print(f'p2: {p2}')


def main():
    global g_verbose
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--threshold", type=int, default=50, help="Threshold (p2)")
    args = parser.parse_args()
    g_verbose = args.verbose
    solve(args.input)


if __name__ == "__main__":
    main()
