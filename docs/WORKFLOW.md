# Workflow Documentation

This document provides a detailed explanation of the RNA-seq differential expression analysis workflow, including how data flows through the pipeline and what happens at each step.

## Table of Contents
- [Workflow Overview](#workflow-overview)
- [Workflow Diagram](#workflow-diagram)
- [Pipeline Steps Explained](#pipeline-steps-explained)
- [File Dependencies](#file-dependencies)
- [Understanding the Results](#understanding-the-results)
- [Key Features](#key-features)
- [Customization Points](#customization-points)
- [Important Considerations](#important-considerations)
- [Tips for Beginners](#tips-for-beginners)

## Workflow Overview

This pipeline implements a complete RNA-seq differential expression analysis workflow using **Snakemake** for workflow management and **pyDESeq2** for statistical analysis. The workflow is designed to be:

- **Beginner-friendly**: Clear, modular scripts with extensive comments
- **Reproducible**: Automated dependency tracking ensures consistent results
- **Flexible**: Easy configuration without code modification
- **Robust**: Handles batch effects and provides comprehensive QC

## Workflow Diagram

```
Input Data Files
├── GSE152075_raw_counts_GEO.txt (raw count matrix)
└── GSE152075_series_matrix.txt (sample metadata)
        ↓
┌───────────────────────────────────────┐
│  Step 1: load_data.py                 │
│  - Parse count matrix                 │
│  - Extract metadata from series file  │
│  - Align samples                      │
│  - Convert condition labels           │
└───────────────────────────────────────┘
        ↓
    counts_raw.csv + metadata.csv
        ↓
┌───────────────────────────────────────┐
│  Step 2: filter_genes.py              │
│  - Remove low-count genes             │
│  - Keep genes with total count ≥ 10  │
│  - Reduce noise                       │
└───────────────────────────────────────┘
        ↓
    counts_filtered.csv
        ↓
┌───────────────────────────────────────┐
│  Step 3: run_deseq2.py                │
│  - Differential expression analysis   │
│  - Design: ~ batch + condition        │
│  - Contrast: covid vs control         │
│  - Statistical testing                │
└───────────────────────────────────────┘
        ↓
    deseq2_results.csv
        ↓
┌───────────────────────────────────────┐
│  Step 4-6: Generate Plots             │
│  ├── plot_volcano.py → volcano.png    │
│  ├── plot_pca.py → pca.png            │
│  └── plot_heatmap.py → heatmap.png    │
└───────────────────────────────────────┘
```

## Pipeline Steps Explained

### Step 1: Data Loading (`load_data.py`)

**Input Files:**
- `data/GSE152075_raw_counts_GEO.txt` - Raw count matrix
- `data/GSE152075_series_matrix.txt` - GEO series matrix

**Output Files:**
- `results/counts_raw.csv` - Processed count matrix
- `results/metadata.csv` - Sample metadata

**What it does:**

1. **Reads the raw count matrix** (genes × samples)
   - Handles various delimiters (tab, space)
   - Converts to integer counts (required by DESeq2)
   - Fills missing values with 0

2. **Parses the GEO series matrix file** to extract:
   - Sample conditions (COVID positive/negative)
   - Sequencing batch information
   - Optional covariates:
     - Age
     - Gender
     - N1 Ct values (viral load proxy)

3. **Processes metadata:**
   - Converts condition labels: `pos` → `covid`, `neg` → `control`
   - Converts to categorical types (required for DESeq2)
   - Handles missing values appropriately

4. **Aligns count matrix and metadata:**
   - Ensures sample names match between files
   - Handles case-insensitive and whitespace variations
   - Keeps only samples present in both files

**Key Functions:**
- `get_field_values()`: Extracts fields from series matrix
- `to_numeric_clean()`: Converts messy numeric fields
- Regex extraction for metadata fields

**Output Preview:**
```
metadata.csv:
sample,condition,batch,age,gender,n1_ct
Sample1,covid,A,45,M,25.3
Sample2,control,B,52,F,NA
...
```

### Step 2: Gene Filtering (`filter_genes.py`)

**Input Files:**
- `results/counts_raw.csv`

**Output Files:**
- `results/counts_filtered.csv`

**What it does:**

1. **Filters low-expression genes:**
   - Calculates total count across all samples for each gene
   - Removes genes with total count < threshold (default: 10)
   - Reduces noise and improves statistical power

2. **Why filter?**
   - Low-count genes have unreliable estimates
   - Filtering reduces multiple testing burden
   - Improves false discovery rate control
   - Speeds up downstream analysis

**Parameters:**
- `min_total_count`: Minimum total count threshold (from `config.yml`)

**Typical Results:**
- Before filtering: ~60,000 genes
- After filtering: ~20,000-30,000 genes
- Removed: ~30,000-40,000 low-count genes

### Step 3: Differential Expression (`run_deseq2.py`)

**Input Files:**
- `results/counts_filtered.csv`
- `results/metadata.csv`

**Output Files:**
- `results/deseq2_results.csv`

**What it does:**

1. **Prepares data for DESeq2:**
   - Transposes count matrix (DESeq2 expects samples as rows)
   - Sets categorical reference levels (control as baseline)
   - Ensures proper data types

2. **Creates DESeq2 dataset:**
   - Design formula: `~ batch + condition` (default)
   - Accounts for batch effects
   - Tests for condition effect (covid vs control)

3. **Runs DESeq2 analysis:**
   - **Size factor normalization**: Accounts for library size differences
   - **Dispersion estimation**: Models gene-wise variability
   - **Negative binomial GLM fitting**: Models count data appropriately
   - **Wald test**: Tests for differential expression
   - **Multiple testing correction**: Benjamini-Hochberg FDR

4. **Computes statistics:**
   - Contrast: `condition covid vs control`
   - Generates results table with:
     - baseMean: Average normalized expression
     - log2FoldChange: Effect size
     - lfcSE: Standard error
     - stat: Test statistic
     - pvalue: Raw p-value
     - padj: Adjusted p-value (FDR)

**Statistical Model:**
```
counts ~ NegativeBinomial(μ, α)
log(μ) = β₀ + β_batch + β_condition
```

Where:
- μ: Expected count
- α: Dispersion parameter
- β_batch: Batch effect coefficients
- β_condition: Condition effect (what we test)

**Output Preview:**
```
deseq2_results.csv:
gene,baseMean,log2FoldChange,lfcSE,stat,pvalue,padj
GENE1,1234.5,2.3,0.15,15.3,1.2e-52,3.4e-48
GENE2,567.8,-1.8,0.20,-9.0,2.3e-19,4.5e-16
...
```

### Step 4: Volcano Plot (`plot_volcano.py`)

**Input Files:**
- `results/deseq2_results.csv`

**Output Files:**
- `results/plots/volcano_plot.png`

**What it does:**

1. **Creates volcano plot:**
   - X-axis: log2 fold change (effect size)
   - Y-axis: -log10(adjusted p-value) (significance)
   - Points colored by significance threshold

2. **Interpretation:**
   - **Top of plot**: Most significant genes
   - **Left side**: Downregulated in COVID (higher in control)
   - **Right side**: Upregulated in COVID
   - **Gray points**: Not significant (padj ≥ 0.05)
   - **Colored points**: Significant (padj < 0.05)

**Parameters:**
- `padj_threshold`: Significance cutoff (from `config.yml`)

### Step 5: PCA Plot (`plot_pca.py`)

**Input Files:**
- `results/counts_filtered.csv`
- `results/metadata.csv`

**Output Files:**
- `results/plots/pca_plot.png`

**What it does:**

1. **Performs PCA:**
   - Log-transforms counts: log2(count + 1)
   - Standardizes features (genes)
   - Computes principal components
   - Plots PC1 vs PC2

2. **Visualization:**
   - Points represent samples
   - Colors indicate condition (covid vs control)
   - Shows percentage of variance explained

3. **Interpretation:**
   - **Good separation**: Conditions cluster separately
   - **Batch effects**: Samples cluster by batch instead of condition
   - **Outliers**: Points far from their group
   - **Quality control**: Identifies technical issues

### Step 6: Heatmap (`plot_heatmap.py`)

**Input Files:**
- `results/counts_filtered.csv`
- `results/metadata.csv`
- `results/deseq2_results.csv`

**Output Files:**
- `results/plots/heatmap.png`

**What it does:**

1. **Selects top DE genes:**
   - Filters by adjusted p-value < threshold
   - Selects top N genes by significance (default: 50)

2. **Prepares data:**
   - Extracts counts for selected genes
   - Log-transforms: log2(count + 1)
   - Z-score normalizes (per gene)

3. **Creates clustered heatmap:**
   - Hierarchical clustering of genes (rows)
   - Hierarchical clustering of samples (columns)
   - Color bar shows sample conditions
   - Dendrograms show relationships

4. **Interpretation:**
   - **Red**: High expression (above mean)
   - **Blue**: Low expression (below mean)
   - **Gene clusters**: Co-regulated genes
   - **Sample clusters**: Similar expression profiles

**Parameters:**
- `padj_threshold`: Significance cutoff
- `top_n_genes`: Number of genes to display

## File Dependencies

```
config.yml ──────────────────┐
                             ↓
data/GSE152075_*.txt ──→ load_data ──→ filter_genes ──→ run_deseq2 ──→ plots
                             ↓              ↓              ↓
                        metadata.csv   counts_filt   results.csv
                             └──────────────┴──────────────┘
                                           ↓
                                    All plotting scripts
```

**Dependency Rules:**
- `filter_genes` requires `load_data` outputs
- `run_deseq2` requires `filter_genes` and `load_data` outputs
- All plots require their respective inputs
- Snakemake automatically determines execution order

## Understanding the Results

### `deseq2_results.csv` Columns

| Column | Description | Interpretation |
|--------|-------------|----------------|
| **gene** | Gene identifier | Gene name or ID |
| **baseMean** | Average normalized count | Overall expression level |
| **log2FoldChange** | Log2 fold change | Effect size (positive = higher in COVID) |
| **lfcSE** | Standard error of log2FC | Uncertainty in effect size |
| **stat** | Wald test statistic | Test statistic value |
| **pvalue** | Raw p-value | Uncorrected significance |
| **padj** | Adjusted p-value | **Use this for significance!** |

### Interpreting Significance

**Statistical Significance:**
- **padj < 0.05**: Statistically significant (default threshold)
- **padj < 0.01**: Highly significant
- **padj < 0.001**: Very highly significant

**Biological Significance:**
- **|log2FoldChange| > 1**: 2-fold change (biologically meaningful)
- **|log2FoldChange| > 2**: 4-fold change (strong effect)
- **|log2FoldChange| > 3**: 8-fold change (very strong effect)

**Combined Criteria:**
- **High confidence DE genes**: padj < 0.05 AND |log2FC| > 1
- **Direction**: 
  - log2FC > 0: Upregulated in COVID
  - log2FC < 0: Downregulated in COVID (higher in control)

### Example Interpretation

```
Gene: IFIT1
baseMean: 2345.6
log2FoldChange: 3.2
padj: 1.2e-45
```

**Interpretation:**
- IFIT1 is highly expressed (baseMean = 2345.6)
- 3.2 log2FC = 2^3.2 = ~9-fold higher in COVID samples
- Extremely significant (padj = 1.2e-45)
- **Conclusion**: IFIT1 is strongly upregulated in COVID-19

## Key Features

### Beginner-Friendly Design

1. **Modular scripts**: Each step is a separate, readable Python script
2. **Clear naming**: File and variable names are descriptive
3. **Extensive comments**: Scripts include explanatory comments
4. **Configuration**: Parameters in `config.yml` (no code editing needed)
5. **Error handling**: Informative error messages

### Snakemake Benefits

1. **Automatic dependency tracking**: Only reruns necessary steps
2. **Parallel execution**: Can run independent steps simultaneously
3. **Reproducibility**: Same inputs always produce same outputs
4. **Checkpointing**: Resumes from last successful step if interrupted
5. **Workflow visualization**: Generate diagrams of the pipeline

### Statistical Rigor

1. **Negative binomial modeling**: Appropriate for count data
2. **Batch effect correction**: Accounts for technical variation
3. **Multiple testing correction**: Controls false discovery rate
4. **Robust normalization**: Size factor normalization
5. **Dispersion estimation**: Gene-wise variance modeling

## Customization Points

Edit `config.yml` to customize the analysis:

```yaml
# Gene filtering threshold
min_total_count: 10          # Increase to be more stringent

# Statistical model
design_formula: "~ batch + condition"  # Modify for different designs

# Significance threshold
padj_threshold: 0.05         # Adjust for more/less stringent cutoff

# Visualization
top_n_genes: 50              # Number of genes in heatmap
```

### Common Modifications

**1. Change significance threshold:**
```yaml
padj_threshold: 0.01  # More stringent
```

**2. Remove batch correction:**
```yaml
design_formula: "~ condition"  # Simple model
```

**3. Stricter gene filtering:**
```yaml
min_total_count: 50  # Keep only highly expressed genes
```

**4. More genes in heatmap:**
```yaml
top_n_genes: 100  # Show more genes
```

## Important Considerations

### Batch-Condition Confounding

**Critical Issue**: In this dataset, sequencing batch is strongly confounded with infection status.

**What this means:**
- Many batches contain **only COVID-positive samples**
- Controls are concentrated in a **few batches**
- Cannot reliably separate batch effects from biological effects

**Implications:**
- Model `~ batch + condition` may yield **few significant genes**
- Batch adjustment removes both technical AND biological signal
- This is a **dataset limitation**, not a pipeline issue

**Recommendations:**

1. **For case-control comparison:**
   ```yaml
   design_formula: "~ condition"  # No batch adjustment
   ```
   - Examine PCA to visualize confounding
   - Interpret results cautiously

2. **For within-COVID analyses:**
   ```yaml
   design_formula: "~ batch + n1_ct"  # Viral load analysis
   ```
   - Batch adjustment is appropriate
   - Tests viral load effects within COVID samples

3. **Quality control:**
   - Always examine PCA plot
   - Check batch distribution across conditions
   - Consider batch as a biological variable if confounded

## Tips for Beginners

### Getting Started

1. **Start with defaults**: Run with default parameters first
2. **Check intermediate files**: Inspect CSVs to understand data flow
3. **One step at a time**: Use `snakemake <target>` to run partial workflow
4. **Dry run first**: Use `snakemake -n` to preview execution
5. **Read the logs**: Pay attention to console output

### Understanding the Analysis

1. **Examine PCA first**: Shows overall data structure
2. **Check gene filtering**: How many genes were removed?
3. **Review DE results**: How many significant genes?
4. **Interpret volcano plot**: Where are the significant genes?
5. **Study heatmap**: Do samples cluster by condition?

### Troubleshooting

1. **Check input files**: Ensure data files are in `data/` directory
2. **Verify environment**: `conda activate project2-env`
3. **Read error messages**: They usually indicate the problem
4. **Run step-by-step**: Isolate which step fails
5. **Check file sizes**: Ensure outputs are reasonable

### Best Practices

1. **Document changes**: Keep notes on parameter modifications
2. **Backup results**: Save results before re-running
3. **Version control**: Use git to track changes
4. **Reproducibility**: Record exact commands used
5. **Validate results**: Cross-check with literature

## Additional Resources

### Learning Materials

- **DESeq2 Paper**: [Love et al., 2014](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-014-0550-8)
- **Snakemake Tutorial**: https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html
- **RNA-seq Best Practices**: https://www.bioconductor.org/help/course-materials/

### Related Documentation

- [USAGE.md](USAGE.md) - How to run the pipeline
- [CONFIGURATION.md](CONFIGURATION.md) - Parameter details
- [RESULTS.md](RESULTS.md) - Interpreting outputs
- [docs/FAQ.md](docs/FAQ.md) - Common questions

### Getting Help

- **GitHub Issues**: Report bugs or ask questions
- **Snakemake Docs**: Workflow management help
- **pyDESeq2 Docs**: Statistical analysis help
- **Bioinformatics Forums**: Community support

---

**Note**: This workflow is designed for educational purposes and demonstrates best practices for reproducible RNA-seq analysis. For production use, consider additional quality control steps, validation, and biological interpretation with domain experts.
