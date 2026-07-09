"""
Generate PCA plot from filtered count data
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Snakemake inputs and outputs
counts_file = snakemake.input.counts
metadata_file = snakemake.input.metadata
output_plot = snakemake.output.plot

print("Generating PCA plot...")

# Load data
counts = pd.read_csv(counts_file, index_col=0)
metadata = pd.read_csv(metadata_file, index_col=0)

# Log-transform counts (samples x genes)
log_counts = np.log2(counts + 1).T

# Perform PCA
pca = PCA(n_components=2)
pc = pca.fit_transform(log_counts)

# Create PCA plot
plt.figure(figsize=(8, 6))

# Plot each condition with different colors
conditions = metadata['condition'].unique()
colors = {'covid': 'firebrick', 'control': 'steelblue'}

for cond in conditions:
    idx = (metadata['condition'] == cond).to_numpy()
    plt.scatter(
        pc[idx, 0], 
        pc[idx, 1], 
        label=str(cond),
        alpha=0.7,
        s=60,
        c=colors.get(cond, 'gray'),
        edgecolors='black',
        linewidth=0.5
    )

plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', fontsize=12)
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', fontsize=12)
plt.title('PCA of Samples (log2 counts + 1)', fontsize=14, fontweight='bold')
plt.legend(title='Condition', fontsize=10)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_plot, dpi=300, bbox_inches='tight')
plt.close()

print(f"PCA plot saved to {output_plot}")
print(f"PC1 variance explained: {pca.explained_variance_ratio_[0]*100:.2f}%")
print(f"PC2 variance explained: {pca.explained_variance_ratio_[1]*100:.2f}%")
