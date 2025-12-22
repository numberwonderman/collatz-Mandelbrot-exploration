import pandas as pd
import matplotlib.pyplot as plt

# Load your 1000-point scan results
file_path = 'experiments/galaxy_scan_1000.csv'
df = pd.read_csv(file_path)

# --- RAW PLOT (NO H-C v2 MAPPING) ---
# We use the raw Final_RE and Final_IM directly from your JS Engine
raw_x = df['Final_RE']
raw_y = df['Final_IM']

plt.figure(figsize=(10, 10), facecolor='black')
ax = plt.gca()
ax.set_facecolor('black')

# Plot the raw points in gold/yellow to stay consistent with the "Galaxy" theme
plt.scatter(raw_x, raw_y, color='#FFD700', s=2, alpha=0.7, label='Raw Gaussian Sinks')

# Formatting for the "Raw Galaxy"
plt.title("Raw Galaxy: Unmapped Gaussian Sinks", color='white', fontsize=15)
plt.xlabel("Real Axis (A)", color='white')
plt.ylabel("Imaginary Axis (B)", color='white')
plt.tick_params(colors='white')
plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

# Save as a separate file as requested
plt.savefig('experiments/raw_galaxy.png', dpi=300)
print("✅ Raw Galaxy image saved to experiments/raw_galaxy.png")
plt.show()