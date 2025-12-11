import pandas as pd
from scipy.stats import pearsonr
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# The plotting function is now internalized in generate_complex_plot, so we don't need the old import from visualization.py.


# --- UTILITY FUNCTIONS ---
def calculate_mandelbrot_escape_time(c: complex, max_iter: int = 100, bailout: float = 2.0) -> int:
    """Calculates the number of iterations before the sequence diverges."""
    z = 0 + 0j
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > bailout:
            return i
    return max_iter 

# --- NEW PLOTTING FUNCTION (Centralized Visualization Logic) ---
def generate_complex_plot(
    df: pd.DataFrame, 
    z_column: str, 
    ccr_column: str, 
    r_value: float, 
    title: str, 
    fig_id: str, 
    script_dir: str
):
    """
    Generates the Complex Plane plot with Mandelbrot overlay for a specific hypothesis.
    """
    
    # 1. Generate Mandelbrot Background 
    h, w = 400, 400
    y, x = np.ogrid[-1.5:1.5:h*1j, -2.5:1.5:w*1j]
    c_grid = x + y*1j
    z = c_grid
    div_time = h + np.zeros(z.shape, dtype=int)

    for i in range(50):
        z = z**2 + c_grid
        diverge = z * np.conj(z) > 4 # 2**2 = 4
        div_now = diverge & (div_time == h) 
        div_time[div_now] = i 
        z[diverge] = 2 

    # 2. Plotting Setup
    plt.figure(figsize=(12, 10))
    
    # Draw Mandelbrot (in grayscale)
    plt.imshow(div_time, extent=[-2.5, 1.5, -1.5, 1.5], cmap='gray_r', alpha=0.6)
    
    # Overlay Collatz Points 
    sc = plt.scatter(
        df[z_column].apply(lambda z: z.real), 
        df[z_column].apply(lambda z: z.imag), 
        c=df[ccr_column], 
        cmap='coolwarm', 
        edgecolors='black', 
        linewidths=0.5,
        s=100,
        label=f'Points (r={r_value:.4f})'
    )
    
    # Titles and Labels
    plt.colorbar(sc, label='Collatz Convergence Rate (CCR)')
    plt.title(title, fontsize=14)
    plt.xlabel('Real (c)')
    plt.ylabel('Imaginary (c)')
    plt.text(0.05, 0.95, 
             f'Pearson Correlation: r = {r_value:.4f}', 
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
             
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # 3. Highlight Standard Collatz (A=2, B=3, C=1) - Coordinates are mapping-dependent
    real_c, imag_c = None, None # Initialize location variables

    if fig_id == 'A1':
        # Hypothesis A (V1 Mapping): z = 3/2 + 1/2 i = (1.5, 0.5)
        real_c, imag_c = 1.5, 0.5
    elif fig_id == 'A2':
        # Hypothesis B (Logarithmic Mapping): z = (ln(1.5)-1) + (ln(0.5)-1)i
        real_c = np.log(1.5) - 1
        imag_c = np.log(0.5) - 1
    elif fig_id == 'A3':
        # Hypothesis D (Reciprocal Mapping): z = 1/3 + 1/2 i
        real_c = 1 / 3
        imag_c = 0.5
    elif fig_id == 'C-ALT':
        # Hypothesis C (Polar Mapping): z = (6/sqrt(10)) + (2/sqrt(10)) i
        real_c = 6 / np.sqrt(10)
        imag_c = 2 / np.sqrt(10)
    
    if real_c is not None:
        plt.scatter([real_c], [imag_c], color='yellow', marker='*', s=350, edgecolors='black', label='Standard Collatz (A=2, B=3, C=1)')

    
    plt.legend()
    plt.tight_layout()
    
    # 4. Save the figure
    save_path = os.path.join(script_dir, f'Appendix_Figure_{fig_id.replace(" ", "_")}.png') 
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"✅ Generated Appendix Figure {fig_id} and saved to {save_path}")


# --- MAPPING FUNCTIONS (Embedded - ORIGINAL FORMULAS) ---

def map_params_to_complex_v1(A: int, B: int, C: int) -> complex:
    """Hypothesis A / V1 Mapping: z = (B/A) + (C/A)i"""
    if A == 0:
        raise ValueError("Divisor 'A' cannot be zero.") 
    return complex(B / A, C / A)

def map_params_logarithmic(A: int, B: int, C: int) -> complex:
    """Hypothesis B: Logarithmic Mapping"""
    real_part = np.log(B / A) - 1.0 
    imag_part = np.log(C / A) - 1.0
    return complex(real_part, imag_part)

def map_params_polar(A: int, B: int, C: int) -> complex:
    """Hypothesis C: Polar/Trigonometric Mapping"""
    r = (B + C) / A
    theta = np.arctan(C / B) 
    real_part = r * np.cos(theta)
    imag_part = r * np.sin(theta)
    return complex(real_part, imag_part)

def map_params_reciprocal_products(A: int, B: int, C: int) -> complex:
    """Hypothesis D: Reciprocal Products Mapping"""
    return (1 / B) + (1 / (A * C)) * 1j


