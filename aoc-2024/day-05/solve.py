import argparse
import re


class Parser:
    rules: dict[int, list[int]]
    pages: list[list[int]]

    def __init__(self, puzzle: str):
        self.rules = {}
        self.pages = []
        is_page_rules = True
        for line in puzzle.splitlines():
            if line == '':
                is_page_rules = False
                continue

            if is_page_rules:
                m = re.match(r"(\d+)\|(\d+)", line)
                if m is None:
                    raise ValueError(f"Invalid line: {line}")
                before = int(m.group(1))
                after = int(m.group(2))
                self.rules[before] = (self.rules[before] if before in self.rules else []) + [after]
            else:
                self.pages.append([int(x) for x in line.split(',')])

    def check_page(self, page: list[int]):
        previous_page_nos = set()
        for page_no in page:
            if page_no in self.rules:
                for after_items in self.rules[page_no]:
                    if after_items in previous_page_nos:
                        return False
            previous_page_nos.add(page_no)
        return True

    def mid_page_no(self, page: list[int]):
        n = len(page)
        if n % 2 == 0:
            raise ValueError("Invalid page length (even)")
        return page[n // 2]


def part1(parser: Parser, verbose: bool):
    return sum([parser.mid_page_no(page) for page in parser.pages if parser.check_page(page)])


def part2(parser: Parser, verbose: bool):
    result = []
    for page_set in parser.pages:
        # remove the ones that is in correct order
        if parser.check_page(page_set):
            continue

        # Try to insert one at a time.
        fixed_page_set = []
        for (i, page_no) in enumerate(page_set):
            print(f'i: {i}, page_no: {page_no}') if verbose else None
            for j in range(i, -1, -1):
                new_page_set = fixed_page_set.copy()
                new_page_set.insert(j, page_no)
                if parser.check_page(new_page_set):
                    fixed_page_set = new_page_set
                    print(f'fixed: {fixed_page_set}') if verbose else None
                    break
        assert parser.check_page(fixed_page_set), "Failed to fix the page"
        result.append(fixed_page_set)
    return sum([parser.mid_page_no(page) for page in result])


def solve(input_file: str, verbose: bool):
    with open(input_file, "r", encoding='utf-8') as file:
        input_text = file.read().strip()
    parser = Parser(input_text)

    part1_result = part1(parser, verbose)
    print(f"part1: {part1_result}")
    part2_result = part2(parser, verbose)
    print(f"part2: {part2_result}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    solve(args.input, args.verbose)


if __name__ == "__main__":
    main()
