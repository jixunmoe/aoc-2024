import argparse
import math
import re


def parse(text: str):
    result = []
    btn_a = None
    btn_b = None

    for line in text.splitlines():
        if (m := re.match(r"Button ([AB]): X\+(\d+), Y\+(\d+)", line)) is not None:
            btn = (int(m.group(2)), int(m.group(3)))
            if m.group(1) == "A":
                btn_a = btn
            else:
                btn_b = btn
        elif (m := re.match(r"Prize: X=(\d+), Y=(\d+)", line)) is not None:
            prize = (int(m.group(1)), int(m.group(2)))
            assert btn_a is not None and btn_b is not None
            result.append((btn_a, btn_b, prize))
            btn_a = btn_b = None
        else:
            assert line == "", f"unexpected line {line}"

    return result


def try_solve(entry, offset):
    (x1, y1), (x2, y2), (xp, yp) = entry

    xp += offset
    yp += offset

    b = (y1 * xp - x1 * yp) / (x2 * y1 - x1 * y2)
    if b.is_integer():
        a = (xp - b * x2) / x1
        if a.is_integer():
            return entry, int(a), int(b)
    return None

def solve(input_path, verbose):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip()

    data = parse(input_text)

    answers = []
    price_a = 3
    price_b = 1
    for offset in (0, 10000000000000):
        answer = 0
        for (q, a, b) in filter(bool, map(lambda x: try_solve(x, offset), data)):
            answer += a * price_a + b * price_b
        answers.append(answer)
    p1, p2 = answers
    print(f"p1: {p1}")
    print(f"p2: {p2}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    # parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    solve(args.input, args.verbose)


if __name__ == "__main__":
    main()
