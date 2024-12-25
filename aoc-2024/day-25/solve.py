import argparse
from operator import eq, ne

type KeyLockSemantic = tuple[int, int, int, int, int]


def parse(text: str):
    locks = []
    keys = []
    patterns = text.split('\n\n')
    for pattern in patterns:
        kl = pattern.splitlines()
        test_char = kl[0][0]
        is_lock = test_char == '#'
        comparator = eq if is_lock else ne
        key_lock_lengths = tuple(sum([int(comparator(line[i], test_char)) for line in kl[1:-1]]) for i in range(5))
        (locks if is_lock else keys).append(key_lock_lengths)
    return locks, keys


def solve(input_path: str, /, verbose=False, **_kwargs):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '')

    locks, keys = parse(input_text)

    # p1: Brute force them all!
    p1 = 0
    for lock in locks:
        for key in keys:
            if all(l + k <= 5 for l, k in zip(lock, key)):
                verbose and print(f'{lock=} {key=}')
                p1 += 1
    print(f'p1: {p1}')

    print(f'p2: N/A')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    solve(args.input, verbose=args.verbose)


if __name__ == "__main__":
    main()
