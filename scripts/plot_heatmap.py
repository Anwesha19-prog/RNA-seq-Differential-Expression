"""
Generate heatmap of top differentially expressed genes
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Snakemake inputs and outputs
counts_file = snakemake.input.counts
metadata_file = snakemake.input.metadata
results_file = snakemake.input.results
output_plot = snakemake.output.plot
padj_threshold = snakemake.params.padj_threshold
top_n_genes = snakemake.params.top_n_genes

print("Generating heatmap of top DE genes...")

# Load data
counts = pd.read_csv(counts_file, index_col=0)
metadata = pd.read_csv(metadata_file, index_col=0)
results = pd.read_csv(results_file, index_col=0)

# Get significant genes
sig_genes = results[results['padj'] < padj_threshold].copy()
print(f"Significant genes (padj < {padj_threshold}): {len(sig_genes)}")

# Select top N genes by adjusted p-value
top_genes = sig_genes.head(top_n_genes).index
print(f"Plotting top {len(top_genes)} genes")

# Get counts for top genes
top_counts = counts.loc[top_genes]

# Log-transform
log_top = np.log2(top_counts + 1)

# Create color mapping for conditions
condition_colors = metadata.loc[log_top.columns, 'condition'].map({
    'control': 'steelblue',
    'covid': 'firebrick'
})

# Create clustermap
g = sns.clustermap(
    log_top,
    col_colors=condition_colors,
    cmap='vlag',
    z_score=0,  # Z-score normalize by row (gene)
    figsize=(12, 10),
    cbar_kws={'label': 'Z-score'},
    dendrogram_ratio=0.15,
    colors_ratio=0.03
)

# Add title
g.fig.suptitle(f'Top {len(top_genes)} Differentially Expressed Genes (padj < {padj_threshold})', 
               fontsize=14, fontweight='bold', y=0.98)

# Save plot
plt.savefig(output_plot, dpi=300, bbox_inches='tight')
plt.close()

print(f"Heatmap saved to {output_plot}")
