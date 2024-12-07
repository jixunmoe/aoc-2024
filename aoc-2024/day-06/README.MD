# Day 6: Guard Gallivant

[[^ up]](../../README.asciidoc) [[< prev]](../day-05/README.MD) [[next >]](../day-07/README.MD) [[solution ✨]](./solve.py) [[solution 🦀]](./src/main.rs)

<!-- article begin -->

## Part 1

- Implement a "game engine" that simulates the board.
    - For each step taken, record the position and direction
    - If the position/direction combination has been visited, stop.
    - If the position is out of board, count unique positions visited.

## Part 2

- Use the points found in previous part
    - Place an extra "wall" on a point from the path.
    - See if the player can get out of the board.
    - Count the number of positions.

Improve performance:

- Multiprocessing the iteration.

Iterate

<!-- article end -->

---

* Puzzle: https://adventofcode.com/2024/day/6
* Input: https://adventofcode.com/2024/day/6/input
