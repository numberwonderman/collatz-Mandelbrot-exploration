# Project Requirements

This project requires Python 3.8+ and the following scientific and data analysis libraries.

These libraries can be installed using `pip`:

```bash
pip install numpy pandas matplotlib 
Library,Purpose
numpy,Fundamental package for scientific computing; used extensively for Mandelbrot grid generation and array operations.
pandas,"Used for creating, manipulating, and exporting the experimental results data (e.g., saving to experiment_01_results.csv)."
matplotlib,Used by src/visualization.py to generate the overlay plot of Collatz parameters on the Mandelbrot set.
*(Note: For formal Python projects, the list of libraries would typically be saved in a file named `requirements.txt`.)*