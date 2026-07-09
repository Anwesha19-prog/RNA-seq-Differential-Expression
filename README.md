# RNA-seq Differential Expression Analysis Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Snakemake](https://img.shields.io/badge/snakemake-≥7.0-brightgreen.svg)](https://snakemake.readthedocs.io)

A comprehensive, beginner-friendly **Snakemake workflow** for RNA-seq differential expression analysis using **pyDESeq2**. This pipeline analyzes the GSE152075 dataset comparing SARS-CoV-2 positive vs. negative nasopharyngeal swab samples.

## 🌟 Features

- **Automated Workflow**: Snakemake-based pipeline with automatic dependency tracking
- **Reproducible**: Conda environment ensures consistent results across systems
- **Modular Design**: Each analysis step is a separate, readable Python script
- **Comprehensive QC**: PCA, volcano plots, and heatmaps for quality control
- **Beginner-Friendly**: Clear documentation and well-commented code
- **Flexible**: Easy configuration through `config.yml` without code editing
- **Batch Effect Handling**: Statistical model accounts for sequencing batch effects

## 📊 Pipeline Overview

```
Raw Data (GEO) → Load & Parse → Filter Genes → DESeq2 Analysis → Visualizations
                      ↓              ↓              ↓                ↓
                  metadata.csv   filtered.csv   results.csv    plots/*.png
```

The workflow performs:
1. **Data Loading**: Parse GEO count matrix and metadata
2. **Gene Filtering**: Remove low-expression genes
3. **Differential Expression**: DESeq2 analysis with batch correction
4. **Visualization**: Generate volcano plot, PCA, and heatmap

## 🚀 Quick Start

