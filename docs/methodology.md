test confirmatinon i must ensure my core code works.


# Experiment 01: Collatz-Mandelbrot Correlation Methodology

This experiment tests the hypothesis that generalized Collatz parameter sets $(A, B, C)$ which map to the stable region of the Mandelbrot set will exhibit higher Collatz sequence convergence rates.

## 1. Parameter Definition (Collatz)

The generalized Collatz rule used is:

$$
n \to
\begin{cases}
n / A & \text{if } n \equiv 0 \pmod A \\
(B n + C) / A^k & \text{if } n \not\equiv 0 \pmod A
\end{cases}
$$

Where:
* $A$ is the **Divisor**.
* $B$ is the **Multiplier**.
* $C$ is the **Adder**.
* $A^k$ represents the maximal division shortcut, applied for non-standard $(2, 3, 1)$ cases.

A set of 100 random parameter combinations $(A, B, C)$ are generated within a restricted integer range (e.g., $A \in [2, 10]$, $B \in [1, 10]$, $C \in [1, 10]$).

## 2. Collatz Metric Calculation

For each parameter set $(A, B, C)$:
1.  $N$ initial starting numbers (e.g., $N=50$) are tested.
2.  Each sequence is run until it converges to $1$, enters a cycle, or hits the maximum iteration limit ($\text{max\_iter}=10^6$) or divergence limit ($\text{max\_value}=10^{50}$).
3.  The primary metric recorded is the **Convergence Rate**, defined as the percentage of the $N$ initial numbers that successfully converge to $1$.

## 3. Complex Plane Mapping

The discrete integer parameters $(A, B, C)$ are mapped to a continuous complex number $z$ using the following transformation (Mapping V1):

$$
z = \left(\frac{B}{A}\right) + \left(\frac{C}{A}\right) i
$$

* The **Real component** represents the growth ratio ($\text{Multiplier}/\text{Divisor}$).
* The **Imaginary component** represents the offset ratio ($\text{Adder}/\text{Divisor}$).

## 4. Mandelbrot Metric Calculation

For the resulting complex number $z$:
1.  The standard Mandelbrot iteration $z_{k+1} = z_k^2 + c$ (where $c=z$) is performed, starting at $z_0=0$.
2.  The number of iterations required for the magnitude $|z_k|$ to exceed $2$ (the escape condition) is recorded as the **Escape Time**. A higher Escape Time indicates the point is closer to or inside the stable Mandelbrot set.

## 5. Correlation and Visualization

The experiment calculates the Pearson correlation coefficient between the **Collatz Convergence Rate** and the **Mandelbrot Escape Time** across all 100 samples.

The results are visualized using a scatter plot:
* **X-axis:** Real component of $z$ ($B/A$)
* **Y-axis:** Imaginary component of $z$ ($C/A$)
* **Point Color:** Collatz Convergence Rate (using a colormap to show stability/instability)

This visualization tests the core hypothesis visually by observing if highly-convergent Collatz parameter sets cluster inside the Mandelbrot set boundary.