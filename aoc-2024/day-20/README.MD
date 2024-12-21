# Day 20: Race Condition

[[^ up]](../../README.asciidoc) [[< prev]](../day-19/README.MD) [[next >]](../day-21/README.MD) [[solution ✨]](./solve.py)

<!-- article begin -->

## Part 1

- Build Dijkstra's cost graph as cache.
- Iterate each "wall" position, find free space around the wall.
- Calculate the cost difference the lowest and highest free space, then -2 (crossing the wall) to get the time saved.

## Part 2

- Iterate each "free" space instead.
- Iterate all free blocks within `n` (=20) distance from the free space.
- Calculate the cost difference, adjusted to the actual distance.

<!-- article end -->

---

* Puzzle: https://adventofcode.com/2024/day/20
* Input: https://adventofcode.com/2024/day/20/input

