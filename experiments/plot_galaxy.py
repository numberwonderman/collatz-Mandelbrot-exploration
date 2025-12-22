import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def plot_collatz_galaxy(csv_path, scale=0.0001):
    # 1. Load the Data
    if not os.path.exists(csv_path):
        print(f"Error: CSV not found at {csv_path}")
        return
    
    df = pd.read_csv(csv_path)
    
    # 2. Setup Mandelbrot Background
    # We use a slightly wider view to see the whole set
    h, w = 1000, 1000
    y, x = np.ogrid[-1.5:1.5:h*1j, -2.0:1.0:w*1j]
    c = x + y*1j
    z = c
    mandel_set = np.zeros(z.shape, dtype=bool)

    # Iteration loop to define the set boundary
    for i in range(50):
        z = z**2 + c
        mandel_set = np.abs(z) <= 2

  # 3. Plotting
    plt.figure(figsize=(12, 12), facecolor='black')
    
    # Background: Mandelbrot Set
    plt.imshow(mandel_set, extent=[-2.0, 1.0, -1.5, 1.5], cmap='magma', alpha=0.3)
    
    # Ensure these are aligned with the 'plt' commands
   # Ensure RE and IM are fully capitalized to match your CSV headers
    real_coords = df['Final_RE'] * scale
    imag_coords = df['Final_IM'] * scale
    
    # Now call scatter with the clean variables
    plt.scatter(
        real_coords, 
        imag_coords,
        color='cyan', 
        s=2, 
        alpha=0.4, 
        label='Gaussian Sinks'
    )

    plt.title(f'Galaxy Scan Overlay\nScale: {scale} | Residency: 91.8%', color='white', fontsize=15)
    plt.axis('off')
    
    # Save output
    output_png = csv_path.replace('.csv', '_plot.png')
    plt.savefig(output_png, dpi=300, facecolor='black', bbox_inches='tight')
    print(f"Visualization complete: {output_png}")

if __name__ == "__main__":
    path = "/workspaces/collatz-Mandelbrot-exploration/experiments/galaxy_scan_1000.csv"
    plot_collatz_galaxy(path)