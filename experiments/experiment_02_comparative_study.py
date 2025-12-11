import pandas as pd
from scipy.stats import pearsonr
import numpy as np # Needed for the map_params_polar and map_params_logarithmic functions
# Add these three lines near the top of your script
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- ASSUMED UTILITY FUNCTIONS ---
# This is a standard Mandelbrot calculation function (from the original experiment)
def calculate_mandelbrot_escape_time(c: complex, max_iter: int = 100, bailout: float = 2.0) -> int:
    """Calculates the number of iterations before the sequence diverges."""
    z = 0 + 0j
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > bailout:
            # Return i (the number of steps taken before divergence)
            return i
    # Return max_iter if the sequence did not diverge (bounded)
    return max_iter 

# --- IMPORT ALL FOUR MAPPING HYPOTHESES ---
# NOTE: Ensure these functions are correctly defined in src/mapping_functions.py
from src.mapping_functions import (
    map_params_to_complex_v1,      # Hypothesis A
    map_params_logarithmic,        # Hypothesis B
    map_params_polar,              # Hypothesis C
    map_params_reciprocal_products # Hypothesis D
)

def run_comparative_study():
    """
    Loads Experiment 01 data and runs the correlation test against 
    four different Mandelbrot parameter mappings.
    """
    try:
        # 1. Load the clean Collatz data
        data_path = 'data/results/experiment_01_results.csv'
        df_clean = pd.read_csv(data_path)
        print(f"✅ Data loaded successfully from {data_path}. Total samples: {len(df_clean)}")
        
    except FileNotFoundError:
        print("❌ ERROR: The file 'data/results/experiment_01_results.csv' was not found.")
        print("Please ensure you have saved the clean 100-sample CSV content there.")
        return

    # --- 2. APPLY MAPPING HYPOTHESES ---
    print("\nApplying four different Collatz-to-Mandelbrot mappings...")
    
    # Hypothesis A (V1 - Control)
    df_clean['z_v1'] = df_clean.apply(
        lambda row: map_params_to_complex_v1(row['a_divisor'], row['b_multiplier'], row['c_adder']), axis=1
    )

    # Hypothesis B (Logarithmic)
    df_clean['z_log'] = df_clean.apply(
        lambda row: map_params_logarithmic(row['a_divisor'], row['b_multiplier'], row['c_adder']), axis=1
    )

    # Hypothesis C (Polar/Trigonometric)
    df_clean['z_polar'] = df_clean.apply(
        lambda row: map_params_polar(row['a_divisor'], row['b_multiplier'], row['c_adder']), axis=1
    )

    # Hypothesis D (Reciprocal Products)
    df_clean['z_reciprocal'] = df_clean.apply(
        lambda row: map_params_reciprocal_products(row['a_divisor'], row['b_multiplier'], row['c_adder']), axis=1
    )

    # --- 3. CALCULATE MANDELBROT ESCAPE TIMES ---
    print("Calculating Mandelbrot Escape Time for all four hypotheses...")
    
    df_clean['escape_v1'] = df_clean['z_v1'].apply(calculate_mandelbrot_escape_time)
    df_clean['escape_log'] = df_clean['z_log'].apply(calculate_mandelbrot_escape_time)
    df_clean['escape_polar'] = df_clean['z_polar'].apply(calculate_mandelbrot_escape_time)
    df_clean['escape_reciprocal'] = df_clean['z_reciprocal'].apply(calculate_mandelbrot_escape_time)

    # --- 4. CALCULATE AND PRINT CORRELATIONS ---
    print("\n--- Comparative Correlation Results ---")
    
    collatz_rates = df_clean['collatz_conv_rate']

    corr_v1, _ = pearsonr(collatz_rates, df_clean['escape_v1'])
    print(f"Hypothesis A (V1 Control):         r = {corr_v1:.4f}")

    corr_log, _ = pearsonr(collatz_rates, df_clean['escape_log'])
    print(f"Hypothesis B (Logarithmic):        r = {corr_log:.4f}")

    corr_polar, _ = pearsonr(collatz_rates, df_clean['escape_polar'])
    print(f"Hypothesis C (Polar/Trigonometric): r = {corr_polar:.4f}")

    corr_recip, _ = pearsonr(collatz_rates, df_clean['escape_reciprocal'])
    print(f"Hypothesis D (Reciprocal Products): r = {corr_recip:.4f}")

    # Determine the best hypothesis
    correlations = {
        'A (V1 Control)': abs(corr_v1),
        'B (Logarithmic)': abs(corr_log),
        'C (Polar/Trigonometric)': abs(corr_polar),
        'D (Reciprocal Products)': abs(corr_recip),
    }
    best_hypothesis = max(correlations, key=correlations.get)
    best_r = correlations[best_hypothesis]

    print("\n-------------------------------------")
    print(f"🏆 Best Correlation Found: {best_hypothesis} (r = {best_r:.4f})")
    print("-------------------------------------") 
    # Add these lines to experiment_02_comparative_study.py
    # -----------------------------------------------------
    df_clean.to_csv(data_path, index=False)
    print(f"✅ Updated data saved successfully to {data_path} with new columns (z_polar, escape_polar, etc.).")
    # -----------------------------------------------------



if __name__ == "__main__":
    run_comparative_study()
