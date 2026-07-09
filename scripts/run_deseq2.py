"""
Run differential expression analysis using pyDESeq2
"""

import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# Snakemake inputs and outputs
counts_file = snakemake.input.counts
metadata_file = snakemake.input.metadata
output_file = snakemake.output.results
design = snakemake.params.design

print("Running differential expression analysis with pyDESeq2...")

# Load data
counts = pd.read_csv(counts_file, index_col=0)
metadata = pd.read_csv(metadata_file, index_col=0)

# # Ensure categorical types
# metadata['condition'] = metadata['condition'].astype('category')
# if 'batch' in metadata.columns:
#     metadata['batch'] = metadata['batch'].astype('category')

# Ensure categorical types with explicit reference levels
from pandas.api.types import CategoricalDtype

# Set condition as categorical with 'control' as reference (first category)
condition_type = CategoricalDtype(categories=['control', 'covid'], ordered=False)
metadata['condition'] = metadata['condition'].astype(condition_type)

# Set batch as categorical if present
if 'batch' in metadata.columns:
    batch_categories = sorted(metadata['batch'].dropna().unique())
    batch_type = CategoricalDtype(categories=batch_categories, ordered=False)
    metadata['batch'] = metadata['batch'].astype(batch_type)


print(f"Design formula: {design}")
print(f"Counts shape: {counts.shape}")
print(f"Metadata shape: {metadata.shape}")

# pyDESeq2 expects counts with samples as rows
counts_T = counts.T

# Create DESeq2 dataset
dds = DeseqDataSet(
    counts=counts_T,
    metadata=metadata,
    design=design,
    refit_cooks=True,
)

# Run DESeq2 analysis
print("Running DESeq2...")
dds.deseq2()

# Get differential expression statistics
print("Computing statistics for contrast: condition covid vs control")
stats = DeseqStats(dds, contrast=('condition', 'covid', 'control'))
stats.summary()

# Get results
results = stats.results_df.sort_values('padj')

# Print summary
n_sig = (results['padj'] < 0.05).sum()
print(f"\nDifferentially expressed genes (padj < 0.05): {n_sig}")
print(f"Total genes tested: {len(results)}")

# Save results
results.to_csv(output_file)

print("Differential expression analysis complete!")
