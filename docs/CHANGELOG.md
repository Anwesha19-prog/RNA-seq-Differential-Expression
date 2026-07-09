# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Automated testing suite
- Support for additional GEO datasets
- Interactive HTML reports
- Additional visualization options
- Docker container for easy deployment

## [1.0.0] - 2026-07-09

### Added
- Complete Snakemake workflow for RNA-seq differential expression analysis
- Six modular Python scripts for each analysis step:
  - `load_data.py`: Data loading and preprocessing
  - `filter_genes.py`: Low-count gene filtering
  - `run_deseq2.py`: Differential expression analysis with pyDESeq2
  - `plot_volcano.py`: Volcano plot generation
  - `plot_pca.py`: PCA visualization
  - `plot_heatmap.py`: Heatmap of top DE genes
- Comprehensive documentation:
  - `README.md`: Project overview and quick start
  - `INSTALLATION.md`: Detailed installation guide
  - `USAGE.md`: Comprehensive usage instructions
  - `WORKFLOW.md`: Detailed workflow explanation
  - `CONFIGURATION.md`: Configuration parameter guide
  - `RESULTS.md`: Results interpretation guide
  - `CONTRIBUTING.md`: Contribution guidelines
  - `docs/FAQ.md`: Frequently asked questions
- Configuration file (`config.yml`) for easy parameter customization
- Conda environment specification (`environment.yml`)
- `.gitignore` for proper version control
- MIT License
- Support for GEO series matrix format
- Batch effect correction capability
- Flexible design formula specification
- Automatic sample alignment between count matrix and metadata

### Features
- **Beginner-friendly**: Clear documentation and modular code
- **Reproducible**: Conda environment and Snakemake workflow
- **Flexible**: Easy configuration without code modification
- **Robust**: Handles batch effects and missing data
- **Comprehensive**: Complete analysis from raw data to publication-quality plots

### Technical Details
- Python 3.10+ support
- Snakemake ≥7.0 workflow management
- pyDESeq2 ≥0.4.0 for differential expression
- Pandas, NumPy, Matplotlib, Seaborn for data processing and visualization
- Scikit-learn for PCA analysis

### Dataset
- Primary dataset: GSE152075 (SARS-CoV-2 nasopharyngeal swab RNA-seq)
- Comparison: COVID-19 positive vs. negative samples
- Includes batch information and clinical metadata

### Known Limitations
- Batch-condition confounding in GSE152075 dataset
- Manual testing only (automated tests planned for future release)
- Limited to count-based RNA-seq data
- Requires GEO series matrix format for metadata

## [0.2.0] - 2026-06-15 (Pre-release)

### Added
- Initial Jupyter notebook implementation
- Basic DESeq2 analysis workflow
- PCA and heatmap visualizations
- Manual data loading and processing

### Changed
- Migrated from notebook to Snakemake workflow
- Improved error handling
- Enhanced documentation

## [0.1.0] - 2026-05-01 (Initial Development)

### Added
- Project initialization
- Basic data loading scripts
- Exploratory data analysis
- Initial documentation

---

## Version History Summary

- **v1.0.0** (2026-07-09): First stable release with complete Snakemake workflow
- **v0.2.0** (2026-06-15): Pre-release with notebook implementation
- **v0.1.0** (2026-05-01): Initial development version

## How to Read This Changelog

### Categories

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

### Version Numbers

Following [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards-compatible)
- **PATCH**: Bug fixes (backwards-compatible)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute to this project.

## Links

- [Repository](https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression)
- [Issues](https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression/issues)
- [Releases](https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression/releases)
