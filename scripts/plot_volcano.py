"""
Generate volcano plot from differential expression results
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Snakemake inputs and outputs
results_file = snakemake.input.results
output_plot = snakemake.output.plot
padj_threshold = snakemake.params.padj_threshold

print("Generating volcano plot...")

# Load results
results = pd.read_csv(results_file, index_col=0)

# Prepare data for plotting
plot_df = results.copy()
plot_df['padj_clipped'] = plot_df['padj'].clip(lower=1e-300)
plot_df['significant'] = plot_df['padj'] < padj_threshold

# Create volcano plot
plt.figure(figsize=(8, 6))
plt.scatter(
    plot_df['log2FoldChange'],
    -np.log10(plot_df['padj_clipped']),
    c=plot_df['significant'],
    cmap='bwr',
    alpha=0.6,
    s=10,
)

plt.xlabel('log2 Fold Change', fontsize=12)
plt.ylabel('-log10 Adjusted P-value', fontsize=12)
plt.title('Volcano Plot: COVID vs Control', fontsize=14, fontweight='bold')

# Add threshold lines
plt.axhline(y=-np.log10(padj_threshold), color='gray', linestyle='--', linewidth=1, alpha=0.5)
plt.axvline(x=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)

# Add legend
n_sig = plot_df['significant'].sum()
plt.text(0.02, 0.98, f'Significant genes: {n_sig}', 
         transform=plt.gca().transAxes, 
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig(output_plot, dpi=300, bbox_inches='tight')
plt.close()

print(f"Volcano plot saved to {output_plot}")
print(f"Significant genes (padj < {padj_threshold}): {n_sig}")
