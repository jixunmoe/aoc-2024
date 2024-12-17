# Day 11: Plutonian Pebbles

[[^ up]](../../README.asciidoc) [[< prev]](../day-10/README.MD) [[next >]](../day-12/README.MD) [[solution ✨]](./solve.py) [[c++ solution 🚀]](./solve.cpp)

<!-- article begin -->

## Part 1

- Brute force with lists.

## Part 2

- The order of stones doesn't matter.
- Tried brute force with caching, but it was still slow. `tqdm` estimates a few hours.
  - Ran out of memory (on a 8GB RAM machine) and bought down the system, OOM-killer did nothing 😞
  - The number of stones expands exponentially.

Went online and got a tip from [@1234abcdcba4321](https://www.reddit.com/r/adventofcode/comments/1hbwxrb/comment/m1jn1uj/):

> I claim that my code will take almost the exact same amount of time to compute the answer for the inputs `1` and `1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1`.
> I believe pretty much any working solution also will.
> Use this to guide your solution making process somehow.

So:

- Have a peek of the stones after a few iters.
- Observe that there's a lot of "repeated stones"
  - Work with the _unique_ stones and increment their counts at once.
  - Fewer "stones" to iter, everything is more manageable.

To think about it next time...

- Have a peek of the stones (and their counts) after a few iters 🙃

<!-- article end -->

---

* Puzzle: https://adventofcode.com/2024/day/11
* Input: https://adventofcode.com/2024/day/11/input
