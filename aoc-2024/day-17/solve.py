import argparse
import re

# 0  | ADV | COM      | DIV A, A, COM    | A = A / (2 ^ COM)
# 1  | BXL | IMM      | XOR B, IMM       | OP1 = CONST
# 2  | BST | COM      | MOV B, (COM % 8) | B = COM % 8 (AND 7)
# 3  | JNZ | IMM      | JNZ IMM          | if (A != 0) => IP = IMM
# 4  | BXC | 1xUNUSED | XOR B, C         |
# 5  | OUT | COM      | WRITE (COM % 8)  | Write the value of operand
# 6  | BDV | COM      | DIV B, A, COM    | B = A / (2 ^ COM)
# 7  | CDV | COM      | DIV C, A, COM    | C = A / (2 ^ COM)

INST_ADV = 0
INST_BXL = 1
INST_BST = 2
INST_JNZ = 3
INST_BXC = 4
INST_OUT = 5
INST_BDV = 6
INST_CDV = 7

REG_A = 0
REG_B = 1
REG_C = 2

DIV_MAPPING = {
    INST_ADV: 0,
    INST_BDV: 1,
    INST_CDV: 2
}


def letter(n: int):
    return chr(n + ord('A'))


def simulate(code: list[int], reg_init: tuple[int, int, int] = (0, 0, 0)):
    trace = []
    output = []
    regs: list[int] = [*reg_init]  # register A, B, C

    def read_combined_operand(value: int):
        if value <= 3:
            return int(value), f'#{value}'
        if value <= 6:
            return int(regs[value - 4]), f'REG.{letter(value - 4)}'
        return -1, f'#undef.{value}'

    pc = 0
    while pc < len(code):
        opcode = code[pc]
        if opcode in (INST_ADV, INST_BDV, INST_CDV):
            reg_idx = DIV_MAPPING[opcode]
            op_value, op_name = read_combined_operand(code[pc + 1])
            trace.append(f'{pc:02} | DIV {letter(reg_idx)}, A, {op_name} # A={regs[REG_A]}, {op_name}={op_value}')

            regs[reg_idx] = regs[REG_A] // (2 ** op_value)
            pc += 2
        elif opcode == INST_BXL:
            op_imm = code[pc + 1]
            trace.append(f'{pc:02} | XOR B, #{op_imm}')

            regs[REG_B] ^= op_imm
            pc += 2
        elif opcode == INST_BXC:
            trace.append(f'{pc:02} | XOR B, C # B={regs[REG_B]}, C={regs[REG_C]}')

            regs[REG_B] ^= regs[REG_C]
            pc += 2  # "legacy" reason
        elif opcode == INST_BST:
            op_value, op_name = read_combined_operand(code[pc + 1])
            regs[REG_B] = op_value & 7
            trace.append(f'{pc:02} | MOV B, {op_name} # {op_value} = {op_value & 7} mod 8')
            pc += 2
        elif opcode == INST_JNZ:
            op_imm = code[pc + 1]
            taken = regs[REG_A] != 0
            trace.append(f'{pc:02} | JNZ #{op_imm} # A={regs[REG_A]}, {"take" if taken else "miss"}')

            if taken:
                pc = op_imm
            else:
                pc += 2
        elif opcode == INST_OUT:
            op_value, op_name = read_combined_operand(code[pc + 1])
            trace.append(f'{pc:02} | WRITE {op_name} # {op_value} = {op_value & 7} mod 8')
            output.append(op_value & 7)

            pc += 2

    return regs, trace, output


def run_tests():
    # If register C contains 9, the program 2,6 would set register B to 1.
    regs, trace, output = simulate([2, 6], (0, 0, 9))
    print('\n'.join(trace))
    print(f'regs={regs}')
    print(f'output={output}')
    assert regs[REG_B] == 1
    print('-' * 80)

    # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    regs, trace, output = simulate([5, 0, 5, 1, 5, 4], (10, 0, 0))
    print('\n'.join(trace))
    print(f'regs={regs}')
    print(f'output={output}')
    assert output == [0, 1, 2]
    print('-' * 80)

    # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    regs, trace, output = simulate([0, 1, 5, 4, 3, 0], (2024, 0, 9))
    print('\n'.join(trace))
    print(f'regs={regs}')
    print(f'output={output}')
    assert output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert regs[REG_A] == 0
    print('-' * 80)

    # If register B contains 29, the program 1,7 would set register B to 26.
    regs, trace, output = simulate([1, 7], (0, 29, 0))
    print('\n'.join(trace))
    print(f'regs={regs}')
    print(f'output={output}')
    assert regs[REG_B] == 26
    print('-' * 80)

    # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    regs, trace, output = simulate([4, 0], (0, 2024, 43690))
    print('\n'.join(trace))
    print(f'regs={regs}')
    print(f'output={output}')
    assert regs[REG_B] == 44354
    print('-' * 80)

    # p2
    regs, trace, output = simulate([0, 3, 5, 4, 3, 0], (117440, 0, 0))
    print('\n'.join(trace))
    print(f'regs={regs}')
    print(f'output={output}')
    assert output == [0, 3, 5, 4, 3, 0]
    print('-' * 80)


def parse(file: str):
    values = list(map(int, re.findall(r'\d+', file)))
    regs: tuple[int, int, int] = tuple(values[:3])
    code = values[3:]
    return regs, code


def solve(input_path, verbose, run_test):
    if run_test:
        run_tests()
        return

    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '')

    regs, code = parse(input_text)
    verbose and print(f'regs={regs}')
    verbose and print(f'code={code}')

    regs, trace, output = simulate(code, regs)
    verbose and print('\n'.join(trace))
    verbose and print(f'regs={regs}')
    verbose and print(f'output={output}')

    p1 = ",".join(map(str, output))
    print(f'p1: {p1}')

    print(f'p2: check solve.cpp')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-t", "--test", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    solve(args.input, args.verbose, args.test)


if __name__ == "__main__":
    main()
