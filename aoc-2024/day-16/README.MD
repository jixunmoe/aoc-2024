# Day 16: Reindeer Maze

[[^ up]](../../README.asciidoc) [[< prev]](../day-15/README.MD) [[next >]](../day-17/README.MD) [[solution ✨]](./solve.py) [[c++ solution 🚀]](./solve.cpp)

<!-- article begin -->

## Part 1

- Explore maze, calculate the cost of each path (BFS)
- Find the cost of the shortest path

## Part 2

- BFS does not seem to be optimal finding all paths, unless proper caching can be done.
- Hence, using Dijkstra's algorithm to build a graph and then backtrack all best paths.

Optimisation inspired from [scorixear's solution](https://github.com/scorixear/AdventOfCode/blob/5302069/2024/16/dijkstra2.py).

C++ implementation can complete in `~0.02s`, while Python implementation takes `~0.49s`.

<!-- article end -->

---

* Puzzle: https://adventofcode.com/2024/day/16
* Input: https://adventofcode.com/2024/day/16/input

