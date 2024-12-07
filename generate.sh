#!/bin/bash

toc=""
for i in $(seq 25); do
  day="day-$(printf "%02d" $i)"

  prev="[< prev]"
  next="[next >]"

  if [[ $i -ne 1 ]]; then
    prev="[[< prev]](../day-$(printf "%02d" $((i-1)))/README.MD)"
  fi
  if [[ $i -ne 25 ]]; then
    next="[[next >]](../day-$(printf "%02d" $((i+1)))/README.MD)"
  fi

  if [[ ! -f "aoc-2024/$day/README.MD" ]]; then
    mkdir -p "aoc-2024/$day"
    cat > "aoc-2024/$day/README.MD" <<EOF
# Day $i: TBD

[[^ up]](../../README.asciidoc) $prev $next <!-- [[solution ✨]](./solve.py) -->

<!-- article begin -->

<!-- article end -->

---

* Puzzle: https://adventofcode.com/2024/day/$i
* Input: https://adventofcode.com/2024/day/$i/input

EOF
  fi
done
