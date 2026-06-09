# 🧬 TCGA Breast Cancer RNA-Seq Dashboard

Interactive Streamlit dashboard for exploring DESeq2 differential expression
results from TCGA-BRCA data.

---

## ⚡ Quickstart

```bash
# 1. Clone / copy your project folder
cd tcga_dashboard

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate          # Mac / Linux
# venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the dashboard
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**

---

## 📁 Required Input Files

Upload these three CSV files via the **sidebar** in the app.

---

### 1. `deseq2_results.csv` — DESeq2 output

Export from R with:

```r
write.csv(as.data.frame(res_ordered), "deseq2_results.csv", quote = FALSE)
```

Expected columns (DESeq2 standard output):

| Column           | Description                                |
|------------------|--------------------------------------------|
| *(row names)*    | Gene symbol or Ensembl ID                 |
| `baseMean`       | Mean normalized count across all samples  |
| `log2FoldChange` | log₂(Tumor / Normal)                      |
| `lfcSE`          | Standard error of log2FC                  |
| `stat`           | Wald statistic                             |
| `pvalue`         | Raw p-value                                |
| `padj`           | BH-adjusted p-value ← **required**        |

> The first column becomes `gene` after import. Make sure row names are gene IDs.

---

### 2. `normalized_counts.csv` — Normalized count matrix

Export from R with:

```r
norm_counts <- counts(dds, normalized = TRUE)
write.csv(norm_counts, "normalized_counts.csv", quote = FALSE)
```

Expected format:

| *(gene)*   | TCGA-A1-01 | TCGA-A2-01 | … |
|------------|------------|------------|---|
| BRCA1      | 142.3      | 98.7       | … |
| TP53       | 67.1       | 201.4      | … |

- **Rows** = genes (row names are gene IDs)
- **Columns** = sample IDs (must match metadata index)

---

### 3. `sample_metadata.csv` — Sample condition labels

Export from R with:

```r
write.csv(sample_info, "sample_metadata.csv", quote = FALSE)
```

Expected format:

| *(sample)*      | condition |
|-----------------|-----------|
| TCGA-A1-01      | Tumor     |
| TCGA-A1-11      | Normal    |

- **Row names** = sample IDs (must match counts matrix column names)
- **`condition`** column = `"Tumor"` or `"Normal"`

---

## 🖥️ Dashboard Sections

| Tab                        | Description                                          |
|----------------------------|------------------------------------------------------|
| 🏠 Home                   | Project overview, dataset stats, pipeline summary    |
| 📊 Data Overview           | Sample counts, metadata table, expression preview    |
| 🔵 PCA Analysis            | Interactive PCA plot, variance explained             |
| 📋 Differential Expression | Filterable DEG table with up/down coloring           |
| 🌋 Volcano Plot            | Interactive volcano with threshold lines             |
| 🗺️ Heatmap                | Z-score heatmap of top N DE genes                   |
| 🏆 Top Genes               | Top 20 up/downregulated + gene search               |
| 🧪 Biological Interpretation | Pathway and biomarker context                     |
| ⬇️ Downloads              | Export DESeq2 results, top genes, PCA coords        |

---

## 🛠️ Dependencies

| Package       | Version   | Purpose                         |
|---------------|-----------|---------------------------------|
| streamlit     | ≥ 1.32    | Dashboard framework             |
| pandas        | ≥ 2.0     | Data handling                   |
| numpy         | ≥ 1.26    | Numerical operations            |
| plotly        | ≥ 5.20    | Interactive visualizations      |
| scikit-learn  | ≥ 1.4     | PCA computation                 |

---

## 🔧 Troubleshooting

**Heatmap shows no genes**
→ Gene IDs in DESeq2 results and counts matrix must match exactly (both Ensembl
  IDs, or both gene symbols).

**PCA shows "No matching samples"**
→ Column names in `normalized_counts.csv` must exactly match row names in
  `sample_metadata.csv`.

**Slow performance on large counts matrices**
→ Pre-filter to the top 5,000 most variable genes before export, or subsample
  columns to the 100 samples analyzed.

---

*Dashboard built with Streamlit · Plotly · scikit-learn*
