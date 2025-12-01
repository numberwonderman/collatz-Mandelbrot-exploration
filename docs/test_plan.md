# Test Plan: Core Function Confirmation

The first step in any experiment is to ensure the **Generalized Collatz Solver** (`src/collatz_generators.py`) is behaving correctly according to the defined parameters $(A=\text{Divisor}, B=\text{Multiplier}, C=\text{Adder})$.

## Test Objective

To confirm that the `generalized_collatz(n, A, B, C)` function accurately returns the sequence and the correct status (`converged`, `cycled`, or `diverged/max_iter`).

## Execution

Tests are executed via the script: `experiments/test_collatz.py`.

## Critical Test Cases

| Test # | Starting N | Parameters (A, B, C) | Expected Sequence Start | Expected Status | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | 6 | (2, 3, 1) | [6, 3, 10, 5, 16, 8, 4, 2, 1] | `converged` | Standard Collatz verification. |
| **2** | 2 | (2, -1, 3) | [2, 1, 2] | `cycled` | Verification of cycle detection for a simple 1, 2 loop. |
| **3** | 5 | (3, 4, 1) | [5, 7, 29, 38, 19, 25, 33, 11, ...] | `max_iter` | Verification of the max-iteration limit for potentially divergent/long-running cases. |

## Confirmation

The full experiment pipeline will only proceed after these unit tests successfully pass, confirming the reliability of the core mathematical model.