### Prerequisites
- [Conda](https://docs.conda.io/en/latest/miniconda.html) or [Mamba](https://mamba.readthedocs.io/)
- 4GB+ RAM recommended
- ~500MB disk space for environment and results

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression.git
cd RNA-seq-Differential-Expression
```

2. **Create the conda environment**
```bash
conda env create -f environment.yml
conda activate project2-env
```

3. **Verify installation**
```bash
snakemake --version
python -c "import pydeseq2; print('pyDESeq2 installed successfully')"
```

### Running the Pipeline

**Execute the complete workflow:**
```bash
snakemake --cores 1
```

**Run specific steps:**
```bash
# Just run differential expression
snakemake results/deseq2_results.csv --cores 1

# Just generate plots
snakemake results/plots/volcano_plot.png --cores 1
```

**Dry run (preview what will be executed):**
```bash
snakemake -n
```

See [docs\USAGE.md](USAGE.md) for detailed usage instructions.

## 📁 Project Structure

```
RNA-seq-Differential-Expression/
├── README.md                      # This file
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
│
├── Snakefile                      # Main workflow definition
├── config.yml                     # Configuration parameters
├── environment.yml                # Conda environment specification
│
├── scripts/                       # Analysis scripts
│   ├── load_data.py              # Parse GEO files
│   ├── filter_genes.py           # Filter low-count genes
│   ├── run_deseq2.py             # Differential expression
│   ├── plot_volcano.py           # Volcano plot
│   ├── plot_pca.py               # PCA visualization
│   └── plot_heatmap.py           # Heatmap of top genes
│
├── data/                          # Input data (download from GEO)
│   ├── .gitkeep
│   ├── GSE152075_raw_counts_GEO.txt
│   └── GSE152075_series_matrix.txt
│
├── results/                       # Generated outputs
│   ├── counts_raw.csv
│   ├── counts_filtered.csv
│   ├── metadata.csv
│   ├── deseq2_results.csv
│   └── plots/
│       ├── volcano_plot.png
│       ├── pca_plot.png
│       └── heatmap.png
│
├── notebook/                      # Alternative Jupyter notebook approach
│   └── Project-2_clean.ipynb
│
└── docs/                          # Additional documentation
    |── FAQ.md
    ├── INSTALLATION.md                # Detailed installation guide
    ├── USAGE.md                       # Comprehensive usage guide
    ├── WORKFLOW.md                    # Detailed workflow explanation
    ├── CONFIGURATION.md               # Configuration options
    └── RESULTS.md                     # Guide to interpreting results
```

## 📈 Dataset Information

- **GEO Accession**: [GSE152075](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE152075)
- **Sample Type**: Nasopharyngeal swab RNA-seq
- **Data Type**: Gene-level raw counts
- **Comparison**: SARS-CoV-2 positive vs. negative samples

### Input Files

1. **`GSE152075_raw_counts_GEO.txt`**: Raw integer count matrix (genes × samples)
2. **`GSE152075_series_matrix.txt`**: Sample metadata including:
   - Condition (COVID-19 positive/negative)
   - Sequencing batch
   - Age, gender, N1 Ct values

Download from: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE152075

## 🔧 Configuration

Edit `config.yml` to customize the analysis:

```yaml
# Gene filtering threshold
min_total_count: 10

# DESeq2 design formula
design_formula: "~ batch + condition"

# Significance threshold
padj_threshold: 0.05

# Number of top genes in heatmap
top_n_genes: 50
```

See [docs/CONFIGURATION.md](CONFIGURATION.md) for detailed parameter descriptions.

## 📊 Output Files

| File | Description |
|------|-------------|
| `results/metadata.csv` | Processed sample metadata with condition labels |
| `results/counts_raw.csv` | Raw count matrix (aligned with metadata) |
| `results/counts_filtered.csv` | Filtered count matrix (low-count genes removed) |
| `results/deseq2_results.csv` | Differential expression results with statistics |
| `results/plots/volcano_plot.png` | Volcano plot (log2FC vs. significance) |
| `results/plots/pca_plot.png` | PCA plot showing sample clustering |
| `results/plots/heatmap.png` | Heatmap of top differentially expressed genes |

See [docs/RESULTS.md](RESULTS.md) for detailed interpretation guide.

## ⚠️ Important Notes

### Batch-Condition Confounding

This dataset has a **known limitation**: sequencing batch is strongly confounded with infection status. Many batches contain only COVID-positive samples, while controls are concentrated in a few batches.

**Implications:**
- A model like `~ batch + condition` cannot reliably separate technical batch effects from true biological differences
- Batch-adjusted analysis may yield fewer significant genes than expected
- This is a dataset limitation, not a pipeline issue

**Recommendations:**
- Use `~ condition` for primary case-control comparison
- Examine PCA plots to visualize the confounding
- For within-COVID analyses (e.g., viral load effects), batch adjustment is more appropriate

See [docs/WORKFLOW.md](WORKFLOW.md) for detailed discussion.

## 🛠️ Troubleshooting

**Common Issues:**

1. **`snakemake: command not found`**
   - Ensure conda environment is activated: `conda activate project2-env`

2. **Missing input files**
   - Download data files from GEO and place in `data/` directory
   - Verify filenames match those in `config.yml`

3. **Memory errors**
   - This dataset requires ~2-4GB RAM
   - Close other applications or use a machine with more memory

4. **Permission errors (Windows)**
   - Run terminal as administrator
   - Check file permissions in the project directory

See [docs/FAQ.md](docs/FAQ.md) for more troubleshooting tips.

## 📚 Documentation

- **[docs/INSTALLATION.md](INSTALLATION.md)**: Detailed installation instructions
- **[docs/USAGE.md](USAGE.md)**: Comprehensive usage guide
- **[docs/WORKFLOW.md](WORKFLOW.md)**: Step-by-step workflow explanation
- **[docs/CONFIGURATION.md](CONFIGURATION.md)**: Configuration options
- **[docs/RESULTS.md](RESULTS.md)**: Interpreting results
- **[docs/FAQ.md](docs/FAQ.md)**: Frequently asked questions

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dataset**: GSE152075 from NCBI GEO
- **Tools**: 
  - [pyDESeq2](https://pydeseq2.readthedocs.io/) - Python implementation of DESeq2
  - [Snakemake](https://snakemake.readthedocs.io/) - Workflow management
  - [DESeq2](https://bioconductor.org/packages/release/bioc/html/DESeq2.html) - Original R package
  - [Cline](https://docs.cline.bot/cline-overview) in VS Code and [Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5) for documentation

## 📧 Contact

- **Author**: Anwesha Sarkar
- **Repository**: https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression

## 📖 Citation

If you use this pipeline in your research, please cite:

```
Sarkar, A. (2026). RNA-seq Differential Expression Analysis Pipeline. 
GitHub repository: https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression
```

And the original tools:
- Love, M.I., Huber, W., Anders, S. (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biology*, 15:550.

## 🔗 Related Resources

- [DESeq2 Paper](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-014-0550-8)
- [pyDESeq2 Documentation](https://pydeseq2.readthedocs.io/)
- [Snakemake Tutorial](https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html)
- [RNA-seq Analysis Best Practices](https://www.bioconductor.org/help/course-materials/2016/CSAMA/lab-3-rnaseq/rnaseq_gene_CSAMA2016.html)

---

**Note**: This pipeline is designed for educational purposes and demonstrates best practices for reproducible RNA-seq analysis. For production use, consider additional quality control steps and validation.
