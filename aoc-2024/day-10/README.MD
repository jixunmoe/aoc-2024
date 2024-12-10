# Day 10: Hoof It

[[^ up]](../../README.asciidoc) [[< prev]](../day-09/README.MD) [[next >]](../day-11/README.MD) [[solution ✨]](./solve.py)

<!-- article begin -->

## Part 1

* Look for 0 (trail head)
* For each trail head,
  * Build a list of nodes (deduplicate) to next item in the trail (i.e. 2, 3, 4, ...)
  * Repeat the discovery of next item until `9` has found.
* Count how many nodes found in last discovery.
* Add all the nodes found in all discoveries.

<!-- article end -->

## Part 2

Same as part 1, but do not deduplicate the list.

---

* Puzzle: https://adventofcode.com/2024/day/10
* Input: https://adventofcode.com/2024/day/10/input

