from abc import ABC
import argparse
from functools import cache
from itertools import product
from typing import Optional

g_verbose = False

CHR_A = ord('A')

UP = ord('^')
DOWN = ord('v')
LEFT = ord('<')
RIGHT = ord('>')

CHR_0 = ord('0')
CHR_1 = ord('1')
CHR_2 = ord('2')
CHR_3 = ord('3')
CHR_4 = ord('4')
CHR_5 = ord('5')
CHR_6 = ord('6')
CHR_7 = ord('7')
CHR_8 = ord('8')
CHR_9 = ord('9')


def get_dir_h(dx: int) -> int:
    return LEFT if dx < 0 else RIGHT


def get_dir_v(dy: int) -> int:
    return UP if dy < 0 else DOWN


class RobotPad(ABC):
    id: int = 0
    dir_cache: dict[tuple[int, int], list[list[int]]]
    pos_cache: dict[tuple[int, int], int]
    child: Optional['RobotPad'] = None

    @cache
    def cost_press_once(self, snapshot: tuple[int, ...]):
        my_id = self.id

        if not self.child:
            assert len(snapshot) == 1
            return 1, snapshot

        g_verbose and print(f'{"  " * my_id}bot #{my_id} request parent press')
        cost_moving, new_snapshot = self.child.cost_moving(CHR_A, snapshot[1:])
        cost_press, new_snapshot = self.child.cost_press_once(new_snapshot)
        return cost_moving + cost_press, (snapshot[0], *new_snapshot)

    @cache
    def cost_moving(self, target_button: int, snapshot: tuple[int, ...]):
        my_id = self.id
        current_button = snapshot[0]

        g_verbose and print(f'{"  " * my_id}bot #{my_id} plan {chr(current_button)} -> {chr(target_button)}')

        if current_button == target_button:
            g_verbose and print(f'{"  " * my_id}bot #{my_id} not moving, already at {chr(target_button)}')
            return 0, snapshot

        # Last layer
        distance = self.pos_cache[current_button, target_button]
        if not self.child:
            g_verbose and print(f'{"  " * my_id}bot #{my_id} move to {chr(target_button)}, cost={distance}')
            assert len(snapshot) == 1
            return distance, (target_button,)

        # Move parent node to the direction I want
        tracking = []
        for possible_routes in self.dir_cache[current_button, target_button]:
            route_cost = 0
            route_snapshot = snapshot[1:]
            for next_direction in possible_routes:
                cost_moving, route_snapshot = self.child.cost_moving(next_direction, route_snapshot)
                cost_press, route_snapshot = self.child.cost_press_once(route_snapshot)
                route_cost += cost_moving + cost_press
            tracking.append((route_cost, (target_button, *route_snapshot)))
        best_cost, best_snapshot = min(tracking, key=lambda x: x[0])
        g_verbose and print(f'{"  " * my_id}bot #{my_id} move to {chr(target_button)}, cost={best_cost}')
        return best_cost, best_snapshot

    def move(self, dst: int, snapshot: tuple[int, ...]):
        return self.cost_moving(dst, snapshot)


class NumPad(RobotPad):
    def __init__(self, bot_id: int):
        self.id = bot_id
        self.board = [
            [0x37, 0x38, 0x39],
            [0x34, 0x35, 0x36],
            [0x31, 0x32, 0x33],
            [0x00, 0x30, 0x41]
        ]
        self.pos_cache = {}
        self.board_lookup = {value: (x, y) for y, row in enumerate(self.board) for x, value in enumerate(row) if value}
        dir_cache: dict[tuple[int, int], list[list[int]]] = {}
        for ((a, (x1, y1)), (b, (x2, y2))) in product(self.board_lookup.items(), repeat=2):
            if a == b: continue
            # Find the direction of move from a to b
            dx = x2 - x1
            dy = y2 - y1

            x_count = abs(dx)
            y_count = abs(dy)

            # Only move in one direction
            if dx == 0 or dy == 0:
                dir_cache[a, b] = [[get_dir_h(dx) if dx else get_dir_v(dy)] * (x_count + y_count)]
            elif a in (CHR_0, CHR_A) and b in (CHR_1, CHR_4, CHR_7):
                # Can only move up and then left
                dir_cache[a, b] = [[UP] * y_count + [LEFT] * x_count]
            elif a in (CHR_1, CHR_4, CHR_7) and b in (CHR_0, CHR_A):
                # Can only move right and then down
                dir_cache[a, b] = [[RIGHT] * x_count + [DOWN] * y_count]
            else:
                # Can move both horizontally and vertically, any order
                dir_h = get_dir_h(dx)
                dir_v = get_dir_v(dy)
                dir_cache[a, b] = [[dir_h] * x_count + [dir_v] * y_count, [dir_v] * y_count + [dir_h] * x_count]

            self.pos_cache[a, b] = abs(dx) + abs(dy)
        self.dir_cache = dir_cache


class DirectionPad(RobotPad):
    def __init__(self, bot_id: int):
        self.id = bot_id
        self.board = [
            [0x00, UP, CHR_A],
            [LEFT, DOWN, RIGHT],
        ]
        self.board_lookup = {value: (x, y) for y, row in enumerate(self.board) for x, value in enumerate(row) if value}
        self.pos_cache = {}
        dir_cache: dict[tuple[int, int], list[list[int]]] = {}
        for ((a, (x1, y1)), (b, (x2, y2))) in product(self.board_lookup.items(), repeat=2):
            # Find the direction of move from a to b
            dx = x2 - x1
            dy = y2 - y1
            self.pos_cache[a, b] = abs(dx) + abs(dy)

            x_count = abs(dx)
            y_count = abs(dy)

            # Only move in one direction
            if dx == 0 or dy == 0:
                dir_cache[a, b] = [[get_dir_h(dx) if dx else get_dir_v(dy)] * (x_count + y_count)]
            elif a == LEFT and b in (UP, CHR_A):
                # Can only move right and then UP
                dir_cache[a, b] = [[RIGHT] * x_count + [UP] * y_count]
            elif a in (UP, CHR_A) and b == LEFT:
                # Can only move down and then left
                dir_cache[a, b] = [[DOWN] * y_count + [LEFT] * x_count]
            else:
                # Can move both horizontally and vertically, any order
                dir_h = get_dir_h(dx)
                dir_v = get_dir_v(dy)
                dir_cache[a, b] = [[dir_h] * x_count + [dir_v] * y_count, [dir_v] * y_count + [dir_h] * x_count]
        self.dir_cache = dir_cache


def solve_ex(codes: list[str], count: int) -> int:
    root = NumPad(0)
    node = root
    for i in range(count):
        bot = DirectionPad(i + 1)
        node.child = bot
        node = bot

    snapshot_init = tuple([CHR_A] * (count + 1))
    result = 0
    for code in codes:
        snapshot = snapshot_init
        total_cost = 0
        for current_chr in map(ord, code):
            prev_char = snapshot[0]
            cost, snapshot = root.cost_moving(current_chr, snapshot)
            cost_press, snapshot = root.cost_press_once(snapshot)
            g_verbose and print(
                f"** move {chr(prev_char)} -> {chr(current_chr)} cost={cost + cost_press} pos={''.join(map(chr, snapshot))}")
            total_cost += cost + cost_press
        numeric_part = int(code[:-1])
        print(f"{code} -> {total_cost} * {numeric_part}")
        result += total_cost * numeric_part

    return result


def solve(input_path: str, /, **_kwargs):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '').splitlines()

    p1 = solve_ex(input_text, 2)
    print(f'p1: {p1}')


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
