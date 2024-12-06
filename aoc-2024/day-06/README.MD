# Day 6: Guard Gallivant

[[^ up]](../../README.MD) [[< prev]](../day-05/README.MD) [[next >]](../day-07/README.MD) [[solution ✨]](./solve.py)

<!-- article begin -->

## Part 1

- Implement a "game engine" that simulates the board.
  - For each step taken, record the position and direction
  - If the position/direction combination has been visited, stop.
  - If the position is out of board, count unique positions visited.

## Part 2

- Iterate the board
  - Place an extra "wall" on the board, if that pos is not already wall nor player.
  - See if the player can get out of the board.
  - Count the number of positions.

Improve performance:

- Multiprocessing the iteration.

Iterate

<!-- article end -->

---

Source: https://adventofcode.com/2024/day/6

