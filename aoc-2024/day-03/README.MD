# Day 3: Mull It Over

[[^ up]](../../README.MD) [[< prev]](../day-02/README.MD) [[next >]](../day-04/README.MD) <!-- [[solution ✨]](./solve.py) -->

<!-- article begin -->

## Part 1

Simple regex matching.

```
mul\((\d+),(\d+)\)
```

Look for `"mul("`, digits, comma, digits, and `")"`, parse the number, and add the product.

## Part 2

Upgrade the regex to match the special cases.

```
((?:do|don't)\(\)|mul\((\d+),(\d+)\))
```

Look for:

- Either `"do()"` or `"don't()"`, or:
- `"mul("`, digits, comma, digits, and `")"`.

Iterate the results, handle each cases, and add the product if enabled.

<!-- article end -->

---

* Source: https://adventofcode.com/2024/day/3
* Puzzle input: https://adventofcode.com/2024/day/3/input
