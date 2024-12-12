import argparse
import math
from collections import Counter


def blink_once(stone: int):
    if stone == 0:
        return (1,)

    digits = math.floor(math.log10(stone)) + 1
    if digits % 2 == 0:
        mod = math.pow(10, digits / 2)
        l = int(stone // mod)
        r = int(stone % mod)
        return l, r

    return (stone * 2024,)


def blink(input_stones: list[int]):
    stones = Counter(input_stones)
    while True:
        next_stones = Counter()
        for (stone, count) in stones.items():
            for next_stone in blink_once(stone):
                next_stones[next_stone] += count
        stones = next_stones
        yield lambda: sum(stones.values())


def solve(input_path, verbose):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip()

    puzzle = list(map(int, input_text.split(' ')))

    for (i, fetch_result) in zip(range(1, 75 + 1), blink(puzzle)):
        match i + 1:
            case 25:
                print(f'p1: {fetch_result()}')
            case 75:
                print(f'p2: {fetch_result()}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    # parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    solve(args.input, args.verbose)


if __name__ == "__main__":
    main()
