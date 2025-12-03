import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def plot_collatz_mandelbrot_overlay(csv_path: str):
    """
    Plots experimental (a,b,c) points over the Mandelbrot set.
    Color of points = Collatz Convergence Rate.
    """
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}. Run the experiment first!")
        return
        
    # 1. Generate Mandelbrot Background (Low-res for speed)
    h, w = 400, 400
    y, x = np.ogrid[-1.5:1.5:h*1j, -2.5:1.5:w*1j]
    c = x + y*1j
    z = c
    div_time = h + np.zeros(z.shape, dtype=int)

    for i in range(50): # Reduced iterations for quick background plot
        z = z**2 + c
        diverge = z * np.conj(z) > 2**2            
        div_now = diverge & (div_time == h)  
        div_time[div_now] = i                  
        z[diverge] = 2                        

    # 2. Load Experiment Data
    df = pd.read_csv(csv_path)
    
    # 3. Plotting
    plt.figure(figsize=(12, 10))
    
    # Draw Mandelbrot (in grayscale)
    plt.imshow(div_time, extent=[-2.5, 1.5, -1.5, 1.5], cmap='gray_r', alpha=0.6)
    
    # Overlay Collatz Points
    # X = Real (b/a), Y = Imag (c/a)
    sc = plt.scatter(
        df['complex_real'], 
        df['complex_imag'], 
        c=df['collatz_conv_rate'], 
        cmap='coolwarm', # Blue=Low Convergence, Red=High Convergence
        edgecolors='black', 
        linewidths=0.5,
        s=100,
        label='Param Sets (a,b,c)'
    )
    
    plt.colorbar(sc, label='Collatz Convergence Rate (1.0 = All Converge)')
    plt.title('Collatz Parameters mapped to Mandelbrot Space\nMapping: z = (Multiplier/Divisor) + (Adder/Divisor)i')
    plt.xlabel('Real (Multiplier / Divisor)')
    plt.ylabel('Imaginary (Adder / Divisor)')
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Highlight Standard Collatz (a=2, b=3, c=1)
    # Real=3/2 = 1.5, Imag=1/2 = 0.5
    plt.scatter([1.5], [0.5], color='yellow', marker='*', s=350, edgecolors='black', label='Standard Collatz (3,1,2)')
    
    plt.legend()
    plt.tight_layout()
    
    # Save the plot
    output_dir = os.path.dirname(csv_path)
    save_path = os.path.join(output_dir, 'collatz_mandelbrot_overlay.png')
    plt.savefig(save_path)
    print(f"\nVisualization saved to {save_path}")
    # plt.show() # Uncomment if you want the plot to appear immediately
    
if __name__ == "__main__":
    # Get the directory of the current script (which is 'experiments/')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go up one level to the project root, then down to 'data/results'
    csv_file_path = os.path.join(script_dir, '..', 'data', 'results', 'experiment_01_results.csv')
    
    plot_collatz_mandelbrot_overlay(csv_file_path)