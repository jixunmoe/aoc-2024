# Day 13: Claw Contraption

[[^ up]](../../README.asciidoc) [[< prev]](../day-12/README.MD) [[next >]](../day-14/README.MD) [[solution ✨]](./solve.py)

<!-- article begin -->

## Part 1

The question can be re-phrased to _find $`a`$ and $`b`$ for each sub-puzzle_:

$$
a \begin{pmatrix} x_1 \\\\ y_1 \end{pmatrix} +
b \begin{pmatrix} x_2 \\\\ y_2 \end{pmatrix} =
  \begin{pmatrix} x_p \\\\ y_p \end{pmatrix}
$$

Which we can then re-write the equation to:

$$
\begin{align*}
a \cdot x_1 + b \cdot x_2 &=& x_p
\\\\
a \cdot y_1 + b \cdot y_2 &=& y_p
\end{align*}
$$

Multiply the equations by $x_2$ and $x_1$ respectively:

$$
\begin{align*}
( a \cdot x_1 + b \cdot x_2 = x_p ) \cdot y_1
&\implies& a \cdot x_1 \cdot y_1 + b \cdot x_2 \cdot y_1 = x_p \cdot y_1
\\\\
( a \cdot y_1 + b \cdot y_2 = y_p ) \cdot x_1
&\implies& a \cdot y_1 \cdot x_1 + b \cdot y_2 \cdot x_1 = y_p \cdot x_1
\end{align*}
$$

Subtract the 2 equations will remove the term "$`a \cdot x_1 \cdot y_1`$":


$$
\begin{align*}
b \cdot x_2 \cdot y_1 - b \cdot y_2 \cdot x_1 &=& x_p \cdot y_1 - y_p \cdot x_1
\\\\
b ( x_2 \cdot y_1 - \cdot y_2 \cdot x_1 ) &=& x_p \cdot y_1 - y_p \cdot x_1
\\\\
b &=& \frac{x_p \cdot y_1 - y_p \cdot x_1}{x_2 \cdot y_1 - \cdot y_2 \cdot x_1}
\end{align*}
$$

Then substitute values back to find $a$:

$$
a = \frac{x_p - b \cdot x_2}{x_1}
$$

## Part 2

Same as part 1, but add $10,000,000,000,000$ to $`\begin{pmatrix} x_p \\ y_p \end{pmatrix}`$ before solving.

<!-- article end -->

---

* Puzzle: https://adventofcode.com/2024/day/13
* Input: https://adventofcode.com/2024/day/13/input

