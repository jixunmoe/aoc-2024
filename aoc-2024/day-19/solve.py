import argparse


def solve_towels(design: str, towels: tuple[str]) -> bool:
    if not design:
        return True

    for towel in towels:
        if design.startswith(towel):
            remaining = design[len(towel):]
            if solve_towels(remaining, towels):
                return True
    return False

def solve_towels_all(cache: dict[str, int], design: str, towels: tuple[str]) -> int:
    if not design:
        return 1

    if design in cache:
        return cache[design]

    total = 0
    for towel in towels:
        if design.startswith(towel):
            remaining = design[len(towel):]
            total += solve_towels_all(cache, remaining, towels)
    cache[design] = total
    return total


def solve(input_path, verbose):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '')

    (towels, designs) = input_text.split('\n\n', 1)
    designs = designs.splitlines()
    # noinspection PyUnresolvedReferences
    towels: tuple[str] = tuple(towels.split(', '))

    p1 = sum([1 for ok in filter(lambda design: solve_towels(design, towels), designs) if ok])
    print(f"p1: {p1}")

    cache = {}
    p2 = sum([solve_towels_all(cache, design, towels) for design in designs])
    print(f"p2: {p2}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    solve(args.input, args.verbose)


if __name__ == "__main__":
    main()
