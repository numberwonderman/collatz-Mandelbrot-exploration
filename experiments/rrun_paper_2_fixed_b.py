import pandas as pd
import numpy as np
import sys
import os

# --- PATH SETUP ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.collatz_metrics import measure_collatz_behavior
from src.mandelbrot_utils import mandelbrot_escape_time

# ALL MAPPINGS RE-INCLUDED
from src.mapping_functions import (
    map_params_to_complex_v1,     # H-A
    map_params_logarithmic,        # H-B
    map_params_polar,              # H-C (Original)
    map_params_reciprocal_products,# H-D
    map_params_polar_v2,           # H-C v2
    map_params_power_squared       # H-E
)

def run_fixed_b_validation_full():
    data = []
    
    # Keeping high-resolution N=1000 for definitive proof
    NUM_SAMPLES = 1000 
    MAX_PARAM_VALUE = 20 
    CCR_START_COUNT = 500 
    
    print(f"Starting FULL Fixed-B Validation: (B=1, N={NUM_SAMPLES})")
    print("-" * 85)
    
    for i in range(NUM_SAMPLES):
        # A and C are random, B IS FIXED AT 1
        a = np.random.randint(2, MAX_PARAM_VALUE + 1)
        b = 1  
        c = np.random.randint(1, MAX_PARAM_VALUE + 1)
        
        # 1. Measure Collatz Behavior
        col_metrics = measure_collatz_behavior(a, b, c, test_range=(1, CCR_START_COUNT))
        ccr = col_metrics['convergence_rate']
        
        # 2. Map & Measure for ALL Hypotheses
        # Use simple variable names for readability in recording
        et_a = mandelbrot_escape_time(map_params_to_complex_v1(a, b, c))
        et_b = mandelbrot_escape_time(map_params_logarithmic(a, b, c))
        et_c = mandelbrot_escape_time(map_params_polar(a, b, c))
        et_c_v2 = mandelbrot_escape_time(map_params_polar_v2(a, b, c))
        et_d = mandelbrot_escape_time(map_params_reciprocal_products(a, b, c))
        et_e = mandelbrot_escape_time(map_params_power_squared(a, b, c))
        
        # 3. Record Data (Matching original column structure)
        data.append({
            'a_divisor': a, 'b_multiplier': b, 'c_adder': c,
            'collatz_conv_rate': ccr,
            'avg_steps': col_metrics['avg_steps_to_one'],
            'et_h_a': et_a,
            'et_h_b': et_b,
            'et_h_c_orig': et_c, 
            'et_h_c_v2': et_c_v2, 
            'et_h_d': et_d,
            'et_h_e': et_e,
        })
        
        if (i+1) % 100 == 0:
            print(f"Sample {i+1}/{NUM_SAMPLES}: (a,B,c)=({a},{b},{c}) | CCR: {ccr:.3f}")
            
    # Save Results
    df = pd.DataFrame(data)
    output_path = 'TEMP_PAPER2_DATA_FIXED_B.csv' 
    df.to_csv(output_path, index=False)
    
    print("\nValidation Complete. Data saved to:", output_path)
    
    # 4. Final Comparison
    print("\n--- FIXED B CORRELATION LEADERBOARD ---")
    results = {
        "H-A (Linear)": df['collatz_conv_rate'].corr(df['et_h_a']),
        "H-B (Log)":    df['collatz_conv_rate'].corr(df['et_h_b']),
        "H-C (Polar)":  df['collatz_conv_rate'].corr(df['et_h_c_orig']),
        "H-C v2 (LogP)":df['collatz_conv_rate'].corr(df['et_h_c_v2']),
        "H-D (Recip)":  df['collatz_conv_rate'].corr(df['et_h_d']),
        "H-E (Squared)":df['collatz_conv_rate'].corr(df['et_h_e'])
    }
    
    for name, r in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print(f"{name:15}: r = {r:.4f}")

    print("-" * 85)

if __name__ == "__main__":
    run_fixed_b_validation_full()