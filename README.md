---


#  TCGA Cancer Analysis Dashboard

**Differential Expression Analysis & PCA Visualization for Breast Cancer (TCGA-BRCA)**

[![Open in Hugging Face](https://img.shields.io/badge/🤗-Launch%20Demo-FFD21E?style=for-the-badge&logo=huggingface)](https://huggingface.co/spaces/somiya-khan01/tcga_dashboard_cancer_analysis)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)](https://python.org)

<div align="center">
  <a href="https://huggingface.co/spaces/somiya-khan01/tcga_dashboard_cancer_analysis">
    <img src="https://img.shields.io/badge/🚀_LAUNCH_DEMO_-Click_Here-FF5722?style=for-the-badge&logo=huggingface&logoColor=white" alt="Launch Demo" width="250">
  </a>
</div>

---

##  About

A **Streamlit-based web application** for analyzing TCGA breast cancer (BRCA) RNA-Seq data. The dashboard performs:

- **Differential Expression Analysis** (DESeq2-style)
- **Principal Component Analysis (PCA)** for sample-level quality control
- **Volcano Plot** visualization of significant genes
- **Heatmap** of top differentially expressed genes
- **Interactive data tables** for result exploration

---

##  Features

| Feature | Description |
|---------|-------------|
| **PCA Analysis** | Visualize sample separation between tumor and normal groups |
| **Differential Expression** | Identify upregulated/downregulated genes (log2FC, padj) |
| **Volcano Plot** | Interactive visualization of significant genes |
| **Heatmap** | Expression patterns of top 1000 genes |
| **Data Export** | Download results as CSV |
| **Variance Explained** | Bar plot of PC contribution |

---

##  Launch Demo

<div align="center">
  <a href="https://huggingface.co/spaces/somiya-khan01/tcga_dashboard_cancer_analysis">
    <img src="https://img.shields.io/badge/🔬_LIVE_DEMO_-TRY_NOW-4CAF50?style=for-the-badge&logo=huggingface&logoColor=white" alt="Live Demo" width="300">
  </a>
</div>

**Click the badge above or visit:** https://huggingface.co/spaces/somiya-khan01/tcga_dashboard_cancer_analysis

---

##  Dashboard Preview

### PCA Analysis - Tumor vs Normal Separation

<img width="1408" height="775" alt="image" src="https://github.com/user-attachments/assets/799d0260-5072-45bc-9f90-076d9a957e13" />


*Figure 1: PCA showing separation between tumor (red) and normal (green) samples*

---

### Differential Expression Results Table

<img width="1395" height="566" alt="image" src="https://github.com/user-attachments/assets/ac3ddbcc-aef8-46d1-8a6f-7f08bd4a9cfb" />


*Figure 2: Top differentially expressed genes with log2FC and adjusted p-values*

---

### Heatmap

<img width="1399" height="648" alt="image" src="https://github.com/user-attachments/assets/611fa555-56b9-4a79-a03a-4e75946b121a" />


*Figure 3: Heatmap*

---

##  Required Data Files

Upload these CSV files to use the dashboard:

| File | Description |
|------|-------------|
| `deseq2_results.csv` | DESeq2 output with log2FC and padj |
| `counts_top1000.csv` | Normalized counts for top 1000 genes |
| `sample_fixed.csv` | Sample metadata (tumor/normal labels) |


---

##  Pipeline Architecture
<img width="5093" height="468" alt="deepseek_mermaid_20260609_07153a" src="https://github.com/user-attachments/assets/a36617e4-abf4-4024-bb9f-d67f3212d8cc" />

---

##  Biological Simulation Design

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





