import argparse
import itertools
from multiprocessing import Pool
from os import cpu_count

from tqdm import tqdm

ops_def = {
    '+': lambda x, y: x + y,
    '*': lambda x, y: x * y,
    '||': lambda x, y: int(f'{x}{y}'),
}


class Game:
    first: int
    items: list[int]
    line: str
    result: int

    def __init__(self, line: str):
        self.line = line
        (result, items) = line.split(': ')
        self.result = int(result)
        self.first, *self.items = [int(x) for x in items.split(' ')]

    def __str__(self):
        return f'{self.result}: {self.items}'

    def __repr__(self):
        return str(self)

    def solve(self, allowed_ops: tuple[str, ...]):
        ops_len = len(self.items)
        for ops in itertools.product(*([allowed_ops] * ops_len)):
            if self.calc(ops) == self.result:
                return self.result

        return 0

    def calc(self, ops: tuple[str, ...]):
        result = self.first
        for (op, item) in zip(ops, self.items):
            result = ops_def[op](result, item)
        return result


def solve_line(line: str):
    game = Game(line)
    r1 = game.solve(('+', '*'))
    # skip check if r1 already found an answer
    r2 = r1 or game.solve(('+', '*', '||'))
    return r1, r2


def solve(input: str, threads: int):
    with open(input, "r", encoding='utf-8') as file:
        input_text = file.read().strip()

    lines = input_text.splitlines()

    p2 = 0
    p1 = 0
    with Pool(threads) as pool:
        for (r1, r2) in tqdm(pool.imap_unordered(solve_line, lines), total=len(lines)):
            p1 += r1
            p2 += r2

    print(f'Part 1: {p1}')
    print(f'Part 2: {p2}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    solve(args.input, args.threads)


if __name__ == "__main__":
    main()
