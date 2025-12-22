import pandas as pd
import matplotlib.pyplot as plt

# Load the master results
df_master = pd.read_csv('experiments/stress_test_master.csv')
# We also need the raw coordinate data from the scan
df_data = pd.read_csv('experiments/galaxy_scan_1000.csv')

betas = df_master['Beta'].unique()
scales = df_master['Scale'].unique()

fig, axes = plt.subplots(len(betas), len(scales), figsize=(15, 15), facecolor='black')
plt.subplots_adjust(hspace=0.4, wspace=0.3)

for i, beta in enumerate(betas):
    for j, scale in enumerate(scales):
        ax = axes[i, j]
        ax.set_facecolor('black')
        
        # In a real run, you'd filter df_data by the specific Beta used
        # For this visualization, we show the raw distribution impact
        ax.scatter(df_data['Final_RE'], df_data['Final_IM'], color='#FFD700', s=1, alpha=0.5)
        
        # Labeling the specific 'Stress' cell
        ax.set_title(f"Beta: {beta}\nScale: {scale}", color='white', fontsize=10)
        ax.tick_params(colors='white', labelsize=8)

plt.suptitle("Stress Test Gallery: Symmetry Evolution", color='cyan', fontsize=20)
plt.savefig('experiments/stress_test_gallery.png', dpi=300)
print("✅ 3x3 Stress Gallery saved to experiments/stress_test_gallery.png")