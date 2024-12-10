# Day 9: Disk Fragmenter

[[^ up]](../../README.asciidoc) [[< prev]](../day-08/README.MD) [[next >]](../day-10/README.MD) [[solution ✨]](./solve.py) [[c++ solution 🚀]](./solve.cpp)

<!-- article begin -->

## Part 1

- Iterate from both left and right
  - Look for empty spot in left, and non-empty spot in right
  - Swap them
- Repeat until left and right meet or cross over.

## Part 2

- To speed up, cache the size of each block.
- Iterate blocks by its id (high to low), then find empty slots from left.
  - Make sure the block _does not move to the right_.
  - If found, swap both blocks from left (free spot) and right (block with content)
- Repeat until all blocks are sorted.

Performance improvement:

- Since we only move blocks to the left, we can safely discard "free space" after current block.
- That means, we can just keep track of the free block and decrease its size, without worry about merging them.
- Now we can iterate by block-of-spaces, instead of each individual space.

※ Performance:

- v1: cpp (~0.2s) vs Python (~7.1s).
- v2: cpp (0.013s) vs Python (0.940s).

I have a feeling this might be dynamic programming problem, but I'm not good at it.

To compile and run the C++ solution using `g++`:

```shell
g++ -O2 -o solve.exe solve.cpp
./solve.exe input.txt
```

<!-- article end -->

---

* Puzzle: https://adventofcode.com/2024/day/9
* Input: https://adventofcode.com/2024/day/9/input

