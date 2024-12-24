# Day 23: LAN Party

[[^ up]](../../README.asciidoc) [[< prev]](../day-22/README.MD) [[next >]](../day-24/README.MD) [[solution ✨]](./solve.py)

<!-- article begin -->

## Part 1

Iterate all members starts with `t`, then for each node it connects to,
find another node from the list that connects to both.

Remember to deduplicate.

## Part 2

Build a list of fully-connected networks, both act as a cache and allow
us to easily find all completed networks with size `n`.

Keep exploring until we found all nodes.

Thoughts for statically typed languages: could cast the names to `u16` to
speed up the lookup of sets (`set<int>` vs `set<string>`).

<!-- article end -->

---

* Puzzle: https://adventofcode.com/2024/day/23
* Input: https://adventofcode.com/2024/day/23/input

