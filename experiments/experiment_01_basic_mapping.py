import pandas as pd
import numpy as np
import sys
import os

# Adjust path to import modules from src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your core analysis modules
from src.collatz_metrics import measure_collatz_behavior
from src.mandelbrot_utils import is_in_mandelbrot_set, mandelbrot_escape_time
from src.mapping_functions import map_params_to_complex_v1

def run_experiment():
    data = []
    num_samples = 100
    
    print("Starting Experiment 01: Collatz-Mandelbrot Parameter Correlation")
    print("-" * 50)
    
    for i in range(num_samples):
        # 1. Define Random Parameters (A=Divisor, B=Multiplier, C=Adder)
        # Using a restricted range for initial exploration
        a = np.random.randint(2, 11)   # Divisor: 2-10
        b = np.random.randint(1, 11)   # Multiplier: 1-10
        c = np.random.randint(1, 11)   # Adder: 1-10
        
        # 2. Measure Collatz Behavior
        col_metrics = measure_collatz_behavior(a, b, c, test_range=(1, 50))
        
        # 3. Map to Complex Plane
        # z = (b/a) + (c/a)i
        z_point = map_params_to_complex_v1(a, b, c)
        
        # 4. Check Mandelbrot Status
        in_mandelbrot = is_in_mandelbrot_set(z_point)
        escape_speed = mandelbrot_escape_time(z_point)
        
        data.append({
            'a_divisor': a, 
            'b_multiplier': b, 
            'c_adder': c,
            'collatz_conv_rate': col_metrics['convergence_rate'],
            'avg_steps': col_metrics['avg_steps_to_one'],
            'complex_real': z_point.real,
            'complex_imag': z_point.imag,
            'in_mandelbrot': in_mandelbrot,
            'escape_time': escape_speed
        })
        
        print(f"Sample {i+1}/{num_samples}: (a,b,c)=({a},{b},{c}) | Conv Rate: {col_metrics['convergence_rate']:.2f} | Complex: {z_point.real:.2f} + {z_point.imag:.2f}i")
        
    # Save Results
    df = pd.DataFrame(data)
    
    # Ensure the results directory exists
    results_dir = '../data/results'
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, 'experiment_01_results.csv')
    df.to_csv(output_path, index=False)
    
    print("\nExperiment Complete. Data saved to:", output_path)
    
    # Calculate and print the key correlation
    correlation = df['collatz_conv_rate'].corr(df['escape_time'])
    print(f"Primary Result: Correlation between Collatz Convergence Rate and Mandelbrot Escape Time: {correlation:.4f}")
    print("-" * 50)

if __name__ == "__main__":
    run_experiment()
