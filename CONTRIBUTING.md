# Contributing to RNA-seq Differential Expression Pipeline

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Trolling or insulting/derogatory comments
- Public or private harassment
- Publishing others' private information without permission

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When reporting a bug, include:**
- **Clear title**: Descriptive summary of the issue
- **Steps to reproduce**: Detailed steps to reproduce the problem
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment details**:
  - Operating system and version
  - Python version
  - Conda/Mamba version
  - Snakemake version
  - pyDESeq2 version
- **Error messages**: Full error output (use code blocks)
- **Configuration**: Your `config.yml` settings
- **Data info**: Dataset size, number of samples (if applicable)

**Example bug report:**
```markdown
## Bug: DESeq2 analysis fails with batch adjustment

**Environment:**
- OS: Windows 11
- Python: 3.10.8
- Snakemake: 7.18.2
- pyDESeq2: 0.4.2

**Steps to reproduce:**
1. Set `design_formula: "~ batch + condition"` in config.yml
2. Run `snakemake --cores 1`
3. Error occurs at run_deseq2 step

**Error message:**
```
ValueError: Variable 'batch' not found in metadata
```

**Expected:** Analysis should complete successfully
**Actual:** Analysis fails with error

**Additional context:** Metadata file contains 'sequencing_batch' column, not 'batch'
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:
- **Clear description**: What feature you'd like to see
- **Use case**: Why this would be useful
- **Examples**: How it would work
- **Alternatives**: Other approaches you've considered

### Contributing Code

We welcome code contributions! Areas where help is appreciated:
- Bug fixes
- New features
- Documentation improvements
- Test coverage
- Performance optimizations
- Additional plotting functions
- Support for other datasets

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/RNA-seq-Differential-Expression.git
cd RNA-seq-Differential-Expression
```

### 2. Create Development Environment

```bash
# Create conda environment
conda env create -f environment.yml
conda activate project2-env

# Install development dependencies (if any)
pip install pytest black flake8
```

### 3. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 4. Make Changes

- Write clear, commented code
- Follow existing code style
- Add tests if applicable
- Update documentation

### 5. Test Your Changes

```bash
# Run the pipeline with test data
snakemake --cores 1

# Run tests (if available)
pytest tests/

# Check code style
black scripts/
flake8 scripts/
```

## Coding Standards

### Python Style

