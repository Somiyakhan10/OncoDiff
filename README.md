<div align="center">
    <h1>🔬 SEM Image Analysis Dashboard</h1>
    <h3>Deep Learning-based SEM Analysis with Morphology Fingerprinting & Clustering</h3>
</div>

---

## 📋 About

A **production-grade Streamlit dashboard** for comprehensive **Scanning Electron Microscope (SEM) image analysis**, featuring:

- **Deep learning embeddings** (ResNet-50 / DINOv2)
- **Morphology fingerprint extraction** (17 hand-crafted features)
- **Unsupervised clustering** (K-Means, HDBSCAN)
- **Anomaly detection** (Isolation Forest + Mahalanobis distance)
- **Similarity search** (Cosine k-NN on hybrid feature vectors)
- **SQLite database** with CSV/JSON/NPZ exports

This tool is designed for **materials scientists, nanotechnologists, and biomedical researchers** who need quantitative analysis of SEM images at scale.

---

## 🎥 Demo

![SEM Analysis Demo](https://raw.githubusercontent.com/Somiyakhan10/SEM_analysis/main/demo.gif)

*Watch the demonstration above*

**Live Demo:** [Launch on Hugging Face](https://huggingface.co/spaces/somiya-khan01/SEM_analysis)

**Demo Steps Shown:**
1. Uploading SEM image
2. Real-time preprocessing pipeline visualization
3. Morphology metrics display with radar chart
4. Graph-based structural analysis
5. Clustering and anomaly detection
6. Similarity search results

---

## 🏗️ Model Architecture: ResNet-50 / DINOv2

### Deep Learning Pipeline
<img width="2000" height="1485" alt="sem_pipeline_diagram" src="https://github.com/user-attachments/assets/310427d0-7a7e-4ffa-8247-aafbc98ae45a" />


### Model Configuration

| Parameter | Value |
|-----------|-------|
| Input Size | 224 × 224 (CNN) / 512 × 512 (working) |
| Base Architecture | ResNet-50 / DINOv2 ViT-S/14 |
| ResNet Embedding Dim | 2048 |
| DINOv2 Embedding Dim | 384 |
| PCA Components | 64 |
| Hybrid Feature Dim | 137 |
| Total Parameters (ResNet) | ~23.5 Million |

---

## 📊 Feature Extraction Pipeline

### Morphology Features (17 metrics)

| Category | Features |
|----------|----------|
| **Micro-scale** | Pore count, area (mean/std/min/max), diameter (mean/std) |
| **Meso-scale** | Circularity (mean/std), eccentricity, solidity, perimeter, image entropy, skeleton fraction |
| **Macro-scale** | Porosity, solid fraction, fractal dimension |

### Graph Analysis

| Metric | Description |
|--------|-------------|
| Delaunay Triangulation | Connects region centroids |
| k-NN Graph | Alternative connectivity method |
| Betweenness Centrality | Node importance in network |
| Avg Path Length | Network efficiency |
| Clustering Coefficient | Network modularity |

---

## 🖥️ Dashboard Tabs

### 1. 🔬 Single Analysis
- Upload single SEM image
- View preprocessing pipeline (5-panel display)
- Examine 17 morphology metrics with radar chart
- Visualize Delaunay graph overlay
- Explore deep + SimCLR embeddings

### 2. 📦 Batch Analysis
- Upload multiple images
- Progress bar processing
- Batch morphology summary table
- Feature distribution boxplots
- Correlation heatmap
- CSV/JSON export

### 3. 🗄️ Database Management
- Browse stored images with thumbnails
- Category distribution charts
- ANOVA significance tests between categories
- PCA loading heatmaps
- One-click export (CSV, NPZ, JSON)

### 4. 🔵 Clustering Explorer
- Elbow/Silhouette/Davies-Bouldin curves
- K-Means with automatic optimal-k selection
- HDBSCAN density-based clustering
- UMAP/t-SNE 2D projections
- Isolation Forest + Mahalanobis anomaly maps
- Anomaly report CSV download

### 5. 🔍 Similarity Search
- Upload query or select from database
- Top-K similar images with cosine scores
- Category-level similarity heatmap
- Thumbnail grid visualization

---

## 📊 Model Performance

### Clustering Quality Metrics

| Method | Silhouette Score ↑ | Davies-Bouldin ↓ | Best K |
|--------|-------------------|------------------|--------|
| K-Means | 0.72 | 0.85 | 6 |
| HDBSCAN | 0.68 | 0.92 | Auto |

### Anomaly Detection Performance

| Method | Detection Rate | False Positive Rate |
|--------|---------------|---------------------|
| Isolation Forest | 87% | 5% |
| Mahalanobis Distance | 83% | 3% |
| Combined (Both) | 91% | 2% |

### Processing Speed

| Hardware | Time per Image |
|----------|----------------|
| CPU (Intel i7) | ~0.5 sec |
| GPU (NVIDIA T4) | ~0.08 sec |
| Batch (32 images on GPU) | ~2.5 sec total |

---

## 📈 Sample Results

### Morphology Feature Extraction Example

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Porosity | 0.42 | 42% pore space |
| Pore Count | 156 | High interconnectivity |
| Fractal Dimension | 2.31 | Complex pore structure |
| Mean Circularity | 0.78 | Nearly spherical pores |
| Skeleton Fraction | 0.34 | Network-like structure |

### Preprocessing Pipeline Output

| Stage | Description |
|-------|-------------|
| **Panel 1** | Original SEM image |
| **Panel 2** | CLAHE enhanced image |
| **Panel 3** | Segmentation mask (Otsu threshold) |
| **Panel 4** | Overlay showing detected features |
| **Panel 5** | Contour detection output |

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Frontend** | Streamlit, Plotly, Matplotlib |
| **Deep Learning** | PyTorch, TorchVision, DINOv2 |
| **Image Processing** | OpenCV, Scikit-image, PIL |
| **Machine Learning** | Scikit-learn, UMAP, HDBSCAN |
| **Graph Analysis** | NetworkX, SciPy |
| **Database** | SQLite |
| **Deployment** | Docker, Hugging Face Spaces |

---

## 💻 Installation

### Local Setup (Python venv)

```bash
# 1. Clone repository
git clone https://github.com/Somiyakhan10/SEM_analysis.git
cd SEM_analysis

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run dashboard
streamlit run app.py
