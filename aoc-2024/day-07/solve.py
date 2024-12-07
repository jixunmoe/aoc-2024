import argparse
import itertools

ops_def = {
    '+': lambda x, y: x + y,
    '*': lambda x, y: x * y,
    '||': lambda x, y: int(f'{x}{y}'),
}


class Game:
    items: list[int]
    line: str
    result: int

    def __init__(self, line: str):
        self.line = line
        (result, items) = line.split(': ')
        self.result = int(result)
        self.items = [int(x) for x in items.split(' ')]

    def __str__(self):
        return f'{self.result}: {self.items}'

    def __repr__(self):
        return str(self)

    def solve(self, allowed_ops: tuple[str, ...]):
        ops_len = len(self.items) - 1
        for ops in itertools.product(*([allowed_ops] * ops_len)):
            if self.calc(ops, self.items) == self.result:
                return itertools.chain.from_iterable(zip(self.items, ops + ('',)))

        return None

    @staticmethod
    def calc(ops: tuple[str, ...], items: list[int]):
        result = items[0]
        for (op, item) in zip(ops, items[1:]):
            result = ops_def[op](result, item)
        return result


def solve(input: str, verbose: bool):
    with open(input, "r", encoding='utf-8') as file:
        input_text = file.read().strip()

    games = [Game(line) for line in input_text.splitlines()]
    p1 = sum([game.result if game.solve(('+', '*')) is not None else 0 for game in games])
    print(p1)
    p2 = sum([game.result if game.solve(('+', '*', '||')) is not None else 0 for game in games])
    print(p2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    solve(args.input, args.verbose)


if __name__ == "__main__":
    main()
