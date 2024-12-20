# Day 17: Chronospatial Computer

[[^ up]](../../README.asciidoc) [[< prev]](../day-16/README.MD) [[next >]](../day-18/README.MD) [[solution ✨]](./solve.py) [[c++ solution 🚀]](./solve.cpp)

<!-- article begin -->

## Part 1

Create a disassembler / interpreter for the puzzle, then simulate the program execution.

## Part 2

> [!NOTE]
> Part 2 solution is only available in C++.

For determined output, find out the input.

- Brute force will not work
- Need to decompile and understand what the program does

Using the output from trace or decompiler, it looks more or less like this:

```asm
LB_00:
    MOV B, A       ; (mod 8)
    XOR B, #imm1
    SHR C, A, B
    XOR B, #imm2
    XOR B, C       ; (hidden operand)
    WRITE B        ; (mod 8)
    SHR A, A, #3
    JNZ LB_00
```

Where `imm1`, `imm2` and "hidden operand" were potentially unique to each user.

It can be translated to C code like this:

```c
#define IMM1 (1)
#define IMM2 (2)

void run(int A, int B, int C) {
  do {
    B = (A % 8) ^ IMM1;
    C = A >> B;
    B ^= C ^ IMM2;
    printf("%d\n", B % 8);
    A >>= 3;
  } while (A);
}
```

There's no one way function to reverse this as the function is not injective.
However, we can attack and conquer the problem by looking at 3 bits at a time.

To produce the first output (3 bits), it depends on the lowest 10 bits of A
(up to 7 bits shifted + 3 bits from A),
we can search for all 10-bit numbers that produces the last 3 bits.

Once we got a 3-bits number confirmed, we move the 10-bits search window
left by 3 bits, and repeat the process until all input bits were processed.

Once the search completes, we should have a set of numbers found.
Sort the list of numbers, the lowest one is the answer to part 2.

See the C++ source code for more details.

<!-- article end -->

---

* Puzzle: https://adventofcode.com/2024/day/17
* Input: https://adventofcode.com/2024/day/17/input

