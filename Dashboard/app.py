# ============================================================
# TCGA Breast Cancer RNA-Seq Analysis Dashboard
# Built with Streamlit + Plotly
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import io

# ── Page configuration ──────────────────────────────────────
st.set_page_config(
    page_title="TCGA BRCA RNA-Seq Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    /* Main background */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #8b949e;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
    }
    [data-testid="stSidebar"] .stRadio [aria-checked="true"] + div {
        color: #58a6ff !important;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem;
    }
    [data-testid="metric-container"] label {
        color: #8b949e !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #58a6ff !important;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.6rem !important;
    }

    /* Section headers */
    h1 { color: #f0f6fc !important; font-weight: 700; letter-spacing: -0.02em; }
    h2 { color: #e6edf3 !important; font-weight: 600; border-bottom: 1px solid #30363d; padding-bottom: 0.4rem; }
    h3 { color: #8b949e !important; font-weight: 400; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; }

    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border: 1px solid #30363d;
        border-radius: 8px;
    }

    /* Slider */
    .stSlider [data-baseweb="slider"] { padding: 0.5rem 0; }

    /* Pill badges */
    .badge-tumor {
        display: inline-block; padding: 2px 10px;
        background: #3d1a1a; color: #f85149;
        border: 1px solid #f85149; border-radius: 20px;
        font-size: 0.75rem; font-family: 'IBM Plex Mono', monospace;
    }
    .badge-normal {
        display: inline-block; padding: 2px 10px;
        background: #1a3d2b; color: #3fb950;
        border: 1px solid #3fb950; border-radius: 20px;
        font-size: 0.75rem; font-family: 'IBM Plex Mono', monospace;
    }
    .badge-up {
        display: inline-block; padding: 2px 10px;
        background: #3d1a1a; color: #f85149;
        border: 1px solid #f85149; border-radius: 20px;
        font-size: 0.75rem; font-family: 'IBM Plex Mono', monospace;
    }
    .badge-down {
        display: inline-block; padding: 2px 10px;
        background: #1a2d4d; color: #58a6ff;
        border: 1px solid #58a6ff; border-radius: 20px;
        font-size: 0.75rem; font-family: 'IBM Plex Mono', monospace;
    }

    /* Info boxes */
    .info-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 3px solid #58a6ff;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #8b949e;
    }

    /* Download buttons */
    .stDownloadButton button {
        background: #1f6feb;
        color: white;
        border: none;
        border-radius: 6px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
    }
    .stDownloadButton button:hover {
        background: #388bfd;
    }

    /* Pipeline step */
    .pipeline-step {
        display: flex; align-items: center; gap: 12px;
        padding: 0.6rem 1rem;
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        margin: 0.3rem 0;
        font-size: 0.85rem;
        color: #8b949e;
    }
    .step-num {
        background: #1f6feb;
        color: white;
        width: 22px; height: 22px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem; font-weight: 700;
        flex-shrink: 0;
    }

    /* Search input */
    .stTextInput input {
        background: #161b22;
        border: 1px solid #30363d;
        color: #e6edf3;
        border-radius: 6px;
        font-family: 'IBM Plex Mono', monospace;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: transparent;
        border-bottom: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #8b949e;
        border-radius: 6px 6px 0 0;
        font-size: 0.82rem;
        padding: 0.5rem 1rem;
    }
    .stTabs [aria-selected="true"] {
        background: #161b22 !important;
        color: #58a6ff !important;
        border: 1px solid #30363d;
        border-bottom: 1px solid #0d1117;
    }

    /* Expander */
    [data-testid="stExpander"] {
        border: 1px solid #30363d;
        border-radius: 8px;
        background: #161b22;
    }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ─────────────────────────────────────────────
PLOTLY_THEME = dict(
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    font=dict(family="IBM Plex Sans", color="#8b949e"),
    xaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d", color="#8b949e"),
    yaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d", color="#8b949e"),
    title_font=dict(color="#e6edf3", size=15),
    legend=dict(bgcolor="#161b22", bordercolor="#30363d", borderwidth=1),
)

TUMOR_COLOR  = "#f85149"   # red
NORMAL_COLOR = "#3fb950"   # green
UP_COLOR     = "#f85149"
DOWN_COLOR   = "#58a6ff"
NS_COLOR     = "#3d444d"

# ── Data loading ─────────────────────────────────────────────
@st.cache_data
def load_deseq_results(uploaded_file):
    df = pd.read_csv(uploaded_file, index_col=0)
    df.index.name = "gene"
    df = df.reset_index()
    return df

@st.cache_data
def load_counts_matrix(uploaded_file):
    df = pd.read_csv(uploaded_file, index_col=0)
    return df

@st.cache_data
def load_metadata(uploaded_file):
    df = pd.read_csv(uploaded_file, index_col=0)
    return df

# ── Sidebar navigation ───────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧬 TCGA BRCA")
    st.markdown("<div style='color:#8b949e;font-size:0.75rem;margin-bottom:1.5rem;'>RNA-Seq Analysis Dashboard</div>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "📊 Data Overview",
            "🔵 PCA Analysis",
            "📋 Differential Expression",
            "🌋 Volcano Plot",
            "🗺️ Heatmap",
            "🏆 Top Genes",
            "🧪 Biological Interpretation",
            "⬇️ Downloads",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### Upload Data Files")

    deseq_file   = st.file_uploader("DESeq2 Results CSV",   type="csv", key="deseq")
    counts_file  = st.file_uploader("Normalized Counts CSV", type="csv", key="counts")
    meta_file    = st.file_uploader("Sample Metadata CSV",   type="csv", key="meta")

    # Status indicators
    st.markdown("---")
    st.markdown("<div style='font-size:0.75rem;color:#8b949e;'>FILE STATUS</div>", unsafe_allow_html=True)
    for label, f in [("DESeq2 Results", deseq_file), ("Counts Matrix", counts_file), ("Metadata", meta_file)]:
        icon = "🟢" if f else "⚪"
        st.markdown(f"<div style='font-size:0.8rem;margin:2px 0;'>{icon} {label}</div>", unsafe_allow_html=True)

# ── Load data if available ───────────────────────────────────
deseq_df  = load_deseq_results(deseq_file)   if deseq_file  else None
counts_df = load_counts_matrix(counts_file)  if counts_file else None
meta_df   = load_metadata(meta_file)         if meta_file   else None

# ── Helper: no-data warning ──────────────────────────────────
def require(file_label: str):
    st.warning(f"⬅️ Please upload **{file_label}** in the sidebar to view this section.", icon="📁")

# ============================================================
# PAGE: HOME
# ============================================================
if page == "🏠 Home":
    st.markdown("# 🧬 TCGA Breast Cancer RNA-Seq Analysis")
    st.markdown("<div style='color:#8b949e;font-size:1.05rem;margin-bottom:2rem;'>Differential expression analysis of tumor vs normal tissue using DESeq2 on real TCGA-BRCA data</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Dataset", "TCGA-BRCA")
    with col2:
        n_genes = f"{deseq_df.shape[0]:,}" if deseq_df is not None else "—"
        st.metric("Genes Analyzed", n_genes)
    with col3:
        n_samples = f"{counts_df.shape[1]:,}" if counts_df is not None else "—"
        st.metric("Samples", n_samples)
    with col4:
        if deseq_df is not None and "padj" in deseq_df.columns:
            sig = (deseq_df["padj"] < 0.05).sum()
            st.metric("Significant DEGs", f"{sig:,}")
        else:
            st.metric("Significant DEGs", "—")

    st.markdown("---")
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("## About this Project")
        st.markdown("""
<div class='info-box'>
This dashboard presents a complete RNA-Seq differential expression analysis of
<b style='color:#58a6ff'>TCGA Breast Cancer (BRCA)</b> data obtained from the
UCSC Xena data portal. The analysis compares gene expression profiles between
primary tumor samples and adjacent normal tissue to identify cancer-associated
transcriptional changes.
</div>
""", unsafe_allow_html=True)

        st.markdown("## Dataset Details")
        info = {
            "Source": "UCSC Xena — TCGA-BRCA HiSeqV2",
            "Assay": "RNA-Seq (Illumina HiSeq)",
            "Comparison": "Tumor (01) vs Normal (11)",
            "Pipeline": "DESeq2 v1.40 in R",
            "Normalization": "Variance Stabilizing Transformation (VST)",
        }
        for k, v in info.items():
            st.markdown(f"<div class='pipeline-step'><span style='color:#58a6ff;font-weight:600;width:110px;flex-shrink:0;'>{k}</span>{v}</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("## Analysis Pipeline")
        steps = [
            "Download raw TCGA-BRCA count matrix from UCSC Xena",
            "Identify tumor (01) and normal (11) samples by barcode suffix",
            "Filter low-count genes (rowSums > 10)",
            "Run DESeq2 differential expression analysis",
            "Apply Variance Stabilizing Transformation (VST) for PCA",
            "Generate PCA, Volcano, and Heatmap visualizations",
            "Export results for downstream interpretation",
        ]
        for i, s in enumerate(steps, 1):
            st.markdown(f"<div class='pipeline-step'><span class='step-num'>{i}</span>{s}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='color:#8b949e;font-size:0.78rem;text-align:center;'>Upload your CSV files in the sidebar to activate all interactive sections.</div>", unsafe_allow_html=True)

# ============================================================
# PAGE: DATA OVERVIEW
# ============================================================
elif page == "📊 Data Overview":
    st.markdown("# Data Overview")

    if deseq_df is None and counts_df is None and meta_df is None:
        require("DESeq2 Results, Counts Matrix, and Metadata")
    else:
        if meta_df is not None:
            st.markdown("## Sample Distribution")
            col1, col2, col3 = st.columns(3)
            condition_col = next((c for c in meta_df.columns if "condition" in c.lower() or "type" in c.lower()), meta_df.columns[0])
            counts_by_cond = meta_df[condition_col].value_counts()

            with col1:
                st.metric("Total Samples", len(meta_df))
            with col2:
                t = counts_by_cond.get("Tumor", counts_by_cond.iloc[0])
                st.metric("Tumor Samples", int(t))
            with col3:
                n = counts_by_cond.get("Normal", counts_by_cond.iloc[-1] if len(counts_by_cond) > 1 else 0)
                st.metric("Normal Samples", int(n))

            st.markdown("## Sample Metadata")
            st.dataframe(meta_df, use_container_width=True, height=300)

        if counts_df is not None:
            st.markdown("## Expression Matrix")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Genes (rows)", f"{counts_df.shape[0]:,}")
            with col2:
                st.metric("Samples (cols)", f"{counts_df.shape[1]:,}")

            with st.expander("🔍 Preview expression matrix (first 100 rows)"):
                st.dataframe(counts_df.head(100), use_container_width=True, height=350)

        if deseq_df is not None:
            st.markdown("## DESeq2 Results Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Genes Tested", f"{len(deseq_df):,}")
            if "padj" in deseq_df.columns:
                sig = deseq_df["padj"] < 0.05
                with col2:
                    st.metric("Significant (padj < 0.05)", f"{sig.sum():,}")
            if "log2FoldChange" in deseq_df.columns and "padj" in deseq_df.columns:
                up   = ((deseq_df["log2FoldChange"] > 1) & (deseq_df["padj"] < 0.05)).sum()
                down = ((deseq_df["log2FoldChange"] < -1) & (deseq_df["padj"] < 0.05)).sum()
                with col3:
                    st.metric("Up / Down (|log2FC|>1)", f"{up} / {down}")

# ============================================================
# PAGE: PCA
# ============================================================
elif page == "🔵 PCA Analysis":
    st.markdown("# PCA Analysis")
    st.markdown("<div class='info-box'>Principal Component Analysis (PCA) is used as a quality-control step to assess sample-level separation between tumor and normal groups after Variance Stabilizing Transformation.</div>", unsafe_allow_html=True)

    if counts_df is None or meta_df is None:
        require("Normalized Counts CSV + Metadata CSV")
    else:
        condition_col = next((c for c in meta_df.columns if "condition" in c.lower() or "type" in c.lower()), meta_df.columns[0])

        # Align samples
        common = [s for s in meta_df.index if s in counts_df.columns]
        if not common:
            st.error("No matching sample names between metadata and counts matrix. Check that sample IDs match.")
        else:
            X = counts_df[common].T.fillna(0)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            pca = PCA(n_components=min(10, X_scaled.shape[1]))
            coords = pca.fit_transform(X_scaled)
            var_explained = pca.explained_variance_ratio_ * 100

            pca_plot_df = pd.DataFrame({
                "PC1": coords[:, 0],
                "PC2": coords[:, 1],
                "Sample": common,
                "Condition": meta_df.loc[common, condition_col].values,
            })

            col_slider, _ = st.columns([1, 3])
            with col_slider:
                point_size = st.slider("Point size", 4, 20, 9)

            color_map = {"Tumor": TUMOR_COLOR, "Normal": NORMAL_COLOR}
            # Fallback for arbitrary condition names
            unique_conds = pca_plot_df["Condition"].unique()
            if len(unique_conds) == 2 and not all(c in color_map for c in unique_conds):
                color_map = {unique_conds[0]: TUMOR_COLOR, unique_conds[1]: NORMAL_COLOR}

            fig = px.scatter(
                pca_plot_df, x="PC1", y="PC2",
                color="Condition",
                color_discrete_map=color_map,
                hover_data={"Sample": True, "PC1": ":.2f", "PC2": ":.2f"},
                labels={
                    "PC1": f"PC1 ({var_explained[0]:.1f}% variance)",
                    "PC2": f"PC2 ({var_explained[1]:.1f}% variance)",
                },
                title="PCA — Tumor vs Normal",
            )
            fig.update_traces(marker=dict(size=point_size, opacity=0.85, line=dict(width=0.5, color="#0d1117")))
            fig.update_layout(**PLOTLY_THEME, height=520)
            st.plotly_chart(fig, use_container_width=True)

            # Variance explained bar chart
            n_pcs = min(10, len(var_explained))
            var_df = pd.DataFrame({"PC": [f"PC{i+1}" for i in range(n_pcs)], "Variance (%)": var_explained[:n_pcs]})
            fig2 = px.bar(var_df, x="PC", y="Variance (%)", title="Variance Explained per PC",
                          color_discrete_sequence=["#1f6feb"])
            fig2.update_layout(**PLOTLY_THEME, height=280, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

            with st.expander("PCA coordinates table"):
                st.dataframe(pca_plot_df, use_container_width=True)

# ============================================================
# PAGE: DIFFERENTIAL EXPRESSION
# ============================================================
elif page == "📋 Differential Expression":
    st.markdown("# Differential Expression Results")

    if deseq_df is None:
        require("DESeq2 Results CSV")
    else:
        required_cols = {"log2FoldChange", "padj"}
        if not required_cols.issubset(deseq_df.columns):
            st.error(f"DESeq2 results must contain columns: {required_cols}. Found: {list(deseq_df.columns)}")
        else:
            col1, col2 = st.columns(2)
            with col1:
                lfc_thresh = st.slider("log₂ Fold Change threshold (|log2FC| ≥)", 0.0, 5.0, 1.0, 0.1)
            with col2:
                padj_thresh = st.slider("Adjusted p-value threshold (padj ≤)", 0.001, 0.5, 0.05, 0.001, format="%.3f")

            df = deseq_df.copy().dropna(subset=["padj", "log2FoldChange"])
            mask_up   = (df["log2FoldChange"] >=  lfc_thresh) & (df["padj"] <= padj_thresh)
            mask_down = (df["log2FoldChange"] <= -lfc_thresh) & (df["padj"] <= padj_thresh)
            df["Regulation"] = "Not Significant"
            df.loc[mask_up,   "Regulation"] = "Upregulated"
            df.loc[mask_down, "Regulation"] = "Downregulated"

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Upregulated",   int(mask_up.sum()),   delta=None)
            with col2:
                st.metric("Downregulated", int(mask_down.sum()), delta=None)
            with col3:
                st.metric("Not Significant", int((df["Regulation"] == "Not Significant").sum()))

            # Color-styled display
            show_cols = ["gene", "log2FoldChange", "padj", "Regulation"] if "gene" in df.columns else ["log2FoldChange", "padj", "Regulation"]
            display_df = df[show_cols].sort_values("padj")

            def color_regulation(val):
                if val == "Upregulated":
                    return "color: #f85149"
                elif val == "Downregulated":
                    return "color: #58a6ff"
                return "color: #3d444d"

            styled = display_df.style.applymap(color_regulation, subset=["Regulation"])
            st.dataframe(styled, use_container_width=True, height=450)

# ============================================================
# PAGE: VOLCANO PLOT
# ============================================================
elif page == "🌋 Volcano Plot":
    st.markdown("# Volcano Plot")
    st.markdown("<div class='info-box'>Each point represents a gene. X-axis: log₂ fold change (Tumor / Normal). Y-axis: −log₁₀ adjusted p-value. Dashed lines mark the significance thresholds.</div>", unsafe_allow_html=True)

    if deseq_df is None:
        require("DESeq2 Results CSV")
    else:
        required_cols = {"log2FoldChange", "padj"}
        if not required_cols.issubset(deseq_df.columns):
            st.error(f"Columns required: {required_cols}")
        else:
            col1, col2 = st.columns(2)
            with col1:
                lfc_thresh = st.slider("log₂FC threshold", 0.0, 5.0, 1.0, 0.1, key="vlfc")
            with col2:
                padj_thresh = st.slider("padj threshold", 0.001, 0.5, 0.05, 0.001, key="vpadj", format="%.3f")

            df = deseq_df.dropna(subset=["padj", "log2FoldChange"]).copy()
            df["neg_log10_padj"] = -np.log10(df["padj"].clip(lower=1e-300))

            def label_gene(row):
                if row["log2FoldChange"] >= lfc_thresh and row["padj"] <= padj_thresh:
                    return "Upregulated"
                elif row["log2FoldChange"] <= -lfc_thresh and row["padj"] <= padj_thresh:
                    return "Downregulated"
                return "Not Significant"

            df["Category"] = df.apply(label_gene, axis=1)

            color_map = {"Upregulated": UP_COLOR, "Downregulated": DOWN_COLOR, "Not Significant": NS_COLOR}
            gene_col  = "gene" if "gene" in df.columns else df.index.name or df.columns[0]

            hover_cols = {gene_col: True, "log2FoldChange": ":.3f", "padj": ":.2e", "Category": True}

            fig = px.scatter(
                df, x="log2FoldChange", y="neg_log10_padj",
                color="Category",
                color_discrete_map=color_map,
                hover_data=hover_cols,
                labels={"log2FoldChange": "log₂ Fold Change", "neg_log10_padj": "−log₁₀(padj)"},
                title="Volcano Plot — Tumor vs Normal",
                opacity=0.75,
            )
            fig.update_traces(marker=dict(size=5))

            # Threshold lines
            fig.add_vline(x= lfc_thresh,  line_dash="dash", line_color="#58a6ff", line_width=1, opacity=0.6)
            fig.add_vline(x=-lfc_thresh,  line_dash="dash", line_color="#58a6ff", line_width=1, opacity=0.6)
            fig.add_hline(y=-np.log10(padj_thresh), line_dash="dash", line_color="#f0883e", line_width=1, opacity=0.6)

            fig.update_layout(**PLOTLY_THEME, height=580)
            st.plotly_chart(fig, use_container_width=True)

            counts = df["Category"].value_counts()
            c1, c2, c3 = st.columns(3)
            c1.metric("Upregulated",    counts.get("Upregulated", 0))
            c2.metric("Downregulated",  counts.get("Downregulated", 0))
            c3.metric("Not Significant",counts.get("Not Significant", 0))

# ============================================================
# PAGE: HEATMAP
# ============================================================
elif page == "🗺️ Heatmap":
    st.markdown("# Expression Heatmap")
    st.markdown("<div class='info-box'>Z-score normalized expression of the top differentially expressed genes across all samples. Blue = low, Red = high expression.</div>", unsafe_allow_html=True)

    if deseq_df is None or counts_df is None:
        require("DESeq2 Results CSV + Normalized Counts CSV")
    else:
        n_genes = st.slider("Number of top DE genes", 10, 100, 50, 5)

        # Get top genes by padj
        top_gene_col = "gene" if "gene" in deseq_df.columns else None
        de = deseq_df.dropna(subset=["padj"]).sort_values("padj")
        if top_gene_col:
            top_genes = de[top_gene_col].head(n_genes).tolist()
        else:
            top_genes = de.index.head(n_genes).tolist()

        # Filter counts to available top genes
        available = [g for g in top_genes if g in counts_df.index]
        if not available:
            st.error("None of the top DE genes were found as row names in the counts matrix. Check that gene IDs match.")
        else:
            sub = counts_df.loc[available]
            log_counts = np.log2(sub + 1)
            # Z-score per gene
            zscore = log_counts.subtract(log_counts.mean(axis=1), axis=0).divide(log_counts.std(axis=1).replace(0, 1), axis=0)

            fig = go.Figure(data=go.Heatmap(
                z=zscore.values,
                x=zscore.columns.tolist(),
                y=zscore.index.tolist(),
                colorscale=[
                    [0.0,  "#1f6feb"],
                    [0.5,  "#0d1117"],
                    [1.0,  "#f85149"],
                ],
                colorbar=dict(title="Z-score", tickfont=dict(color="#8b949e")),
                hovertemplate="Sample: %{x}<br>Gene: %{y}<br>Z-score: %{z:.2f}<extra></extra>",
            ))
            fig.update_layout(
                **PLOTLY_THEME,
                height=max(450, n_genes * 12),
                xaxis=dict(showticklabels=False, title="Samples"),
                yaxis=dict(title="Genes", tickfont=dict(size=9)),
                title=f"Top {len(available)} DE Genes — Z-score Heatmap",
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PAGE: TOP GENES
# ============================================================
elif page == "🏆 Top Genes":
    st.markdown("# Top Differentially Expressed Genes")

    if deseq_df is None:
        require("DESeq2 Results CSV")
    else:
        required_cols = {"log2FoldChange", "padj"}
        if not required_cols.issubset(deseq_df.columns):
            st.error(f"Columns required: {required_cols}")
        else:
            gene_col = "gene" if "gene" in deseq_df.columns else None
            df = deseq_df.dropna(subset=["padj", "log2FoldChange"]).copy()

            search = st.text_input("🔍 Search gene name", placeholder="e.g. BRCA1, ERBB2, MKI67 …")

            if search and gene_col:
                result = df[df[gene_col].str.contains(search, case=False, na=False)]
                st.markdown(f"**{len(result)} result(s) for '{search}'**")
                st.dataframe(result[[gene_col, "log2FoldChange", "padj"]].style.format(
                    {"log2FoldChange": "{:.3f}", "padj": "{:.2e}"}), use_container_width=True)
                st.markdown("---")

            col1, col2 = st.columns(2)

            sig = df[df["padj"] < 0.05].copy()
            top_up   = sig[sig["log2FoldChange"] > 0].nlargest(20, "log2FoldChange")
            top_down = sig[sig["log2FoldChange"] < 0].nsmallest(20, "log2FoldChange")

            display_cols = ([gene_col] if gene_col else []) + ["log2FoldChange", "padj"]

            with col1:
                st.markdown("### 🔴 Top 20 Upregulated")
                st.dataframe(
                    top_up[display_cols].style
                    .format({"log2FoldChange": "{:.3f}", "padj": "{:.2e}"})
                    .background_gradient(subset=["log2FoldChange"], cmap="Reds"),
                    use_container_width=True, height=450,
                )

            with col2:
                st.markdown("### 🔵 Top 20 Downregulated")
                st.dataframe(
                    top_down[display_cols].style
                    .format({"log2FoldChange": "{:.3f}", "padj": "{:.2e}"})
                    .background_gradient(subset=["log2FoldChange"], cmap="Blues_r"),
                    use_container_width=True, height=450,
                )

            # Bar chart
            st.markdown("## Fold Change Overview")
            top_both = pd.concat([top_up.head(10), top_down.head(10)])
            if gene_col:
                top_both["label"] = top_both[gene_col]
            else:
                top_both["label"] = top_both.index.astype(str)
            top_both = top_both.sort_values("log2FoldChange")
            top_both["color"] = top_both["log2FoldChange"].apply(lambda x: UP_COLOR if x > 0 else DOWN_COLOR)

            fig = go.Figure(go.Bar(
                x=top_both["log2FoldChange"],
                y=top_both["label"],
                orientation="h",
                marker_color=top_both["color"],
                hovertemplate="%{y}: %{x:.3f}<extra></extra>",
            ))
            fig.update_layout(**PLOTLY_THEME, height=500, xaxis_title="log₂ Fold Change", yaxis_title="", title="Top 10 Up & Downregulated Genes")
            st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PAGE: BIOLOGICAL INTERPRETATION
# ============================================================
elif page == "🧪 Biological Interpretation":
    st.markdown("# Biological Interpretation")

    sections = [
        (
            "🔴 Upregulated Genes in Tumor",
            "Genes overexpressed in tumor tissue typically reflect core hallmarks of cancer: uncontrolled proliferation, cell cycle dysregulation, and evasion of apoptosis. Common findings in breast cancer include elevated expression of <b>MKI67</b> (proliferation marker), <b>TOP2A</b> (DNA replication), <b>AURKA/B</b> (mitotic kinases), and <b>CCNB1/2</b> (cyclins). These genes collectively indicate a highly proliferative tumor phenotype.",
        ),
        (
            "🔵 Downregulated Genes in Tumor",
            "Loss of expression in tumor tissue often reflects silencing of tumor suppressors, differentiation markers, and stromal components. Downregulated genes may include <b>ESR1</b> (estrogen receptor — relevant for ER-negative subtypes), <b>FOXA1</b>, <b>GATA3</b>, and various extracellular matrix genes. Epigenetic silencing via promoter methylation is a frequent mechanism.",
        ),
        (
            "🧬 Cancer-Related Pathways",
            """Common pathways enriched among differentially expressed genes in TCGA-BRCA:
            <ul style='color:#8b949e;margin-top:0.5rem;'>
            <li><b style='color:#58a6ff'>Cell cycle regulation</b> — CDK1, CCNB1, CDC20, BUB1 (G2/M checkpoint)</li>
            <li><b style='color:#58a6ff'>PI3K/AKT/mTOR signaling</b> — frequently activated in luminal subtypes</li>
            <li><b style='color:#58a6ff'>HER2 (ERBB2) signaling</b> — amplified in ~20% of breast cancers</li>
            <li><b style='color:#58a6ff'>Immune evasion</b> — altered expression of MHC-I genes and PD-L1</li>
            <li><b style='color:#58a6ff'>ECM remodeling</b> — MMP family, collagen genes, integrins</li>
            <li><b style='color:#58a6ff'>p53 pathway</b> — TP53 mutations are common in basal-like subtype</li>
            </ul>""",
        ),
        (
            "🏷️ Biomarker Relevance",
            "Several DE genes identified in this analysis correspond to established breast cancer biomarkers used clinically: <b>ESR1</b> (ER status), <b>PGR</b> (PR status), <b>ERBB2</b> (HER2 status), and <b>MKI67</b> (proliferation index in Ki-67 assay). These markers guide treatment decisions including endocrine therapy, HER2-targeted therapy, and chemotherapy selection.",
        ),
        (
            "⚠️ Interpretation Notes",
            "This analysis uses a subset of 50 tumor and up to 50 normal samples for computational efficiency. Results are consistent with published TCGA-BRCA literature. Pathway enrichment tools (GSEA, Enrichr, g:Profiler) should be applied to the full DEG list for rigorous functional interpretation. Findings should not be used for clinical decision-making without further validation.",
        ),
    ]

    for title, body in sections:
        st.markdown(f"## {title}")
        st.markdown(f"<div class='info-box'>{body}</div>", unsafe_allow_html=True)
        st.markdown("")

# ============================================================
# PAGE: DOWNLOADS
# ============================================================
elif page == "⬇️ Downloads":
    st.markdown("# Download Results")
    st.markdown("<div class='info-box'>Export analysis results as CSV files for downstream analysis, pathway enrichment, or reporting.</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── DESeq2 results ──────────────────────────────────────
    st.markdown("### 📄 DESeq2 Differential Expression Results")
    if deseq_df is not None:
        csv1 = deseq_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download DESeq2 Results (full)", csv1, "deseq2_results.csv", "text/csv")
    else:
        st.markdown("<div style='color:#8b949e;font-size:0.85rem;'>Upload DESeq2 Results CSV to enable this download.</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Top 50 genes ────────────────────────────────────────
    st.markdown("### 🏆 Top 50 DE Genes")
    if deseq_df is not None and "padj" in deseq_df.columns:
        top50 = deseq_df.dropna(subset=["padj"]).sort_values("padj").head(50)
        csv2 = top50.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Top 50 Genes", csv2, "top50_DE_genes.csv", "text/csv")
        with st.expander("Preview top 50 genes"):
            st.dataframe(top50, use_container_width=True)
    else:
        st.markdown("<div style='color:#8b949e;font-size:0.85rem;'>Upload DESeq2 Results CSV to enable this download.</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── PCA coordinates ─────────────────────────────────────
    st.markdown("### 🔵 PCA Coordinates")
    if counts_df is not None and meta_df is not None:
        condition_col = next((c for c in meta_df.columns if "condition" in c.lower() or "type" in c.lower()), meta_df.columns[0])
        common = [s for s in meta_df.index if s in counts_df.columns]
        if common:
            X = counts_df[common].T.fillna(0)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            pca = PCA(n_components=min(10, X_scaled.shape[1]))
            coords = pca.fit_transform(X_scaled)
            pca_df = pd.DataFrame(coords[:, :10], index=common,
                                  columns=[f"PC{i+1}" for i in range(min(10, coords.shape[1]))])
            pca_df.insert(0, "Condition", meta_df.loc[common, condition_col].values)
            csv3 = pca_df.to_csv().encode("utf-8")
            st.download_button("⬇️ Download PCA Coordinates", csv3, "pca_coordinates.csv", "text/csv")
        else:
            st.markdown("<div style='color:#8b949e;font-size:0.85rem;'>No matching samples found between counts and metadata.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#8b949e;font-size:0.85rem;'>Upload Normalized Counts + Metadata to enable this download.</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='color:#8b949e;font-size:0.78rem;'>All downloads are generated from your uploaded data files at runtime. No data is stored on any server.</div>", unsafe_allow_html=True)
