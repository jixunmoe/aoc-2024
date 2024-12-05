# Day 5: Print Queue

[[^ up]](../../README.MD) [[< prev]](../day-04/README.MD) [[next >]](../day-06/README.MD) [[solution ✨]](./solve.py)

<!-- article begin -->

## Part 1

- Parse rules and pages
- For each page set:
  - Remember visited pages
  - Check if visited pages exist in the current "forbidden" page list.
- Add all mid-page numbers.

## Part 2

- Same parsing, filter out the ones are not in valid sequence.
- For each _bad_ page set:
  - Make a new, empty list
  - For each page number:
    - Try to insert from right to left to the new list
    - If invalid, move the insert position to the left by one, until it is valid.
    

<!-- article end -->

---

Source: https://adventofcode.com/2024/day/5

