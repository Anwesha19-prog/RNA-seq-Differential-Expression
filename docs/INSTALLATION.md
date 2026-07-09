# Installation Guide

This guide provides detailed instructions for installing and setting up the RNA-seq Differential Expression Analysis Pipeline.

## Table of Contents
- [System Requirements](#system-requirements)
- [Installing Conda](#installing-conda)
- [Setting Up the Environment](#setting-up-the-environment)
- [Verification](#verification)
- [Alternative Installation Methods](#alternative-installation-methods)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+, CentOS 7+)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: ~2GB (500MB for environment, 1.5GB for data and results)
- **Python**: 3.10 or higher (installed via Conda)

### Software Prerequisites
- **Conda** or **Mamba** (package manager)
- **Git** (for cloning the repository)

## Installing Conda

If you don't have Conda installed, follow these instructions:

### Option 1: Miniconda (Recommended)

Miniconda is a minimal installer for Conda.

**Windows:**
1. Download [Miniconda installer](https://docs.conda.io/en/latest/miniconda.html)
2. Run the installer (`.exe` file)
3. Follow the installation wizard
4. Check "Add Miniconda to PATH" (optional but convenient)

**macOS/Linux:**
```bash
# Download installer
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Make executable
chmod +x Miniconda3-latest-Linux-x86_64.sh

# Run installer
./Miniconda3-latest-Linux-x86_64.sh

# Follow prompts, accept license, and initialize conda
```

### Option 2: Mamba (Faster Alternative)

Mamba is a faster reimplementation of Conda:

```bash
# Install Mamba via Conda
conda install -n base -c conda-forge mamba

# Or install Mambaforge directly
# Download from: https://github.com/conda-forge/miniforge#mambaforge
```

### Verify Conda Installation

```bash
conda --version
# Should output: conda 4.x.x or higher
```

## Setting Up the Environment

### Step 1: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression.git

# Navigate to project directory
cd RNA-seq-Differential-Expression
```

**Alternative (if Git is not available):**
- Download ZIP from GitHub
- Extract to desired location
- Navigate to extracted folder

### Step 2: Create Conda Environment

**Using Conda:**
```bash
conda env create -f environment.yml
```

**Using Mamba (faster):**
```bash
mamba env create -f environment.yml
```

This will create an environment named `project2-env` with all required dependencies:
- Python 3.10
- Snakemake ≥7.0
- pandas ≥1.5
- numpy ≥1.23
- matplotlib ≥3.6
- seaborn ≥0.12
- scikit-learn ≥1.2
- pydeseq2 ≥0.4.0

**Installation time**: 5-15 minutes depending on internet speed

### Step 3: Activate the Environment

```bash
conda activate project2-env
```

Your command prompt should now show `(project2-env)` prefix.

### Step 4: Download Data Files

Download the required data files from GEO:

1. Visit: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE152075

2. Download these files:
   - **Supplementary file**: `GSE152075_raw_counts_GEO.txt.gz`
   - **Series Matrix File**: `GSE152075_series_matrix.txt.gz`

3. Extract and place in `data/` directory:

```bash
# On Linux/macOS
gunzip data/GSE152075_raw_counts_GEO.txt.gz
gunzip data/GSE152075_series_matrix.txt.gz

# On Windows (use 7-Zip or similar)
# Or extract manually
```

**Direct download links:**
```bash
# Using wget (Linux/macOS)
cd data/
wget https://ftp.ncbi.nlm.nih.gov/geo/series/GSE152nnn/GSE152075/suppl/GSE152075_raw_counts_GEO.txt.gz
wget https://ftp.ncbi.nlm.nih.gov/geo/series/GSE152nnn/GSE152075/matrix/GSE152075_series_matrix.txt.gz
gunzip *.gz
cd ..

# Using curl (alternative)
curl -O https://ftp.ncbi.nlm.nih.gov/geo/series/GSE152nnn/GSE152075/suppl/GSE152075_raw_counts_GEO.txt.gz
```

## Verification

### Verify Environment Setup

```bash
# Check Snakemake installation
snakemake --version
# Expected output: 7.x.x or higher

# Check Python version
python --version
# Expected output: Python 3.10.x

# Check pyDESeq2 installation
python -c "import pydeseq2; print('pyDESeq2 version:', pydeseq2.__version__)"
# Expected output: pyDESeq2 version: 0.4.x

# List all installed packages
conda list
```

### Verify Data Files

```bash
# Check if data files exist (Linux/macOS)
ls -lh data/

# Windows (PowerShell)
dir data\

# Expected files:
# - GSE152075_raw_counts_GEO.txt (~50MB)
# - GSE152075_series_matrix.txt (~100KB)
```

### Test Run (Dry Run)

```bash
# Preview what Snakemake will execute
snakemake -n

# Expected output: List of jobs to be executed
# Should show: load_data, filter_genes, run_deseq2, plot_volcano, plot_pca, plot_heatmap
```

## Alternative Installation Methods

### Method 1: Using pip (Not Recommended)

If you prefer pip over Conda:

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install snakemake pandas numpy matplotlib seaborn scikit-learn pydeseq2

# Note: This method may have dependency conflicts
```

### Method 2: Using Docker (Advanced)

For containerized deployment:

```dockerfile
# Dockerfile (create this file)
FROM continuumio/miniconda3:latest

WORKDIR /app
COPY environment.yml .
RUN conda env create -f environment.yml

COPY . .
CMD ["conda", "run", "-n", "project2-env", "snakemake", "--cores", "1"]
```

```bash
# Build and run
docker build -t rnaseq-pipeline .
docker run -v $(pwd)/data:/app/data -v $(pwd)/results:/app/results rnaseq-pipeline
```

## Troubleshooting

### Issue 1: Conda Command Not Found

**Problem**: `conda: command not found`

**Solution**:
```bash
# Add Conda to PATH (Linux/macOS)
export PATH="$HOME/miniconda3/bin:$PATH"

# Or reinitialize
~/miniconda3/bin/conda init bash
source ~/.bashrc

# Windows: Restart terminal or use Anaconda Prompt
```

### Issue 2: Environment Creation Fails

**Problem**: `ResolvePackageNotFound` or dependency conflicts

**Solution**:
```bash
# Update Conda
conda update -n base conda

# Try with specific channels
conda env create -f environment.yml -c conda-forge -c bioconda

# Or create environment manually
conda create -n project2-env python=3.10
conda activate project2-env
conda install -c conda-forge snakemake pandas numpy matplotlib seaborn scikit-learn
pip install pydeseq2
```

### Issue 3: pyDESeq2 Installation Fails

**Problem**: `ERROR: Could not find a version that satisfies the requirement pydeseq2`

**Solution**:
```bash
# Ensure pip is updated
pip install --upgrade pip

# Install with specific version
pip install pydeseq2==0.4.0

# Or install from source
pip install git+https://github.com/owkin/PyDESeq2.git
```

### Issue 4: Slow Download Speeds

**Problem**: Conda package downloads are very slow

**Solution**:
```bash
# Use Mamba instead
conda install -n base -c conda-forge mamba
mamba env create -f environment.yml

# Or configure faster mirrors
conda config --add channels conda-forge
conda config --set channel_priority strict
```

### Issue 5: Permission Errors (Windows)

**Problem**: `PermissionError` when creating environment

**Solution**:
- Run Anaconda Prompt as Administrator
- Or install Miniconda in user directory (not Program Files)
- Check antivirus settings (may block file creation)

### Issue 6: SSL Certificate Errors

**Problem**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution**:
```bash
# Temporary workaround (not recommended for production)
conda config --set ssl_verify false

# Better solution: Update certificates
conda update -n base conda
pip install --upgrade certifi
```

### Issue 7: Disk Space Issues

**Problem**: Not enough disk space

**Solution**:
```bash
# Clean Conda cache
conda clean --all

# Remove unused environments
conda env list
conda env remove -n unused_env_name

# Check disk usage
du -sh ~/miniconda3/
```

## Platform-Specific Notes

### Windows
- Use **Anaconda Prompt** or **PowerShell** (not CMD)
- Path separators: use `\` or `/` (both work in most cases)
- Some commands may require administrator privileges

### macOS
- May need to install Xcode Command Line Tools:
  ```bash
  xcode-select --install
  ```
- For M1/M2 Macs, use `osx-arm64` packages when available

### Linux
- Ensure `build-essential` is installed:
  ```bash
  sudo apt-get install build-essential  # Ubuntu/Debian
  sudo yum groupinstall "Development Tools"  # CentOS/RHEL
  ```

## Next Steps

After successful installation:

1. **Read the Usage Guide**: See [USAGE.md](USAGE.md)
2. **Run the Pipeline**: Execute `snakemake --cores 1`
3. **Explore Results**: Check `results/` directory
4. **Customize**: Edit `config.yml` for your needs

## Getting Help

If you encounter issues not covered here:

1. Check [docs/FAQ.md](docs/FAQ.md)
2. Search existing [GitHub Issues](https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression/issues)
3. Create a new issue with:
   - Your operating system
   - Conda/Python version
   - Full error message
   - Steps to reproduce

## Additional Resources

- [Conda User Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/)
- [Snakemake Documentation](https://snakemake.readthedocs.io/)
- [pyDESeq2 Documentation](https://pydeseq2.readthedocs.io/)
