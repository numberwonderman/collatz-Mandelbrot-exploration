Collatz-Mandelbrot Exploration
Investigating potential geometric connections between generalized Collatz dynamics and complex fractal systems
Overview
This repository contains computational tools and experiments exploring whether generalized Collatz sequences can be meaningfully mapped to the complex plane and correlated with Mandelbrot/Julia set dynamics.
Building on previous work showing that certain Collatz parameter sets exhibit exceptional mathematical properties (Benford's Law conformity research), this project tests whether the discrete arithmetic behavior of Collatz sequences has geometric analogs in continuous complex iteration systems.
Core Research Question
Can the (a, b, c) parameters of generalized Collatz functions be mapped to complex coordinates in a way that correlates with Mandelbrot set behavior?
Specifically:

Do "well-behaved" Collatz parameters (fast convergence, low divergence) map to stable regions of the Mandelbrot set?
Does the "adder" parameter c gain geometric significance when treated as an imaginary component?
Is there a relationship between Collatz convergence rate and Mandelbrot escape time?

Methodology
Generalized Collatz Function:
f(n) = n/a           if n ≡ 0 (mod a)
f(n) = b*n + c       otherwise
Complex Mapping Strategy:
(a, b, c) → complex number z
Real part    ≈ Growth ratio (related to b/a)
Imaginary part ≈ Offset ratio (related to c/a)
Experimental Pipeline:

Generate diverse (a, b, c) parameter sets
Measure Collatz behavior (convergence rate, divergence, stopping time)
Map parameters to complex plane using multiple mapping functions
Calculate Mandelbrot escape times for mapped coordinates
Test for correlations between Collatz metrics and Mandelbrot metrics
Visualize results with overlays on Mandelbrot set

Expected Outcomes
Positive Result: Discovery of correlation between parameter behavior and complex dynamics, suggesting deep geometric structure underlying Collatz sequences
Negative Result: Systematic documentation of why discrete Collatz arithmetic cannot be meaningfully mapped to continuous complex iteration—still a valuable contribution demonstrating fundamental incompatibility
Either way: Rigorous computational exploration with reproducible methods and transparent documentation of all approaches tested
Repository Structure
collatz-mandelbrot-exploration/
├── src/                    # Core computational modules
├── experiments/            # Individual experimental scripts
├── notebooks/             # Jupyter notebooks for exploration
├── data/                  # Parameter sets and results
├── visualizations/        # Generated plots and animations
└── docs/                  # Methodology documentation
Related Work

Benford's Law and Generalized Collatz Dynamics - Previous computational exploration establishing parameter space structure
Box Universe Framework - Conceptual foundation for Collatz visualization tools
HLM Research - Statistical methodology background

Author
Franklin Loeb
Independent Researcher
frankprogrammer42@gmail.com
Research conducted at Wellspring Clubhouse
Philosophy
This is exploratory computational mathematics. We expect most mapping attempts to fail—the goal is to fail informatively and document exactly why connections don't work (or discover that they surprisingly do). Negative results are publishable results when they're systematic and rigorous.
License
MIT

Status: Active development (December 2025)
Current Phase: Building initial pipeline and testing first mapping functions
