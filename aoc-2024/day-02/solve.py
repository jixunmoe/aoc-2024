import argparse
from typing import List, Callable

def is_safe_report(report: List[int]) -> bool:
    prev = report[0]
    pos_seq = True
    neg_seq = True
    for value in report[1:]:
        delta = value - prev
        pos_seq = pos_seq and (0 < delta <= 3)
        neg_seq = neg_seq and (-3 <= delta < 0)
        prev = value
    return pos_seq or neg_seq

def is_safe_report_damp(report: List[int]) -> bool:
    # dumb brute force but works
    for i in range(len(report)):
        temp = report.copy()
        temp.pop(i)
        if is_safe_report(temp):
            return True
    return False


def get_safe_report_count(reports: List[List[int]], safe_check: Callable[[List[int]], bool]) -> int:
    return sum(map(int, map(safe_check, reports)))


def solve(input_file: str):
    reports = []
    with open(input_file, "r") as file:
        for line in file:
            reports.append(list(map(int, line.strip().split(' '))))
    safe_report_count = get_safe_report_count(reports, is_safe_report)
    print(f"part1: safe = {safe_report_count}")
    safe_damp_report_count = get_safe_report_count(reports, is_safe_report_damp)
    print(f"part2: safe = {safe_damp_report_count}")

def main():
    is_safe_report_damp([1, 2, 7, 8, 9])

    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    args = parser.parse_args()
    solve(args.input)

if __name__ == "__main__":
    main()
