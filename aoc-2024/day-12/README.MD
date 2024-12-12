# Day 12: Garden Groups

[[^ up]](../../README.asciidoc) [[< prev]](../day-11/README.MD) [[next >]](../day-13/README.MD) [[solution ✨]](./solve.py)

<!-- article begin -->

## Part 1

- Grid counting.
- Iterate board, explore neighbors with same value.
- For each (new) item found,
  - `+3` for perimeter.
  - `+1` for area.
  - If we already visited the node, decrement perimeter by `1`.
- Find the sum of `sides * perimeter`.

## Part 2

- Create 2 other grids with size `(rows + 1, cols + 1)`.
  - One to track unique horizontal lines and one for unique vertical lines.
  - Increment corresponding line.
- Scan for board for consecutive value of `1`s.
- Find the sum of `sides * area`.


<!-- article end -->

---

* Puzzle: https://adventofcode.com/2024/day/12
* Input: https://adventofcode.com/2024/day/12/input