Follow [PEP 8](https://pep8.org/) style guidelines:

```python
# Good
def load_count_matrix(file_path, min_count=10):
    """
    Load and filter count matrix.
    
    Parameters
    ----------
    file_path : str
        Path to count matrix file
    min_count : int, default=10
        Minimum total count threshold
        
    Returns
    -------
    pd.DataFrame
        Filtered count matrix
    """
    counts = pd.read_csv(file_path, index_col=0)
    return counts[counts.sum(axis=1) >= min_count]

# Bad
def loadCountMatrix(filePath,minCount=10):
    counts=pd.read_csv(filePath,index_col=0)
    return counts[counts.sum(axis=1)>=minCount]
```

### Documentation

**Docstrings:**
- Use NumPy-style docstrings
- Document all functions, classes, and modules
- Include parameter types and descriptions
- Provide usage examples

**Comments:**
- Explain *why*, not *what*
- Keep comments up-to-date
- Use clear, concise language

**Example:**
```python
def filter_low_count_genes(counts, threshold=10):
    """
    Remove genes with low total counts across all samples.
    
    Low-count genes have unreliable estimates and increase the
    multiple testing burden. Filtering improves statistical power.
    
    Parameters
    ----------
    counts : pd.DataFrame
        Count matrix with genes as rows, samples as columns
    threshold : int, default=10
        Minimum total count across all samples
        
    Returns
    -------
    pd.DataFrame
        Filtered count matrix
        
    Examples
    --------
    >>> counts = pd.DataFrame({'S1': [100, 5], 'S2': [120, 3]})
    >>> filtered = filter_low_count_genes(counts, threshold=10)
    >>> len(filtered)
    1
    """
    total_counts = counts.sum(axis=1)
    return counts[total_counts >= threshold]
```

### Snakemake Rules

```python
# Good: Clear, documented rule
rule run_deseq2:
    """
    Run differential expression analysis using pyDESeq2.
    
    Performs negative binomial GLM fitting with specified design formula.
    """
    input:
        counts = "results/counts_filtered.csv",
        metadata = "results/metadata.csv"
    output:
        results = "results/deseq2_results.csv"
    params:
        design = config["design_formula"]
    script:
        "scripts/run_deseq2.py"
```

### File Organization

```
scripts/
├── load_data.py          # Data loading and preprocessing
├── filter_genes.py       # Gene filtering
├── run_deseq2.py         # Differential expression
├── plot_volcano.py       # Volcano plot
├── plot_pca.py           # PCA plot
└── plot_heatmap.py       # Heatmap

# Each script should:
# - Have a clear, single purpose
# - Include docstring at top
# - Use Snakemake input/output/params
# - Print progress messages
# - Handle errors gracefully
```

## Submitting Changes

### Pull Request Process

1. **Update documentation**
   - Update README.md if needed
   - Update relevant .md files
   - Add comments to code

2. **Test thoroughly**
   - Run the complete pipeline
   - Test edge cases
   - Verify outputs are correct

3. **Commit changes**
   ```bash
   git add .
   git commit -m "Add feature: descriptive message"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Go to GitHub repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out PR template

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tested with default parameters
- [ ] Tested with custom parameters
- [ ] Verified outputs are correct
- [ ] Updated documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Comments added where needed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Commit Messages

Write clear, descriptive commit messages:

```bash
# Good
git commit -m "Fix: Handle missing batch column in metadata"
git commit -m "Add: Support for custom design formulas"
git commit -m "Docs: Update installation instructions for Windows"

# Bad
git commit -m "fix bug"
git commit -m "update"
git commit -m "changes"
```

**Format:**
```
Type: Brief description (50 chars or less)

Detailed explanation if needed (wrap at 72 chars).
Explain what and why, not how.

Fixes #123
```

**Types:**
- `Fix`: Bug fixes
- `Add`: New features
- `Update`: Updates to existing features
- `Docs`: Documentation changes
- `Refactor`: Code refactoring
- `Test`: Adding or updating tests
- `Style`: Code style changes

## Reporting Bugs

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**To Reproduce**
1. Step 1
2. Step 2
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 11, macOS 12, Ubuntu 20.04]
- Python version: [e.g., 3.10.8]
- Snakemake version: [e.g., 7.18.2]
- pyDESeq2 version: [e.g., 0.4.2]

**Error Output**
```
Paste full error message here
```

**Configuration**
```yaml
# Your config.yml settings
```

**Additional Context**
Any other relevant information
```

## Suggesting Enhancements

### Enhancement Template

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why this feature would be useful

**Proposed Solution**
How you envision this working

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Any other relevant information
```

## Development Guidelines

### Adding New Scripts

When adding new analysis scripts:

1. **Follow naming convention**: `verb_noun.py` (e.g., `plot_volcano.py`)
2. **Use Snakemake integration**:
   ```python
   # Access Snakemake variables
   input_file = snakemake.input.data
   output_file = snakemake.output.result
   param_value = snakemake.params.threshold
   ```

3. **Include progress messages**:
   ```python
   print("Starting analysis...")
   print(f"Loaded {len(data)} samples")
   print("Analysis complete!")
   ```

4. **Handle errors gracefully**:
   ```python
   try:
       data = pd.read_csv(input_file)
   except FileNotFoundError:
       raise FileNotFoundError(f"Input file not found: {input_file}")
   ```

### Adding New Rules

When adding Snakemake rules:

```python
rule new_analysis:
    """
    Brief description of what this rule does.
    """
    input:
        data = "results/input_file.csv"
    output:
        result = "results/output_file.csv"
    params:
        param1 = config["param1"]
    script:
        "scripts/new_analysis.py"
```

### Testing

Currently, testing is manual. Future contributions for automated testing are welcome!

**Manual testing checklist:**
- [ ] Pipeline runs without errors
- [ ] Outputs are generated correctly
- [ ] Results are scientifically valid
- [ ] Documentation is accurate
- [ ] Works on different operating systems

## Questions?

If you have questions about contributing:
- Check existing [documentation](README.md)
- Search [existing issues](https://github.com/Anwesha19-prog/RNA-seq-Differential-Expression/issues)
- Create a new issue with the "question" label

## Recognition

Contributors will be acknowledged in:
- README.md contributors section
- CHANGELOG.md for specific contributions
- GitHub contributors page

Thank you for contributing to make this project better! 🎉
