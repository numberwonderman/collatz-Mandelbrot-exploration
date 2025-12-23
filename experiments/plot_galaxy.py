import pandas as pd
import matplotlib.pyplot as plt
import os

betas = [{"re": 1, "im": 0}, {"re": 2, "im": 0}, {"re": 1, "im": 1}]
scales = [0.001, 0.0001, 0.00001]
fig, axes = plt.subplots(3, 3, figsize=(15, 15), facecolor='black')

for i, b in enumerate(betas):
    for j, s in enumerate(scales):
        ax = axes[i, j]
        ax.set_facecolor('black')
        fname = f"experiments/raw_data_B{b['re']}_i{b['im']}_S{s}.csv"
        
        if os.path.exists(fname):
            df = pd.read_csv(fname)
            # Plot Stable (Cyan) and Unstable (Gold)
            for state, color, alpha in [(0, '#FFD700', 0.2), (1, 'cyan', 0.7)]:
                subset = df[df['Is_Stable'] == state]
                ax.scatter(subset['Final_RE'], subset['Final_IM'], color=color, s=2, alpha=alpha)
            
            # SMART ZOOM: If it's the tiny scale, zoom into the center
            if s == 0.00001:
                ax.set_xlim(-100, 100)
                ax.set_ylim(-100, 100)
            else:
                ax.set_xlim(-3000, 3000)
                ax.set_ylim(-3000, 3000)
        
        ax.set_title(f"Beta: {b['re']}+{b['im']}i | Scale: {s}", color='white')
        ax.tick_params(colors='white')

plt.savefig('experiments/FINAL_V4_GALLERY.png', dpi=300, facecolor='black')
print("✅ V4 Gallery with Smart Zoom generated.")