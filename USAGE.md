# Usage Guide

This guide provides comprehensive instructions for running the RNA-seq Differential Expression Analysis Pipeline.

## Table of Contents
- [Quick Start](#quick-start)
- [Running the Complete Workflow](#running-the-complete-workflow)
- [Running Individual Steps](#running-individual-steps)
- [Snakemake Commands](#snakemake-commands)
- [Workflow Visualization](#workflow-visualization)
- [Advanced Usage](#advanced-usage)
- [Common Workflows](#common-workflows)
- [Tips and Best Practices](#tips-and-best-practices)

## Quick Start

### Basic Execution

```bash
# 1. Activate the environment
conda activate project2-env

# 2. Navigate to project directory
cd RNA-seq-Differential-Expression

# 3. Run the complete pipeline
snakemake --cores 1
```

That's it! The pipeline will automatically:
- Load and parse data
- Filter low-count genes
- Run differential expression analysis
- Generate all plots

## Running the Complete Workflow

### Standard Execution

```bash
# Run with 1 core (recommended for this dataset)
snakemake --cores 1

# Run with multiple cores (for parallel execution)
snakemake --cores 4

# Run with all available cores
snakemake --cores all
```

### Dry Run (Preview)

Before running, preview what will be executed:

```bash
# Show what would be done
snakemake -n

# Show detailed reasoning
snakemake -n -r

# Show detailed reasoning with printout
snakemake -n -r -p
```

### Force Re-run

```bash
# Force re-run all steps
snakemake --cores 1 --forceall

# Force re-run specific rule
snakemake --cores 1 --forcerun run_deseq2

# Re-run from a specific step onwards
snakemake --cores 1 --forcerun filter_genes
```

## Running Individual Steps

You can run specific parts of the workflow by specifying target files:

### Step 1: Load Data Only

```bash
snakemake results/metadata.csv results/counts_raw.csv --cores 1
```

**Outputs:**
- `results/counts_raw.csv` - Raw count matrix
- `results/metadata.csv` - Sample metadata

### Step 2: Filter Genes

```bash
snakemake results/counts_filtered.csv --cores 1
```

**Outputs:**
- `results/counts_filtered.csv` - Filtered count matrix

### Step 3: Run DESeq2 Analysis

```bash
snakemake results/deseq2_results.csv --cores 1
```

**Outputs:**
- `results/deseq2_results.csv` - Differential expression results

### Step 4: Generate Specific Plots

```bash
# Volcano plot only
snakemake results/plots/volcano_plot.png --cores 1

# PCA plot only
snakemake results/plots/pca_plot.png --cores 1

# Heatmap only
snakemake results/plots/heatmap.png --cores 1

# All plots
snakemake results/plots/volcano_plot.png results/plots/pca_plot.png results/plots/heatmap.png --cores 1
```

## Snakemake Commands

### Essential Commands

```bash
# List all rules
snakemake --list

# List all target files
snakemake --list-target-rules

# Show rule dependencies
snakemake --list-params-changes

# Print shell commands
snakemake -n -p

# Detailed summary
snakemake --summary
```

### Workflow Information

```bash
# Show workflow DAG (requires graphviz)
snakemake --dag | dot -Tpng > workflow_dag.png

# Show rule graph
snakemake --rulegraph | dot -Tpng > rule_graph.png

# Show file graph
snakemake --filegraph | dot -Tpng > file_graph.png
```

### Cleaning Up

```bash
# Remove all output files
snakemake --delete-all-output

# Remove specific outputs
snakemake --delete-output results/deseq2_results.csv

# Clean temporary files
rm -rf .snakemake/
```

## Workflow Visualization

### Generate Workflow Diagram

Requires [Graphviz](https://graphviz.org/download/) to be installed:

```bash
# Install graphviz
conda install -c conda-forge graphviz

# Generate DAG (Directed Acyclic Graph)
snakemake --dag | dot -Tpng > dag.png

# Generate rule graph (simplified)
snakemake --rulegraph | dot -Tpng > rulegraph.png

# Generate with SVG (scalable)
snakemake --dag | dot -Tsvg > dag.svg
```

### View Workflow Report

```bash
# Generate HTML report
snakemake --report report.html

# This creates an interactive HTML report with:
# - Workflow statistics
# - Runtime information
# - File provenance
# - Rule execution details
```

## Advanced Usage

### Using Different Configuration Files

```bash
# Use custom config file
snakemake --configfile custom_config.yml --cores 1

# Override specific config values
snakemake --config min_total_count=20 padj_threshold=0.01 --cores 1
```

### Parallel Execution

```bash
# Run with 4 cores (independent steps run in parallel)
snakemake --cores 4

# Limit resources
snakemake --cores 4 --resources mem_mb=8000
```

### Cluster Execution (Advanced)

For running on HPC clusters:

```bash
# SLURM cluster
snakemake --cluster "sbatch -p {cluster.partition} -t {cluster.time}" \
          --cluster-config cluster.yml \
          --jobs 10

# SGE cluster
snakemake --cluster "qsub -pe smp {threads}" --jobs 10
```

### Conda Integration

```bash
# Use conda environments per rule (if defined)
snakemake --use-conda --cores 1

# Create conda environments only
snakemake --use-conda --conda-create-envs-only
```

### Logging

```bash
# Save log to file
snakemake --cores 1 > pipeline.log 2>&1

# Verbose output
snakemake --cores 1 --verbose

# Quiet mode (minimal output)
snakemake --cores 1 --quiet
```

## Common Workflows

### Workflow 1: First-Time Analysis

```bash
# 1. Activate environment
conda activate project2-env

# 2. Dry run to check everything
snakemake -n

# 3. Run complete pipeline
snakemake --cores 1

# 4. Check results
ls -lh results/
ls -lh results/plots/
```

### Workflow 2: Re-run with Different Parameters

```bash
# 1. Edit config.yml
nano config.yml  # or use your preferred editor

# 2. Force re-run affected steps
snakemake --cores 1 --forcerun run_deseq2

# 3. Check new results
head results/deseq2_results.csv
```

### Workflow 3: Generate Only Plots

```bash
# If you already have deseq2_results.csv
snakemake results/plots/volcano_plot.png \
          results/plots/pca_plot.png \
          results/plots/heatmap.png \
          --cores 1
```

### Workflow 4: Troubleshooting Failed Run

```bash
# 1. Check what failed
snakemake --summary

# 2. Clean failed outputs
snakemake --delete-all-output

# 3. Re-run with verbose output
snakemake --cores 1 --verbose

# 4. Or run specific step with debugging
snakemake results/deseq2_results.csv --cores 1 -p
```

### Workflow 5: Batch Processing Multiple Datasets

```bash
# Create separate config files
cp config.yml config_dataset1.yml
cp config.yml config_dataset2.yml

# Edit each config file for different datasets
# Then run separately:
snakemake --configfile config_dataset1.yml --cores 1
snakemake --configfile config_dataset2.yml --cores 1
```

## Tips and Best Practices

### Performance Tips

1. **Use appropriate core count**
   ```bash
   # For this pipeline, 1-2 cores is usually sufficient
   snakemake --cores 1
   ```

2. **Monitor resource usage**
   ```bash
   # Use system monitor while running
   htop  # Linux/macOS
   # Task Manager on Windows
   ```

3. **Clean up between runs**
   ```bash
   # Remove .snakemake directory if issues occur
   rm -rf .snakemake/
   ```

### Reproducibility Tips

1. **Always use the same environment**
   ```bash
   conda activate project2-env
   ```

2. **Document parameter changes**
   ```bash
   # Keep track of config.yml changes
   git diff config.yml
   ```

3. **Save workflow reports**
   ```bash
   snakemake --report report_$(date +%Y%m%d).html
   ```

### Debugging Tips

1. **Use dry run first**
   ```bash
   snakemake -n -r -p
   ```

2. **Run steps individually**
   ```bash
   # Test each step separately
   snakemake results/metadata.csv --cores 1
   ```

3. **Check intermediate files**
   ```bash
   # Inspect CSV files
   head results/counts_raw.csv
   wc -l results/counts_filtered.csv
   ```

4. **Enable verbose output**
   ```bash
   snakemake --cores 1 --verbose --printshellcmds
   ```

### File Management Tips

1. **Backup results before re-running**
   ```bash
   cp -r results/ results_backup_$(date +%Y%m%d)/
   ```

2. **Check file sizes**
   ```bash
   du -sh results/
   ls -lh results/*.csv
   ```

3. **Verify outputs exist**
   ```bash
   # Check all expected outputs
   ls results/deseq2_results.csv
   ls results/plots/*.png
   ```

## Interpreting Output Messages

### Success Messages

```
Building DAG of jobs...
Using shell: /bin/bash
Provided cores: 1
Rules claiming more threads will be scaled down.
Job counts:
    count   jobs
    1       all
    1       filter_genes
    1       load_data
    ...
    6

[timestamp] rule load_data:
    input: data/GSE152075_raw_counts_GEO.txt, data/GSE152075_series_matrix.txt
    output: results/counts_raw.csv, results/metadata.csv
    ...
Finished job 0.
6 of 6 steps (100%) done
```

### Common Warnings

```
Warning: Ignoring missing output file...
```
- Usually safe if file is optional

```
Nothing to be done.
```
- All outputs are up to date

### Error Messages

```
MissingInputException
```
- Input file not found - check data/ directory

```
RuleException
```
- Error in script execution - check script output

```
WorkflowError
```
- Configuration or workflow definition issue

## Next Steps

After running the pipeline:

1. **Examine Results**: See [RESULTS.md](RESULTS.md) for interpretation guide
2. **Customize Analysis**: See [CONFIGURATION.md](CONFIGURATION.md) for parameter tuning
3. **Understand Workflow**: See [WORKFLOW.md](WORKFLOW.md) for detailed explanation

## Getting Help

- **Check FAQ**: [docs/FAQ.md](docs/FAQ.md)
- **Snakemake Documentation**: https://snakemake.readthedocs.io/
- **Report Issues**: https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression/issues
