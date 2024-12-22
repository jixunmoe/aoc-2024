# Day 21: Keypad Conundrum

[[^ up]](../../README.asciidoc) [[< prev]](../day-20/README.MD) [[next >]](../day-22/README.MD) <!-- [[solution ✨]](./solve.py) -->

<!-- article begin -->

## Part 1

```text
FINAL    Bot 1    Bot 2    INPUT
.....    .....    .....    .....
.789.    ..^A.    ..^A.    ..^A.
.456......<v>......<v>......<v>.
.123.    .....    .....    .....
..0A.
.....
```

- To press the button, we need to find:
    - What button should we press?
    - In final, how can we move from one button to another?
        - Cost will be propagated from input.

Implemented like this in `solve_p1_only.py`.

## Part 2

For some reason, the algorithm does not work for `n > 2`. It is pretty fast with `n = 25`,
but it does not produce the correct shortest path.

Went online for help, found [solution by
`oshlern`](https://github.com/oshlern/adventofcode/blob/main/advent24/2024/python/18/concise.py).

- Look for the cost (number of key press) when there's no bots
- Adding a new layer, map the key presses to new layer.
    - i.e. what used to be a single press to go from `A` to `<`, now become `v<<<A` or `<<<vA`.
    - Find the shortest combination (also the legal one) from it.
    - Keep building until we reach the end.

<!-- article end -->

---

* Puzzle: https://adventofcode.com/2024/day/21
* Input: https://adventofcode.com/2024/day/21/input

