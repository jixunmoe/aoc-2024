import argparse


# maze
# Turn: 1000 pts
# Move: 1 pt


def parse(text: str):
    pass


def solve(input_path, verbose, grid_size):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-W", "--width", type=int, default=11)
    parser.add_argument("-H", "--height", type=int, default=7)
    # parser.add_argument("-t", "--threads", type=int, default=max(cpu_count() - 1, 1))
    args = parser.parse_args()
    solve(args.input, args.verbose, (args.width, args.height))


if __name__ == "__main__":
    main()
