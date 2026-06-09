# 🧬 Cancer Transcriptomics Project

**Realistic Cancer Data Simulation & Differential Expression Analysis**


<div align="center">
    <h3>🔬 Simulating Breast Cancer Transcriptomics Data with Differential Expression Analysis</h3>
    <p>5,000 Genes | 100 Samples | TCGA-Based Patterns | Volcano Plot + Heatmap Visualization</p>
</div>



## 📋 About

This project performs **realistic cancer transcriptomics data simulation** based on TCGA (The Cancer Genome Atlas) breast cancer patterns. It creates a simulated gene expression dataset with **5,000 genes** across **100 samples** (50 tumor, 50 normal), incorporating biologically realistic expression patterns including:

-  **Strongly upregulated genes** (potential oncogenes)
-  **Strongly downregulated genes** (tumor suppressors)
-  **Moderately regulated genes** (cancer-associated)
-  **Statistical significance testing** with multiple testing correction
-  **Differential expression analysis** between tumor and normal samples
---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **Realistic Simulation** | Based on TCGA breast cancer expression patterns |
| **Sample Size** | 5,000 genes × 100 samples (50 tumor, 50 normal) |
| **Expression Patterns** | Log-normal distribution with biological fold-changes |
| **Differential Expression** | t-test with Bonferroni correction |
| **Visualization** | Volcano plot + Expression heatmap |
| **Output Format** | PNG images (publication-ready) |
| **Requirements** | Base R only (no additional packages needed) |

---

## 📊 Pipeline Architecture
<img width="200" height="500" alt="deepseek_mermaid_20260609_64663f" src="https://github.com/user-attachments/assets/87c84033-fc35-4ec2-ab21-6c5b8efbe754" />


---

## 🔬 Biological Simulation Design

### Expression Patterns by Gene Range

| Gene Range | Regulation Type | Fold Change | Biological Meaning |
|------------|----------------|-------------|--------------------|
| **1-300** | Strongly Upregulated | **5×** | Potential **oncogenes** - drive cancer growth |
| **301-600** | Strongly Downregulated | **0.2×** (5× less) | Potential **tumor suppressors** - inactivated |
| **601-1000** | Moderately Upregulated | **2.5×** | Cancer-associated genes |
| **1001-1500** | Moderately Downregulated | **0.4×** | Protective genes |
| **1501-5000** | No Change | **1×** | Housekeeping genes |

### Statistical Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Tumor meanlog** | 8.0 | Average tumor expression (log scale) |
| **Normal meanlog** | 7.5 | Average normal expression (log scale) |
| **Tumor sdlog** | 1.5 | Tumor expression variability |
| **Normal sdlog** | 1.2 | Normal expression variability |
| **Significance threshold** | p < 0.05 | After Bonferroni correction |
| **Log2FC threshold** | \|log2FC\| > 1 | Biologically meaningful change |

}



