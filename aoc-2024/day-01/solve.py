import argparse
import re
from collections import Counter
from typing import List


def part1(left: List[int], right: List[int]) -> int:
    distance = 0
    for (a, b) in zip(sorted(left), sorted(right)):
        distance += abs(a - b)
    return distance


def part2(left: List[int], right: List[int]) -> int:
    counter_l = Counter(left)
    counter_r = Counter(right)

    similarity_score = 0
    for position in counter_l.keys():
        similarity_score += position * counter_r[position] * counter_l[position]
    return similarity_score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    args = parser.parse_args()

    left = []
    right = []
    with open(args.input, "r") as file:
        for line in file:
            m = re.match(r'(\d+)\s+(\d+)', line.strip())
            if m is None:
                raise Exception("Invalid input")
            left.append(int(m.group(1)))
            right.append(int(m.group(2)))

    distance = part1(left, right)
    print(f'part1: distance = {distance}')

    score = part2(left, right)
    print(f'part2: score    = {score}')


if __name__ == "__main__":
    main()
