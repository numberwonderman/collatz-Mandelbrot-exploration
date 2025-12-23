import pandas as pd
import matplotlib.pyplot as plt
import os

# Define exact Beta objects to match Node.js
betas = [{"re": 1, "im": 0}, {"re": 2, "im": 0}, {"re": 1, "im": 1}]
scales = [0.001, 0.0001, 0.00001]

fig, axes = plt.subplots(3, 3, figsize=(15, 15), facecolor='black')
plt.subplots_adjust(hspace=0.4, wspace=0.3)

for i, b in enumerate(betas):
    for j, s in enumerate(scales):
        ax = axes[i, j]
        ax.set_facecolor('black')
        
        # Match the new filename format
        filename = f"experiments/raw_data_B{b['re']}_i{b['im']}_S{s}.csv"
        
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            stable = df[df['Is_Stable'] == 1]
            unstable = df[df['Is_Stable'] == 0]
            
            ax.scatter(unstable['Final_RE'], unstable['Final_IM'], color='#FFD700', s=2, alpha=0.3)
            ax.scatter(stable['Final_RE'], stable['Final_IM'], color='cyan', s=2, alpha=0.8)
        
        ax.set_title(f"Beta: {b['re']}+{b['im']}i | Scale: {s}", color='white', fontsize=12)
        ax.tick_params(colors='white')

plt.suptitle("Gaussian Collatz: Stability Mapping (Baseline V3)", color='cyan', fontsize=22)
plt.savefig('experiments/stress_test_gallery_FIXED.png', dpi=300, facecolor='black')
print("✅ FIXED Gallery generated: experiments/stress_test_gallery_FIXED.png")