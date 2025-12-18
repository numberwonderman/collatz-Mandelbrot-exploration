import pandas as pd
import numpy as np
import sys
import os

# --- FINAL PATH FIX ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import core analysis modules
from src.collatz_metrics import measure_collatz_behavior
from src.mandelbrot_utils import mandelbrot_escape_time

# 🚨 DIRECT IMPORTS from src/mapping_functions.py
from src.mapping_functions import map_params_to_complex_v1  # Hypothesis A
from src.mapping_functions import map_params_logarithmic  # Hypothesis B
from src.mapping_functions import map_params_polar  # Hypothesis C (Original)
from src.mapping_functions import map_params_reciprocal_products  # Hypothesis D
from src.mapping_functions import map_params_polar_v2 # Refinement (H-C v2)
from src.mapping_functions import map_params_power_squared # Hypothesis E

def run_experiment_paper_2():
    data = []
    
    # --- PAPER 2 SCOPE ---
    NUM_SAMPLES = 1000 
    MAX_PARAM_VALUE = 20 
    CCR_START_COUNT = 500 
    
    print("Starting Experiment 02: Final Test (N=1000, N_start=500)")
    print("-" * 85)
    
    for i in range(NUM_SAMPLES):
        # 1. Define Random Parameters (A, B, C)
        a = np.random.randint(2, MAX_PARAM_VALUE + 1)
        b = np.random.randint(1, MAX_PARAM_VALUE + 1)
        c = np.random.randint(1, MAX_PARAM_VALUE + 1)
        
        # 2. Measure Collatz Behavior
        col_metrics = measure_collatz_behavior(a, b, c, test_range=(1, CCR_START_COUNT))
        
        # 3. Map to Complex Plane & Measure ET (for all hypotheses)
        
        # H-A (V1 Control)
        z_a = map_params_to_complex_v1(a, b, c)
        et_a = mandelbrot_escape_time(z_a)
        
        # H-B (Logarithmic)
        z_b = map_params_logarithmic(a, b, c)
        et_b = mandelbrot_escape_time(z_b)
        
        # H-C Original 
        z_c_orig = map_params_polar(a, b, c) 
        et_c_orig = mandelbrot_escape_time(z_c_orig)
        
        # H-C Refinement (v2)
        z_c_v2 = map_params_polar_v2(a, b, c) 
        et_c_v2 = mandelbrot_escape_time(z_c_v2) 
        
        # H-D (Reciprocal Products)
        z_d = map_params_reciprocal_products(a, b, c)
        et_d = mandelbrot_escape_time(z_d)
        
        # --- Hypothesis E: B/A Dominance (Squared) ---
        z_e = map_params_power_squared(a, b, c)
        et_e = mandelbrot_escape_time(z_e)
        
        # 4. Record Data
        data.append({
            'a_divisor': a, 'b_multiplier': b, 'c_adder': c,
            'collatz_conv_rate': col_metrics['convergence_rate'],
            'avg_steps': col_metrics['avg_steps_to_one'],
            
            'et_h_a': et_a,
            'et_h_b': et_b,
            'et_h_d': et_d,
            'et_h_c_orig': et_c_orig, 
            'et_h_c_v2': et_c_v2, 
            
            # --- NEW HYPOTHESIS E COLUMN ---
            'et_h_e': et_e,
        })
        
        if (i+1) % 100 == 0:
            print(f"Sample {i+1}/{NUM_SAMPLES}: (a,b,c)=({a},{b},{c}) | CCR: {col_metrics['convergence_rate']:.3f} | H-E Real/Imag: {z_e.real:.4f} + {z_e.imag:.4f}i")
            
    # Save Results
    df = pd.DataFrame(data)
    
    # --- SAFE SAVE PATH ---
    output_path = 'TEMP_PAPER2_DATA_FINAL_TESTS.csv' # New safe name
    df.to_csv(output_path, index=False)
    
    print("\nExperiment Complete. Data saved to:", output_path)
    
    # 5. Calculate and print FINAL correlations
    print("\n--- Final Correlation Results (Hypothesis E Test) ---")
    
    # Calculate all correlations
    corr_a = df['collatz_conv_rate'].corr(df['et_h_a'])
    corr_c_orig = df['collatz_conv_rate'].corr(df['et_h_c_orig'])
    corr_c_v2 = df['collatz_conv_rate'].corr(df['et_h_c_v2'])
    corr_e = df['collatz_conv_rate'].corr(df['et_h_e'])
    
    # Print the most important results
    print(f"H-A (Linear B/A): r = {corr_a:.4f} (Baseline Winner)")
    print(f"H-C Original (Polar): r = {corr_c_orig:.4f}")
    print(f"H-C v2 (Logarithmic): r = {corr_c_v2:.4f} (Confirmed Dead End)")
    print(f"H-E (B/A Squared): r = {corr_e:.4f} (The Final Test)")

    print("-" * 85)

if __name__ == "__main__":
    run_experiment_paper_2()