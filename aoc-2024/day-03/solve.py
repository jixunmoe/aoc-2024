import argparse
import re


def part1(input_text: str):
    result = 0
    for m in re.findall(r'mul\((\d+),(\d+)\)', input_text):
        mul = int(m[0]) * int(m[1])
        result += mul
    return result


def part2(input_text: str):
    result = 0
    enabled = True
    for (item, a, b) in re.findall(r"((?:do|don't)\(\)|mul\((\d+),(\d+)\))", input_text):
        match item:
            case 'do()':
                enabled = True
            case "don't()":
                enabled = False
            case _:
                result += (int(a) * int(b)) if enabled else 0
    return result


def solve(input_file: str):
    with open(input_file, "r", encoding='utf-8') as file:
        input_text = file.read().strip()

    part1_result = part1(input_text)
    print(f"part1: {part1_result}")
    part2_result = part2(input_text)
    print(f"part2: {part2_result}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    args = parser.parse_args()
    solve(args.input)


if __name__ == "__main__":
    main()