# --- MAIN EXECUTION FUNCTION ---
def run_comparative_study():
    """
    Loads Experiment 01 data, runs the correlation test, and generates all required plots.
    """
    print("--- SCRIPT STARTED. CHECKING ENVIRONMENT ---")

    data_path = 'data/results/experiment_01_results.csv' 

    try:
        df_clean = pd.read_csv(data_path)
        print(f"✅ Data loaded successfully from {data_path}. Total samples: {len(df_clean)}")
    except FileNotFoundError as e:
        absolute_check_path = os.path.abspath(data_path)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"❌ FATAL ERROR: Data file not found. Please ensure the file is at this exact location: {absolute_check_path}")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        raise e 

    # --- 2. APPLY MAPPING HYPOTHESES & CALCULATE ET ---
    print("\nApplying four different Collatz-to-Mandelbrot mappings and calculating Escape Times...")
    
    MAX_ITER = 100 
    
    df_clean['z_v1'] = df_clean.apply(lambda row: map_params_to_complex_v1(row['a_divisor'], row['b_multiplier'], row['c_adder']), axis=1)
    df_clean['z_log'] = df_clean.apply(lambda row: map_params_logarithmic(row['a_divisor'], row['b_multiplier'], row['c_adder']), axis=1)
    df_clean['z_polar'] = df_clean.apply(lambda row: map_params_polar(row['a_divisor'], row['b_multiplier'], row['c_adder']), axis=1)
    df_clean['z_reciprocal'] = df_clean.apply(lambda row: map_params_reciprocal_products(row['a_divisor'], row['b_multiplier'], row['c_adder']), axis=1)

    df_clean['escape_v1'] = df_clean['z_v1'].apply(lambda c: calculate_mandelbrot_escape_time(c, max_iter=MAX_ITER))
    df_clean['escape_log'] = df_clean['z_log'].apply(lambda c: calculate_mandelbrot_escape_time(c, max_iter=MAX_ITER))
    df_clean['escape_polar'] = df_clean['z_polar'].apply(lambda c: calculate_mandelbrot_escape_time(c, max_iter=MAX_ITER))
    df_clean['escape_reciprocal'] = df_clean['z_reciprocal'].apply(lambda c: calculate_mandelbrot_escape_time(c, max_iter=MAX_ITER))

    # --- 3. CALCULATE CORRELATIONS ---
    print("\n--- Comparative Correlation Results ---")
    
    valid_data_v1 = df_clean.dropna(subset=['escape_v1'])
    valid_data_log = df_clean.dropna(subset=['escape_log'])
    valid_data_recip = df_clean.dropna(subset=['escape_reciprocal'])
    
    corr_v1, _ = pearsonr(valid_data_v1['collatz_conv_rate'], valid_data_v1['escape_v1'])
    print(f"Hypothesis A (V1 Control):         r = {corr_v1:.4f}")

    corr_log, _ = pearsonr(valid_data_log['collatz_conv_rate'], valid_data_log['escape_log'])
    print(f"Hypothesis B (Logarithmic):        r = {corr_log:.4f}")

    corr_polar, _ = pearsonr(df_clean['collatz_conv_rate'], df_clean['escape_polar'])
    print(f"Hypothesis C (Polar/Trigonometric): r = {corr_polar:.4f}")

    corr_recip, _ = pearsonr(valid_data_recip['collatz_conv_rate'], valid_data_recip['escape_reciprocal'])
    print(f"Hypothesis D (Reciprocal Products): r = {corr_recip:.4f}")
    
    # --- 4. GENERATE VISUALIZATIONS (A1, A2, A3, C-ALT) ---
    print("\nGenerating Figures (A1, A2, A3) and Test Figure C-ALT...") 
    
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # *** FIGURE C-ALT PLOT (Main Finding/Visualization Test) ***
    generate_complex_plot(
        df=df_clean, z_column='z_polar', ccr_column='collatz_conv_rate', 
        r_value=corr_polar, 
        title='Figure C-ALT: Hypothesis C (Polar Mapping) Visualization Test', 
        fig_id='C-ALT', 
        script_dir=script_dir
    )
    
    # Hypothesis A (V1 Control) - Figure A1
    generate_complex_plot(
        df=valid_data_v1, z_column='z_v1', ccr_column='collatz_conv_rate', 
        r_value=corr_v1, title='Appendix Figure A1: Hypothesis A (V1 Control - V1 Mapping)', fig_id='A1', script_dir=script_dir
    )
    
    # Hypothesis B (Logarithmic) - Figure A2
    generate_complex_plot(
        df=valid_data_log, z_column='z_log', ccr_column='collatz_conv_rate', 
        r_value=corr_log, title='Appendix Figure A2: Hypothesis B (Logarithmic Mapping)', fig_id='A2', script_dir=script_dir
    )

    # Hypothesis D (Reciprocal Products) - Figure A3
    generate_complex_plot(
        df=valid_data_recip, z_column='z_reciprocal', ccr_column='collatz_conv_rate', 
        r_value=corr_recip, title='Appendix Figure A3: Hypothesis D (Reciprocal Products Mapping)', fig_id='A3', script_dir=script_dir
    )
    print("✅ All required Figures generated and saved to the 'experiments' folder.")


if __name__ == "__main__":
    run_comparative_study()