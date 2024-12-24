import argparse
import re
from typing import Iterable

ops = {
    "XOR": lambda a, b: a ^ b,
    "AND": lambda a, b: a & b,
    "OR": lambda a, b: a | b,
}

type Machines = dict[str, tuple[str, str, str]]


def merge_bits(items: Iterable[int]):
    result = 0
    for item in items:
        result = (result << 1) | item
    return result


class PlugBoard:
    def __init__(self, text: str, verbose=False):
        text_definition, text_rules = text.split('\n\n', maxsplit=2)

        self.verbose = verbose
        self.names: set[str] = set()
        self.registers = {}
        self.machines: Machines = dict()

        for m in re.finditer(r'(.+?): ([01])', text_definition):
            self.registers[m.group(1)] = int(m.group(2))

        for m in re.finditer(r'^(\w+) (XOR|OR|AND) (\w+) -> (\w+)$', text_rules, re.M):
            a, op, b, r = m.groups()
            self.machines[r] = (op, a, b)
            self.names.add(a)
            self.names.add(b)
            self.names.add(r)

    def simulate(self, result_reg_list: list[str], registers: dict[str, int] = None):
        if registers is None:
            registers = self.registers.copy()

        to_solve: set[str] = {*result_reg_list}
        while to_solve:
            next_solve = set()
            for target in to_solve:
                if target in registers: continue
                (op, a, b) = self.machines[target]
                if a in registers and b in registers:
                    registers[target] = ops[op](registers[a], registers[b])
                else:
                    next_solve.add(a)
                    next_solve.add(b)
                    next_solve.add(target)
            if to_solve == next_solve:
                return []
            to_solve = next_solve
        return merge_bits(map(lambda name: registers[name], result_reg_list))

    def find_reg(self, op: str, r1: str, r2: str):
        for dst, (op_inner, a, b) in self.machines.items():
            if op_inner == op and {a, b} == {r1, r2}:
                return dst
        return None

    def replace_board(self, r1, r2):
        self.machines[r1], self.machines[r2] = self.machines[r2], self.machines[r1]

    def fix_machine(self):
        replaced = set()

        # Carry
        cc_prev = self.find_reg('AND', 'x00', 'y00')
        assert cc_prev, 'initial carry not found'

        for i in range(1, 45):
            x_reg = f'x{i:02d}'
            y_reg = f'y{i:02d}'
            z_reg = f'z{i:02d}'

            # add: get z-th bit
            # t[i] = x[i] ^ y[i]
            # z[i] = t[i] ^ c[i - 1]
            t = self.find_reg('XOR', x_reg, y_reg)
            assert t, 't not found'
            assert not t.startswith('z'), 'not handling when t is a "z_reg"'

            # Find all machines, where (z[i] = XOR, t, c[-1]) is
            actual_z_reg = self.find_reg('XOR', t, cc_prev)
            if not actual_z_reg:
                # t needs replace.
                # find one that XOR cc[i - 1]
                for r, (op, ta, tb) in self.machines.items():
                    if op == 'XOR' and cc_prev in (ta, tb):
                        t_replace = tb if ta == cc_prev else ta
                        self.verbose and print(f'replace t: {t} {t_replace}')
                        self.replace_board(t, t_replace)
                        replaced = {*replaced, t, t_replace}
                        t = t_replace
                        break
            elif actual_z_reg != z_reg:
                self.verbose and print(f'replace z: {z_reg} {actual_z_reg}')
                self.replace_board(z_reg, actual_z_reg)
                replaced = {*replaced, z_reg, actual_z_reg}

            # add: get carry
            # a[i] = x[i] & y[i]
            # b[i] = t[i] & c[i - 1]
            # c[i] = a[i] | b[i]
            a = self.find_reg('AND', x_reg, y_reg)
            b = self.find_reg('AND', t, cc_prev)
            c = self.find_reg('OR', a, b)
            assert None not in (a, b, c)

            cc_prev = c
        return replaced


def solve(input_path: str, /, verbose=False, **_kwargs):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '')

    pb = PlugBoard(input_text, verbose)
    z_names = [n for n in sorted(pb.names, reverse=True) if n.startswith('z')]
    p1 = pb.simulate(z_names)
    print(f'p1: {p1}')

    replacements = pb.fix_machine()
    assert len(replacements) == 8

    p2 = ','.join(sorted(replacements))
    print(f'p2: {p2}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    solve(args.input, verbose=args.verbose)


if __name__ == "__main__":
    main()
