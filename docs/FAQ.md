# Frequently Asked Questions (FAQ)

Common questions and answers about the RNA-seq Differential Expression Analysis Pipeline.

## Table of Contents
- [General Questions](#general-questions)
- [Installation Issues](#installation-issues)
- [Running the Pipeline](#running-the-pipeline)
- [Configuration Questions](#configuration-questions)
- [Results Interpretation](#results-interpretation)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

## General Questions

### What is this pipeline for?

This pipeline performs differential expression analysis on RNA-seq count data using DESeq2 methodology (via pyDESeq2). It's designed for comparing gene expression between two conditions (e.g., disease vs. control).

### Do I need programming experience?

Basic command-line knowledge is helpful, but the pipeline is designed to be beginner-friendly. You mainly need to:
- Run commands in a terminal
- Edit a configuration file (YAML format)
- Interpret results

### What data do I need?

You need:
1. **Count matrix**: Gene-level raw counts (genes × samples)
2. **Metadata**: Sample information including conditions and covariates

For GEO datasets, you need:
- Raw counts file (e.g., `GSE152075_raw_counts_GEO.txt`)
- Series matrix file (e.g., `GSE152075_series_matrix.txt`)

### Can I use my own data?

Yes! You can adapt the pipeline for your data by:
1. Formatting your count matrix (genes as rows, samples as columns)
2. Creating a metadata file with sample information
3. Modifying `load_data.py` to read your format
4. Adjusting `config.yml` parameters

### What's the difference between this and the Jupyter notebook?

- **Snakemake workflow** (this): Automated, reproducible, production-ready
- **Jupyter notebook**: Interactive, exploratory, educational

Both perform the same analysis, but the Snakemake workflow is better for:
- Reproducibility
- Automation
- Large-scale analyses
- Sharing with collaborators

## Installation Issues

### Q: `conda: command not found`

**A:** Conda is not installed or not in your PATH.

**Solution:**
```bash
# Check if conda is installed
which conda  # Linux/macOS
where conda  # Windows

# If not found, install Miniconda
# Download from: https://docs.conda.io/en/latest/miniconda.html

# Or add to PATH (Linux/macOS)
export PATH="$HOME/miniconda3/bin:$PATH"
source ~/.bashrc
```

### Q: Environment creation fails with dependency conflicts

**A:** Conda can't resolve package dependencies.

**Solution:**
```bash
# Update conda first
conda update -n base conda

# Try with mamba (faster solver)
conda install -n base -c conda-forge mamba
mamba env create -f environment.yml

# Or create manually
conda create -n project2-env python=3.10
conda activate project2-env
conda install -c conda-forge snakemake pandas numpy matplotlib seaborn scikit-learn
pip install pydeseq2
```

### Q: pyDESeq2 installation fails

**A:** pip can't find or install pyDESeq2.

**Solution:**
```bash
# Update pip
pip install --upgrade pip

# Install specific version
pip install pydeseq2==0.4.0

# Or from GitHub
pip install git+https://github.com/owkin/PyDESeq2.git
```

### Q: Installation is very slow

**A:** Conda package resolution can be slow.

**Solution:**
```bash
# Use mamba (much faster)
conda install -n base -c conda-forge mamba
mamba env create -f environment.yml

# Or use libmamba solver
conda install -n base conda-libmamba-solver
conda config --set solver libmamba
```

## Running the Pipeline

### Q: How do I run the pipeline?

**A:** Basic execution:
```bash
# 1. Activate environment
conda activate project2-env

# 2. Navigate to project directory
cd RNA-seq-Differential-Expression

# 3. Run pipeline
snakemake --cores 1
```

### Q: `Nothing to be done`

**A:** All outputs are up-to-date.

**Solution:**
```bash
# Force re-run all steps
snakemake --cores 1 --forceall

# Or re-run specific step
snakemake --cores 1 --forcerun run_deseq2
```

### Q: Pipeline fails partway through

**A:** An error occurred in one of the steps.

**Solution:**
```bash
# 1. Read the error message carefully
# 2. Check which step failed
# 3. Run that step individually for debugging
snakemake results/deseq2_results.csv --cores 1 -p

# 4. Check intermediate files
head results/counts_filtered.csv
head results/metadata.csv
```

### Q: How long should it take?

**A:** Typical runtime for GSE152075:
- Data loading: 1-2 minutes
- Gene filtering: <1 minute
- DESeq2 analysis: 5-15 minutes
- Plotting: 1-2 minutes
- **Total: ~10-20 minutes**

Larger datasets may take longer.

### Q: Can I run steps in parallel?

**A:** Yes, for independent steps:
```bash
# Use multiple cores
snakemake --cores 4

# Note: Most steps are sequential for this pipeline
# Plotting steps can run in parallel
```

## Configuration Questions

### Q: How do I change parameters?

**A:** Edit `config.yml`:
```yaml
# Example: More stringent filtering
min_total_count: 20
padj_threshold: 0.01
```

Then re-run:
```bash
snakemake --cores 1 --forcerun run_deseq2
```

### Q: Should I use batch correction?

**A:** It depends:

**Use `~ batch + condition` when:**
- Batch is NOT confounded with condition
- You have samples from both conditions in each batch
- PCA shows batch effects

**Use `~ condition` when:**
- Batch is confounded with condition
- All samples in a batch are from one condition
- Batch adjustment removes biological signal

For GSE152075, batch is confounded, so `~ condition` is often better.

### Q: What threshold should I use?

**A:** Depends on your goals:

**Exploratory analysis:**
```yaml
padj_threshold: 0.10
min_total_count: 5
```

**Standard analysis:**
```yaml
padj_threshold: 0.05
min_total_count: 10
```

**Stringent/validation:**
```yaml
padj_threshold: 0.01
min_total_count: 20
```

### Q: Can I analyze different conditions?

**A:** Yes, modify the design formula:
```yaml
# Compare treatments
design_formula: "~ treatment"

# Multiple factors
design_formula: "~ batch + gender + treatment"

# Continuous covariate
design_formula: "~ age + condition"
```

## Results Interpretation

### Q: I have no significant genes. Why?

**A:** Several possible reasons:

1. **Batch-condition confounding**: Try `design_formula: "~ condition"`
2. **Threshold too stringent**: Try `padj_threshold: 0.10`
3. **Weak biological signal**: May be real - check PCA
4. **Small sample size**: Need more samples for power
5. **High variability**: Check PCA for outliers

### Q: All my genes are significant. Is this normal?

**A:** Unusual but possible:

**Check:**
- Very strong biological effect (e.g., infection vs. control)
- Metadata is correct (conditions not swapped)
- No technical artifacts
- PCA shows clear separation

If everything checks out, this may be real!

### Q: How do I interpret log2FoldChange?

**A:** Conversion table:
```
log2FC = 1  → 2-fold change (2x)
log2FC = 2  → 4-fold change (4x)
log2FC = 3  → 8-fold change (8x)
log2FC = -1 → 0.5-fold (50% of original)
log2FC = -2 → 0.25-fold (25% of original)
```

**Direction:**
- Positive: Higher in COVID (upregulated)
- Negative: Lower in COVID (downregulated)

### Q: What's the difference between pvalue and padj?

**A:**
- **pvalue**: Raw p-value (don't use for significance!)
- **padj**: Adjusted for multiple testing (use this!)

Always use `padj < 0.05` for significance, not `pvalue < 0.05`.

### Q: How many significant genes should I expect?

**A:** For GSE152075:
- With `~ condition`: 100-5,000 genes (strong immune response)
- With `~ batch + condition`: 0-100 genes (batch confounding)

Varies by dataset and biological effect size.

## Troubleshooting

### Q: `MissingInputException: Missing input files`

**A:** Input data files not found.

**Solution:**
```bash
# Check files exist
ls data/GSE152075_raw_counts_GEO.txt
ls data/GSE152075_series_matrix.txt

# Verify paths in config.yml match actual files
cat config.yml
```

### Q: `KeyError: 'batch'` or similar

**A:** Variable in design formula not in metadata.

**Solution:**
```bash
# Check metadata columns
head results/metadata.csv

# Adjust design formula to match
# If no 'batch' column, use:
design_formula: "~ condition"
```

### Q: Memory error

**A:** Not enough RAM.

**Solution:**
- Close other applications
- Use a machine with more RAM (need ~4GB)
- Filter more aggressively: `min_total_count: 50`

### Q: Plots are blank or corrupted

**A:** Plotting error or no data to plot.

**Solution:**
```bash
# Check if results file has data
wc -l results/deseq2_results.csv

# Check for significant genes
python -c "import pandas as pd; df = pd.read_csv('results/deseq2_results.csv', index_col=0); print((df['padj'] < 0.05).sum())"

# If no significant genes, relax threshold
```

### Q: `PermissionError` (Windows)

**A:** File access denied.

**Solution:**
- Run terminal as Administrator
- Check antivirus isn't blocking
- Ensure files aren't open in Excel
- Install Miniconda in user directory (not Program Files)

## Advanced Usage

### Q: Can I use this for other organisms?

**A:** Yes! The pipeline is organism-agnostic. You just need:
- Count matrix for your organism
- Metadata with conditions
- Adjust `load_data.py` if needed for your format

### Q: Can I add more plots?

**A:** Yes! Create a new script:

```python
# scripts/plot_custom.py
import pandas as pd
import matplotlib.pyplot as plt

results = pd.read_csv(snakemake.input.results, index_col=0)
# Your plotting code here
plt.savefig(snakemake.output.plot)
```

Add rule to `Snakefile`:
```python
rule plot_custom:
    input:
        results = "results/deseq2_results.csv"
    output:
        plot = "results/plots/custom_plot.png"
    script:
        "scripts/plot_custom.py"
```

### Q: How do I export results for pathway analysis?

**A:** Use Python or R:

```python
import pandas as pd

results = pd.read_csv('results/deseq2_results.csv', index_col=0)

# Significant genes only
sig = results[results['padj'] < 0.05]
sig.index.to_series().to_csv('sig_genes.txt', index=False, header=False)

# Ranked list for GSEA
ranked = results[['log2FoldChange']].dropna().sort_values('log2FoldChange', ascending=False)
ranked.to_csv('ranked_genes.rnk', sep='\t', header=False)
```

### Q: Can I run this on a cluster?

**A:** Yes! Snakemake supports HPC:

```bash
# SLURM
snakemake --cluster "sbatch -p normal -t 1:00:00" --jobs 10

# SGE
snakemake --cluster "qsub -pe smp {threads}" --jobs 10
```

See [Snakemake cluster documentation](https://snakemake.readthedocs.io/en/stable/executing/cluster.html).

### Q: How do I cite this pipeline?

**A:** Use:
```
Sarkar, A. (2026). RNA-seq Differential Expression Analysis Pipeline. 
GitHub: https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression
```

Also cite the tools:
- Love et al. (2014) for DESeq2 methodology
- Snakemake (Köster & Rahmann, 2012)

## Still Have Questions?

If your question isn't answered here:

1. **Check documentation**:
   - [README.md](../README.md) - Overview
   - [INSTALLATION.md](../INSTALLATION.md) - Installation help
   - [USAGE.md](../USAGE.md) - Usage details
   - [WORKFLOW.md](../WORKFLOW.md) - How it works
   - [CONFIGURATION.md](../CONFIGURATION.md) - Parameter details
   - [RESULTS.md](../RESULTS.md) - Interpreting results

2. **Search GitHub Issues**: [Existing issues](https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression/issues)

3. **Create new issue**: [Report a problem](https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression/issues/new)

4. **Community resources**:
   - [Snakemake documentation](https://snakemake.readthedocs.io/)
   - [pyDESeq2 documentation](https://pydeseq2.readthedocs.io/)
   - [Biostars forum](https://www.biostars.org/)
