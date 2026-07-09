# Configuration Guide

This guide explains all configuration parameters in `config.yml` and how to customize the RNA-seq differential expression analysis pipeline.

## Table of Contents
- [Configuration File Overview](#configuration-file-overview)
- [Parameter Reference](#parameter-reference)
- [Common Configuration Scenarios](#common-configuration-scenarios)
- [Design Formula Guide](#design-formula-guide)
- [Advanced Configuration](#advanced-configuration)
- [Best Practices](#best-practices)

## Configuration File Overview

The `config.yml` file contains all adjustable parameters for the pipeline. This allows you to customize the analysis without modifying any Python code.

**Default `config.yml`:**
```yaml
# Configuration file for SARS-CoV-2 differential expression analysis

# Input data files
counts_file: "data/GSE152075_raw_counts_GEO.txt"
series_matrix_file: "data/GSE152075_series_matrix.txt"

# Analysis parameters
min_total_count: 10  # Minimum total count across all samples to keep a gene
design_formula: "~ batch + condition"  # DESeq2 design formula
padj_threshold: 0.05  # Adjusted p-value threshold for significance
top_n_genes: 50  # Number of top DE genes to show in heatmap
```

## Parameter Reference

### Input Data Files

#### `counts_file`
- **Type**: String (file path)
- **Default**: `"data/GSE152075_raw_counts_GEO.txt"`
- **Description**: Path to the raw count matrix file
- **Format**: Tab or space-delimited text file with genes as rows and samples as columns
- **Requirements**: 
  - First column: gene identifiers
  - Remaining columns: integer counts for each sample
  - Header row with sample names

**Example:**
```yaml
counts_file: "data/my_counts.txt"
```

#### `series_matrix_file`
- **Type**: String (file path)
- **Default**: `"data/GSE152075_series_matrix.txt"`
- **Description**: Path to the GEO series matrix file containing sample metadata
- **Format**: GEO series matrix format
- **Requirements**:
  - Contains `!Sample_title` field
  - Contains `!Sample_characteristics_ch1` fields with metadata

**Example:**
```yaml
series_matrix_file: "data/my_series_matrix.txt"
```

### Analysis Parameters

#### `min_total_count`
- **Type**: Integer
- **Default**: `10`
- **Description**: Minimum total count across all samples required to keep a gene
- **Purpose**: Filters out lowly expressed genes to reduce noise
- **Range**: Typically 5-50
- **Impact**:
  - **Lower values** (5-10): Keep more genes, more noise
  - **Higher values** (20-50): Fewer genes, less noise, may lose lowly expressed genes

**When to adjust:**
- **Increase** (20-50) if:
  - You have deep sequencing (>30M reads/sample)
  - You want to focus on highly expressed genes
  - You're seeing too many low-count genes in results
  
- **Decrease** (5-10) if:
  - You have shallow sequencing (<10M reads/sample)
  - You're interested in lowly expressed genes
  - You're losing genes of interest

**Examples:**
```yaml
# Conservative filtering (keep more genes)
min_total_count: 5

# Standard filtering
min_total_count: 10

# Stringent filtering (focus on highly expressed)
min_total_count: 50
```

#### `design_formula`
- **Type**: String (R formula syntax)
- **Default**: `"~ batch + condition"`
- **Description**: DESeq2 design formula specifying the statistical model
- **Format**: R formula notation (e.g., `~ covariate1 + covariate2 + condition`)
- **Requirements**:
  - Must start with `~`
  - Variables must exist in metadata
  - Last term is typically the variable of interest

**Common formulas:**
```yaml
# Simple model (no covariates)
design_formula: "~ condition"

# Batch-adjusted model
design_formula: "~ batch + condition"

# Multiple covariates
design_formula: "~ batch + gender + condition"

# Interaction term
design_formula: "~ batch + condition + batch:condition"
```

See [Design Formula Guide](#design-formula-guide) for detailed explanation.

#### `padj_threshold`
- **Type**: Float
- **Default**: `0.05`
- **Description**: Adjusted p-value (FDR) threshold for significance
- **Range**: 0.0 to 1.0 (typically 0.01 to 0.10)
- **Purpose**: Controls false discovery rate
- **Impact**:
  - **Lower values** (0.01): More stringent, fewer false positives
  - **Higher values** (0.10): Less stringent, more discoveries but more false positives

**When to adjust:**
- **Use 0.01** for:
  - High-stakes applications
  - Validation studies
  - When you need high confidence

- **Use 0.05** for:
  - Standard exploratory analysis
  - Balanced sensitivity/specificity

- **Use 0.10** for:
  - Exploratory/hypothesis-generating studies
  - When you expect subtle effects
  - Small sample sizes

**Examples:**
```yaml
# Stringent (high confidence)
padj_threshold: 0.01

# Standard
padj_threshold: 0.05

# Relaxed (exploratory)
padj_threshold: 0.10
```

#### `top_n_genes`
- **Type**: Integer
- **Default**: `50`
- **Description**: Number of top differentially expressed genes to display in heatmap
- **Range**: 10-500 (practical limits)
- **Purpose**: Controls heatmap complexity and readability
- **Impact**:
  - **Fewer genes** (10-30): Clearer visualization, focus on top hits
  - **More genes** (100-200): Comprehensive view, may be cluttered

**When to adjust:**
- **Use 20-30** for:
  - Publication-quality figures
  - Clear, focused visualization
  - Presentations

- **Use 50-100** for:
  - Comprehensive overview
  - Identifying gene clusters
  - Exploratory analysis

- **Use 100+** for:
  - Detailed analysis
  - Large-scale patterns
  - When you have many significant genes

**Examples:**
```yaml
# Focused view
top_n_genes: 25

# Standard view
top_n_genes: 50

# Comprehensive view
top_n_genes: 100
```

## Common Configuration Scenarios

### Scenario 1: Simple Case-Control Comparison (No Batch Correction)

**Use case**: When batch is confounded with condition, or you want a simple comparison

```yaml
counts_file: "data/GSE152075_raw_counts_GEO.txt"
series_matrix_file: "data/GSE152075_series_matrix.txt"
min_total_count: 10
design_formula: "~ condition"  # No batch adjustment
padj_threshold: 0.05
top_n_genes: 50
```

### Scenario 2: Batch-Corrected Analysis

**Use case**: When you have clear batch effects that are NOT confounded with condition

```yaml
counts_file: "data/GSE152075_raw_counts_GEO.txt"
series_matrix_file: "data/GSE152075_series_matrix.txt"
min_total_count: 10
design_formula: "~ batch + condition"  # Adjust for batch
padj_threshold: 0.05
top_n_genes: 50
```

### Scenario 3: Stringent Analysis (High Confidence)

**Use case**: When you need high-confidence results for validation or publication

```yaml
counts_file: "data/GSE152075_raw_counts_GEO.txt"
series_matrix_file: "data/GSE152075_series_matrix.txt"
min_total_count: 20  # Stricter filtering
design_formula: "~ batch + condition"
padj_threshold: 0.01  # More stringent threshold
top_n_genes: 30  # Focus on top genes
```

### Scenario 4: Exploratory Analysis

**Use case**: Initial exploration, hypothesis generation

```yaml
counts_file: "data/GSE152075_raw_counts_GEO.txt"
series_matrix_file: "data/GSE152075_series_matrix.txt"
min_total_count: 5  # Keep more genes
design_formula: "~ condition"
padj_threshold: 0.10  # More permissive
top_n_genes: 100  # Broader view
```

### Scenario 5: Multiple Covariates

**Use case**: Adjusting for multiple technical or biological factors

```yaml
counts_file: "data/GSE152075_raw_counts_GEO.txt"
series_matrix_file: "data/GSE152075_series_matrix.txt"
min_total_count: 10
design_formula: "~ batch + gender + age + condition"  # Multiple adjustments
padj_threshold: 0.05
top_n_genes: 50
```

## Design Formula Guide

The design formula specifies the statistical model used by DESeq2.

### Basic Syntax

```
~ covariate1 + covariate2 + ... + variable_of_interest
```

- **`~`**: Required prefix
- **`+`**: Additive effects
- **Last term**: Variable being tested (typically `condition`)
- **Earlier terms**: Covariates to adjust for

### Common Patterns

#### 1. Simple Model
```yaml
design_formula: "~ condition"
```
- Tests for condition effect only
- No adjustment for covariates
- Use when: No confounding factors or batch effects

#### 2. Batch-Adjusted Model
```yaml
design_formula: "~ batch + condition"
```
- Adjusts for batch effects
- Tests for condition effect after removing batch variation
- Use when: Clear batch effects that are NOT confounded with condition

#### 3. Multiple Covariates
```yaml
design_formula: "~ batch + gender + condition"
```
- Adjusts for multiple factors
- Tests for condition effect after removing all covariate effects
- Use when: Multiple sources of variation to control

#### 4. Continuous Covariate
```yaml
design_formula: "~ age + condition"
```
- Adjusts for continuous variable (age)
- Use when: Continuous confounders exist

#### 5. Interaction Term
```yaml
design_formula: "~ batch + condition + batch:condition"
```
- Tests if condition effect varies by batch
- More complex model
- Use when: You suspect batch-specific effects

### Important Considerations

1. **Order matters**: Last term is what you're testing
2. **Collinearity**: Variables shouldn't be perfectly correlated
3. **Sample size**: More complex models need more samples
4. **Confounding**: If batch is confounded with condition, adjustment may remove biological signal

### Variable Requirements

Variables in the formula must:
- Exist in `metadata.csv`
- Be categorical (for factors) or numeric (for continuous)
- Have sufficient variation (not all same value)
- Have enough samples per level (at least 2-3)

## Advanced Configuration

### Using Different Datasets

To analyze a different dataset:

```yaml
# Your custom dataset
counts_file: "data/my_experiment_counts.txt"
series_matrix_file: "data/my_experiment_metadata.txt"
min_total_count: 10
design_formula: "~ treatment"  # Adjust to your variables
padj_threshold: 0.05
top_n_genes: 50
```

### Command-Line Overrides

You can override config values without editing the file:

```bash
# Override single parameter
snakemake --config min_total_count=20 --cores 1

# Override multiple parameters
snakemake --config min_total_count=20 padj_threshold=0.01 --cores 1

# Use different config file
snakemake --configfile custom_config.yml --cores 1
```

### Multiple Configurations

Create separate config files for different analyses:

```bash
# Create configs
cp config.yml config_stringent.yml
cp config.yml config_exploratory.yml

# Edit each file with different parameters

# Run with specific config
snakemake --configfile config_stringent.yml --cores 1
```

## Best Practices

### 1. Start with Defaults

Always run with default parameters first to establish a baseline:

```yaml
min_total_count: 10
design_formula: "~ batch + condition"
padj_threshold: 0.05
top_n_genes: 50
```

### 2. Document Changes

Keep track of parameter changes:

```yaml
# Configuration for stringent analysis - 2026-07-09
# Increased filtering and significance threshold for validation
min_total_count: 20  # Increased from 10
padj_threshold: 0.01  # Decreased from 0.05
```

### 3. Version Control

Use git to track config changes:

```bash
git diff config.yml  # See what changed
git commit -m "Adjusted filtering threshold for stringent analysis"
```

### 4. Test Incrementally

Change one parameter at a time to understand its impact:

```bash
# Test 1: Default
snakemake --cores 1

# Test 2: Change filtering only
snakemake --config min_total_count=20 --cores 1

# Test 3: Change threshold only
snakemake --config padj_threshold=0.01 --cores 1
```

### 5. Validate Results

After changing parameters:
- Check number of significant genes
- Examine PCA plot for quality
- Review volcano plot distribution
- Verify heatmap makes sense

### 6. Consider Biological Context

Choose parameters based on:
- **Sequencing depth**: Deeper sequencing → can use higher `min_total_count`
- **Sample size**: More samples → can use more complex `design_formula`
- **Study goals**: Exploratory → relaxed thresholds; Validation → stringent thresholds
- **Expected effect size**: Large effects → standard thresholds; Subtle effects → may need relaxed thresholds

## Troubleshooting Configuration Issues

### Issue: No Significant Genes

**Possible causes:**
- `padj_threshold` too stringent
- `min_total_count` too high
- Batch-condition confounding

**Solutions:**
```yaml
# Try relaxing thresholds
padj_threshold: 0.10
min_total_count: 5

# Or remove batch adjustment if confounded
design_formula: "~ condition"
```

### Issue: Too Many Significant Genes

**Possible causes:**
- `padj_threshold` too relaxed
- `min_total_count` too low
- Strong biological effect

**Solutions:**
```yaml
# Try more stringent thresholds
padj_threshold: 0.01
min_total_count: 20
```

### Issue: Design Formula Error

**Error message**: `Variable not found in metadata`

**Solution:**
- Check variable names in `results/metadata.csv`
- Ensure spelling matches exactly
- Verify variable has variation

### Issue: Heatmap Too Cluttered

**Solution:**
```yaml
# Reduce number of genes
top_n_genes: 25
```

### Issue: Heatmap Shows No Genes

**Possible cause:** No genes pass `padj_threshold`

**Solution:**
```yaml
# Relax threshold
padj_threshold: 0.10
```

## Related Documentation

- [USAGE.md](USAGE.md) - How to run with different configurations
- [WORKFLOW.md](WORKFLOW.md) - Understanding what each parameter affects
- [RESULTS.md](RESULTS.md) - Interpreting results from different configurations
- [docs/FAQ.md](docs/FAQ.md) - Common configuration questions

## Getting Help

If you're unsure about configuration:
1. Start with defaults
2. Consult [WORKFLOW.md](WORKFLOW.md) for parameter effects
3. Check [docs/FAQ.md](docs/FAQ.md) for common scenarios
4. Ask on [GitHub Issues](https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression/issues)
