# RNA-seq Differential Expression — GSE152075 (POS vs NEG)

## Overview
This project demonstrates an end-to-end **RNA-seq differential expression (DE)** workflow in Python using **pydeseq2** (DESeq2-like negative binomial modeling). The notebook covers:

- loading and validating a raw **count matrix**
- constructing **metadata** from GEO annotations (Series Matrix)
- running DE with an explicit contrast
- QC/visualization (PCA, clustered heatmap)
- exporting results for downstream interpretation

## Dataset
- GEO: **GSE152075**
- Data type: nasopharyngeal swab RNA-seq (gene-level counts)
- Inputs:
  - `GSE152075_raw_counts_GEO.txt(.gz)` — raw integer counts
  - `GSE152075_series_matrix.txt` — sample annotations (condition, age, sex, Ct, sequencing batch)

### Metadata fields used
From the series matrix, the notebook extracts:
- `condition` (pos/neg → covid/control)
- `n1_ct` (Ct value; proxy for viral load)
- `age`
- `gender`
- `sequencing_batch`

## Methods
### Differential expression (pydeseq2)
- Count-based modeling using a negative binomial GLM
- Multiple testing correction (FDR / adjusted p-values)
- Results table extraction via `DeseqStats(...).results_df`

### QC and visualization
- PCA to inspect global sample structure (and detect technical effects)
- Heatmap / clustermap of top DE genes (pattern-level interpretation)

## Important note: batch–condition confounding (dataset limitation)
In this dataset, **sequencing batch is strongly confounded with infection status**:
- many sequencing batches contain **only covid-positive samples**
- controls are concentrated in a very small subset of batches

Because of this, a model like `~ batch + condition` cannot reliably separate
**technical batch effects** from **true infection-driven expression changes**.
As a result, batch-adjusted case–control DE may yield few or no significant genes.

**How this notebook handles it**
- Primary case–control comparison is reported with `~ condition` and accompanied by PCA/QC to show the confounding.
- Batch-adjusted modeling is emphasized for **within-covid analyses** where batch adjustment is identifiable (e.g., expression vs viral load / Ct, age, or sex).

## How to run
### Requirements
- Python 3.9+ recommended

Install dependencies:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn pydeseq2
```

Run the notebook:
```bash
jupyter notebook Project-2_clean.ipynb
```

## Outputs
- `metadata_*.csv` (sample annotations extracted from GEO series matrix)
- `deseq2_results_*.csv` (log2FC, p-values, adjusted p-values)
- PCA and heatmap figures generated in-notebook

## Suggested extensions
- Viral-load analysis within covid-positive samples using `n1_ct` (Ct proxy)
- Age/sex stratified analysis within covid-positive samples
- Pathway enrichment (GO/KEGG) on ranked genes or significant DEGs
- Package as a reproducible script/CLI (e.g., `run_deseq.py`) with saved outputs
