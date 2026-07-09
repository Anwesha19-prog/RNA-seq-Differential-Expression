"""
Snakemake workflow for SARS-CoV-2 differential expression analysis
"""

# Configuration
configfile: "config.yml"

# Define all final outputs
rule all:
    input:
        "results/metadata.csv",
        "results/counts_filtered.csv",
        "results/deseq2_results.csv",
        "results/plots/volcano_plot.png",
        "results/plots/pca_plot.png",
        "results/plots/heatmap.png"

# Rule 1: Load and process raw data
rule load_data:
    input:
        counts = config["counts_file"],
        series_matrix = config["series_matrix_file"]
    output:
        counts = "results/counts_raw.csv",
        metadata = "results/metadata.csv"
    script:
        "scripts/load_data.py"

# Rule 2: Filter low-count genes
rule filter_genes:
    input:
        counts = "results/counts_raw.csv",
        metadata = "results/metadata.csv"
    output:
        counts_filtered = "results/counts_filtered.csv"
    params:
        min_count = config["min_total_count"]
    script:
        "scripts/filter_genes.py"

# Rule 3: Run differential expression analysis
rule run_deseq2:
    input:
        counts = "results/counts_filtered.csv",
        metadata = "results/metadata.csv"
    output:
        results = "results/deseq2_results.csv"
    params:
        design = config["design_formula"]
    script:
        "scripts/run_deseq2.py"

# Rule 4: Generate volcano plot
rule plot_volcano:
    input:
        results = "results/deseq2_results.csv"
    output:
        plot = "results/plots/volcano_plot.png"
    params:
        padj_threshold = config["padj_threshold"]
    script:
        "scripts/plot_volcano.py"

# Rule 5: Generate PCA plot
rule plot_pca:
    input:
        counts = "results/counts_filtered.csv",
        metadata = "results/metadata.csv"
    output:
        plot = "results/plots/pca_plot.png"
    script:
        "scripts/plot_pca.py"

# Rule 6: Generate heatmap of top DE genes
rule plot_heatmap:
    input:
        counts = "results/counts_filtered.csv",
        metadata = "results/metadata.csv",
        results = "results/deseq2_results.csv"
    output:
        plot = "results/plots/heatmap.png"
    params:
        padj_threshold = config["padj_threshold"],
        top_n_genes = config["top_n_genes"]
    script:
        "scripts/plot_heatmap.py"
