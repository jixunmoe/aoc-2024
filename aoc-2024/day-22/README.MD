# Day 22: Monkey Market

[[^ up]](../../README.asciidoc) [[< prev]](../day-21/README.MD) [[next >]](../day-23/README.MD) [[solution ✨]](./solve.py)  [[c++ solution 🚀]](./solve.cpp)

<!-- article begin -->

## Part 1

Build a simulator. Use bit-wise operator to speed it up.

## Part 2

Track the price delta, 4 price-delta can fit in a 20 bit number (`5` bit each).

In the python implementation it uses unsigned 8-bit number to represent each group of price-deltas,
and set it if not there (only the first one meets the sequence is accepted).

Then we find the sums for each price deltas (sequence) and find the maximum.

---

My C++ implementation uses u8 array with length `1 << 20` (~1MiB) to track 
the price delta pattern and price it gets.
Since the possible value for each delta is `-9 <= delta <= 9`, this can be easily fit within a
20-bit number. To identify whether a pattern has already occupied, the MSB (`0x80`) will be set.

If we want to know which price each buyer needs to track, we'll need to store `n` MiB of bytes
(my puzzle input had 2k+ "buyers"), so I also added a `PRINT_BUYER_PRICES` flag that can be
turned off to use max around 6MiB of RAM.

With sane vector optimisation, it is able to complete within 300ms.

<!-- article end -->

---

* Puzzle: https://adventofcode.com/2024/day/22
* Input: https://adventofcode.com/2024/day/22/input

