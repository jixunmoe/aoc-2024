import argparse
from collections import Counter, defaultdict


# mix = xor
# prune = take low-24 bits -> secret & 0xFF_FFFF


def derive_secret(secret: int):
    secret = (secret ^ (secret << 6)) & 0xFF_FFFF
    secret = (secret ^ (secret >> 5)) & 0xFF_FFFF
    secret = (secret ^ (secret << 11)) & 0xFF_FFFF
    return secret


def derive_secret_at(seed: int, n: int) -> tuple[int, dict[int, int]]:
    deltas = {}
    secret = seed
    secret_d = seed % 10

    delta_history = 0

    for i in range(n):
        next_secret = derive_secret(secret)
        next_secret_d = next_secret % 10

        delta_history = ((delta_history << 8) | ((next_secret_d - secret_d) % 256)) & 0xffff_ffff

        if i >= 3:
            if delta_history not in deltas:
                deltas[delta_history] = next_secret_d
        secret = next_secret
        secret_d = next_secret_d

    return secret, deltas


def solve_deltas(delta_list: list[dict[int, int]]):
    patterns = {pattern for d in delta_list for pattern in d.keys()}
    print(f'patterns = {len(patterns)}')
    best_pattern = max(patterns, key=lambda p: sum(deltas.get(p, 0) for deltas in delta_list))
    best_score = sum(deltas.get(best_pattern, 0) for deltas in delta_list)
    print(f'best pattern = {hex(best_pattern)} {best_score=}')
    return best_score


def solve(input_path: str, /, **_kwargs):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '').splitlines()

    seeds = list(map(int, input_text))
    deltas = []
    p1 = 0
    for seed in seeds:
        secret, delta_data = derive_secret_at(seed, 2000)
        p1 += secret
        deltas.append(delta_data)
    print(f'p1: {p1}')

    p2 = solve_deltas(deltas)
    print(f'p2: {p2}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    solve(args.input, verbose=args.verbose)


if __name__ == "__main__":
    main()
