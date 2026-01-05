import pandas as pd
import matplotlib.pyplot as plt

# Load the "ton of data"
df = pd.read_csv('experiments/GSV1_Figure1_Beta1+1i.csv')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# Plot 1: The Raw Galaxy
ax1.scatter(df['Raw_RE'], df['Raw_IM'], s=10, alpha=0.6, c='blue')
ax1.set_title('Raw Galaxy Sinks (Beta 1+1i)')
ax1.set_xlabel('Real')
ax1.set_ylabel('Imaginary')
ax1.grid(True, which='both', linestyle='--', alpha=0.5)

# Plot 2: The H-C v2 Transformation
ax2.scatter(df['HCv2_RE'], df['HCv2_IM'], s=10, alpha=0.6, c='red')
ax2.set_title('H-C v2 Logarithmic Mapping')
ax2.set_xlabel('H_Real')
ax2.set_ylabel('H_Imaginary')
ax2.grid(True, which='both', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('experiments/GSV1_Figure1_Comparison.png')
print("✅ Visualization saved to experiments/GSV1_Figure1_Comparison.png")