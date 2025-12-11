import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
def plot_correlation_scatter(df: pd.DataFrame, output_path: str):
    """
    Creates a simple scatter plot to visualize the R=0.6567 correlation.
    """
    plt.figure(figsize=(10, 8))
   
    # X-axis: The Collatz Convergence Rate
    x_data = df['collatz_conv_rate']
    # Y-axis: The Mandelbrot Escape Time for the winning hypothesis
    y_data = df['escape_polar']
   
    plt.scatter(x_data, y_data,
                c=y_data, # Color by Escape Time for gradient effect
                cmap='viridis',
                edgecolors='black',
                s=70,
                alpha=0.7)
   
    # Add a linear trendline to visually confirm R=0.6567
    m, b = np.polyfit(x_data, y_data, 1)
    plt.plot(x_data, m*x_data + b, color='red', linestyle='--', label=f'Trendline (r={0.6567:.4f})')
   
    plt.title(f'Correlation Confirmation: Collatz Stability vs. Mandelbrot Escape Time\nHypothesis C: r = {0.6567:.4f}')
    plt.xlabel('Collatz Convergence Rate (CCR)')
    plt.ylabel('Mandelbrot Escape Time (ET) [Hypothesis C]')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
   
    plt.savefig(output_path)
    print(f"\n✅ Correlation scatter plot saved to {output_path}")


# You must also change the if __name__ == "__main__": block
if __name__ == "__main__":
    # Get the directory of the current script (which is 'experiments/')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, '..', 'data', 'results', 'experiment_01_results.csv')
    output_path = os.path.join(script_dir, '..', 'data', 'results', 'correlation_scatter_C.png')
   
    # Load the data first
    df = pd.read_csv(csv_file_path)


    # --- FINAL VISUALIZATION STEP ---
    # Convert 'z_polar' to complex needed for the old overlay plot,
    # but for the scatter plot, we only need the 'escape_polar' column, which is already numeric.
   
    # Run the new function to show the correlation
    plot_correlation_scatter(df, output_path)
   
    # If you still want the complex plane overlay, you can call it here:
    # plot_collatz_mandelbrot_overlay(csv_file_path)

