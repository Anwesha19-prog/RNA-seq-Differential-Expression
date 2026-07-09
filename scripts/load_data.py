"""
Load and process raw count data and metadata from GEO files
"""

import re
import numpy as np
import pandas as pd

# Snakemake inputs and outputs
counts_file = snakemake.input.counts
series_matrix_file = snakemake.input.series_matrix
output_counts = snakemake.output.counts
output_metadata = snakemake.output.metadata

print("Loading raw count data...")

# Load raw counts
# try:
#     counts_df = pd.read_csv(counts_file, sep='\t', header=0, index_col=0)
# except Exception:
counts_df = pd.read_csv(counts_file, sep=r'\s+', header=0, index_col=0)

# Convert to integer counts (pyDESeq2 requirement)
counts_df = (
    counts_df.apply(pd.to_numeric, errors='coerce')
            .fillna(0)
            .astype(int)
)

print(f"Loaded counts: {counts_df.shape[0]} genes x {counts_df.shape[1]} samples")

# Parse metadata from series matrix file
print("Parsing metadata from series matrix...")

with open(series_matrix_file, 'r', errors='replace') as f:
    lines = f.readlines()

def get_field_values(field_name: str):
    """Extract tab-separated values for a GEO series-matrix field."""
    for line in lines:
        if line.startswith(field_name + '\t'):
            vals = line.strip().split('\t')[1:]
            return [v.strip().strip('"') for v in vals]
    return None

# Get sample titles
sample_titles = get_field_values('!Sample_title')
if sample_titles is None:
    raise ValueError('Could not find !Sample_title in series matrix')

# Collect all characteristics rows
char_lines = [ln for ln in lines if ln.startswith('!Sample_characteristics_ch1\t')]
char_rows = []
for ln in char_lines:
    vals = [v.strip().strip('"') for v in ln.strip().split('\t')[1:]]
    char_rows.append(vals)
char_rows = np.array(char_rows, dtype=object)

# Create metadata DataFrame
meta = pd.DataFrame(index=sample_titles)
meta.index.name = 'sample'

# Combine all characteristics into one blob per sample
char_blob = pd.Series(
    [' | '.join(char_rows[:, i].astype(str)) for i in range(char_rows.shape[1])],
    index=meta.index
)

def to_numeric_clean(x: pd.Series) -> pd.Series:
    """Convert messy numeric fields to floats."""
    x = x.astype(str).str.strip()
    x = x.replace({'Unknown': np.nan, 'N/A': np.nan})
    x = x.str.replace(r'\+$', '', regex=True)  # 90+ -> 90
    return pd.to_numeric(x, errors='coerce')

# Extract fields using regex
meta['positivity'] = char_blob.str.extract(r'sars-cov-2 positivity:\s*([a-z]+)', expand=False)
meta['n1_ct'] = char_blob.str.extract(r'n1_ct:\s*([0-9.]+|Unknown|N/A)', expand=False)
meta['age'] = char_blob.str.extract(r'age:\s*([0-9+]+|Unknown)', expand=False)
meta['gender'] = char_blob.str.extract(r'gender:\s*([MF]|not collected)', expand=False)
meta['batch'] = char_blob.str.extract(r'sequencing_batch:\s*([A-Z])', expand=False)

# Clean and convert types
meta['condition'] = meta['positivity'].map({'pos': 'covid', 'neg': 'control'})
meta['n1_ct'] = to_numeric_clean(meta['n1_ct'])
meta['age'] = to_numeric_clean(meta['age'])
meta['gender'] = meta['gender'].replace({'not collected': np.nan})

# Convert to categorical (required for DESeq2)
meta['condition'] = meta['condition'].astype('category')
meta['gender'] = meta['gender'].astype('category')
meta['batch'] = meta['batch'].astype('category')

# Keep only samples with condition labels
meta = meta.dropna(subset=['condition']).copy()

print(f"\nBefore alignment:")
print(f"  Count matrix columns: {len(counts_df.columns)}")
print(f"  Metadata rows: {len(meta)}")
print(f"  First 5 count columns: {list(counts_df.columns[:5])}")
print(f"  First 5 metadata indices: {list(meta.index[:5])}")

# Align counts and metadata (keep only common samples)
# Try exact match first
common_samples = meta.index.intersection(counts_df.columns)

# If no exact matches, try case-insensitive and whitespace-trimmed matching
if len(common_samples) == 0:
    print("\nNo exact sample name matches found. Trying flexible matching...")
    
    # Create mapping dictionaries with normalized names
    count_cols_normalized = {col.strip().lower(): col for col in counts_df.columns}
    meta_idx_normalized = {idx.strip().lower(): idx for idx in meta.index}
    
    # Find common normalized names
    common_normalized = set(count_cols_normalized.keys()).intersection(meta_idx_normalized.keys())
    
    if len(common_normalized) > 0:
        print(f"Found {len(common_normalized)} samples with flexible matching")
        # Rename columns in counts to match metadata
        rename_map = {count_cols_normalized[norm]: meta_idx_normalized[norm] 
                     for norm in common_normalized}
        counts_df = counts_df.rename(columns=rename_map)
        common_samples = list(rename_map.values())
    else:
        raise ValueError(
            f"No matching samples found between count matrix and metadata!\n"
            f"Count matrix has {len(counts_df.columns)} samples\n"
            f"Metadata has {len(meta)} samples\n"
            f"Please check that sample names match between files."
        )

meta = meta.loc[common_samples].copy()
counts_df = counts_df.loc[:, common_samples].copy()

print(f"\nFinal data: {counts_df.shape[0]} genes x {counts_df.shape[1]} samples")
print(f"Condition distribution:\n{meta['condition'].value_counts()}")

# Save outputs
counts_df.to_csv(output_counts)
meta.to_csv(output_metadata)

print("Data loading complete!")
