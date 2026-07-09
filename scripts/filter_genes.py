"""
Filter low-count genes from the count matrix
"""

import pandas as pd

# Snakemake inputs and outputs
counts_file = snakemake.input.counts
output_file = snakemake.output.counts_filtered
min_count = snakemake.params.min_count

print(f"Filtering genes with total count < {min_count}...")

# Load counts
counts = pd.read_csv(counts_file, index_col=0)

print(f"Before filtering: {counts.shape[0]} genes")

# Filter genes
keep = counts.sum(axis=1) >= min_count
counts_filtered = counts.loc[keep].copy()

print(f"After filtering: {counts_filtered.shape[0]} genes")
print(f"Removed: {counts.shape[0] - counts_filtered.shape[0]} genes")

# Save filtered counts
counts_filtered.to_csv(output_file)

print("Gene filtering complete!")
