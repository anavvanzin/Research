# Design Spec: New Corpus Statistical Analysis (05–07)

**Date:** 2026-04-17
**Status:** Approved — ready for implementation
**Author:** Ana Vanzin + Hermes Agent

## Context

The ICONOCRACY thesis (PPGD/UFSC) has 4 existing statistical notebooks (01–04) covering Chapter 6: descriptive stats, Kruskal-Wallis, OLS regression, and MCA. These are fully executed and thesis-ready.

The `corpus-data.json` (165 items) contains temporal (`year`), geographic (`country`), material (`medium_norm`), and indicator (`indicadores` — 10 ordinal 0–3 fields) data that the existing notebooks do not analyze. Three new analyses fill these gaps.

A preliminary correlation analysis revealed that `monocromatizacao` correlates weakly with all other indicators (rho 0.08–0.36), suggesting ENDURECIMENTO may not be a single dimension. This finding drives the clustering and PCA analyses.

## Data

- **Source:** `corpus/corpus-data.json` (165 items)
- **Year coverage:** 159/165 items (96%), range 1239–1975
- **Indicator coverage:** 146/165 items with complete 10/10 indicators (all 0–3 integer scale)
- **Temporal density:** uneven — pre-1850 decades have 1–3 items; 1850s–1970s have 4–32 items per decade
- **1910s spike:** 32 items, 23 militar regime (WWI-era)

## Notebooks

### 05_temporal.ipynb — Temporal Dynamics

**Purpose:** Descriptive temporal analysis of regime distribution and ENDURECIMENTO over time. Frame as illustrative, not inferential (selection bias, sparse early periods).

| Cell | Type | Content | Output |
|------|------|---------|--------|
| 1 | Code | Setup + data load → 159 items with year, decade bins | — |
| 2 | Code | Regime stacked bar chart (1850s–1970s), annotate 1910s militar spike | `fig_06_regime_timeline.png` |
| 3 | Code | ENDURECIMENTO mean per decade (error bars = std), secondary axis = item count | `fig_07_endurecimento_trend.png` |
| 4 | Code | Country × decade heatmap (which countries appear when) | `fig_08_country_timeline.png` |
| 5 | Code | Medium_norm stacked bar over decades (stamps vs paintings vs sculpture) | `fig_09_medium_timeline.png` |
| 6 | Markdown | Summary: key regime transitions, WWI context, historiographic notes | — |

**Constraints:**
- No p-values or trend regression on pre-1850 data
- Suppress error bars on decades with <5 items
- Annotate WWI context on 1910s

### 06_clustering.ipynb — Indicator Structure & Clustering

**Purpose:** Validate regime taxonomy via unsupervised clustering. Investigate monocromatizacao as structural outlier.

| Cell | Type | Content | Output |
|------|------|---------|--------|
| 1 | Code | Setup + load 146 items × 10 indicators + regime/scope_role metadata | — |
| 2 | Code | Full Spearman heatmap (10×10), highlight monocromatizacao outlier | `fig_10_indicator_correlation.png` |
| 3 | Code | Hierarchical clustering (ward linkage, euclidean), dendrogram colored by regime, silhouette k=2..8 | `fig_11_dendrogram.png`, `fig_12_silhouette.png` |
| 4 | Code | Cut at optimal k, cross-tab cluster × regime, chi-squared + Cramér's V | — |
| 5 | Code | K-means k=2..8, compare with hierarchical via Adjusted Rand Index | — |
| 6 | Code | Cluster profiles: mean indicator values per cluster (grouped bar) | `fig_13_cluster_profiles.png` |
| 7 | Code | Recluster WITHOUT monocromatizacao — does structure change? | — |
| 8 | Code | Outlier detection: items with lowest silhouette scores, list IDs | — |
| 9 | Code | Cross-tab cluster × scope_role (do comparanda cluster separately?) | — |

**Methods:**
- `scipy.cluster.hierarchy.linkage(method='ward')`
- `sklearn.cluster.AgglomerativeClustering` for cut
- `sklearn.metrics.silhouette_score` for k selection
- `sklearn.cluster.KMeans` for validation
- `sklearn.metrics.adjusted_rand_score` for agreement

### 07_dimensionality.ipynb — PCA / Dimensionality Check

**Purpose:** Confirm or challenge single-dimension assumption behind ENDURECIMENTO composite scores.

| Cell | Type | Content | Output |
|------|------|---------|--------|
| 1 | Code | Setup + same 146 × 10 matrix as 06 | — |
| 2 | Code | PCA fit, scree plot (eigenvalues + cumulative variance), components for 80%/90% | `fig_14_scree.png` |
| 3 | Code | Loadings heatmap (indicators × components), print loadings table | `fig_15_loadings.png` |
| 4 | Code | PCA biplot: items on PC1 vs PC2, colored by regime | `fig_16_pca_biplot.png` |
| 5 | Markdown | Implications: does composite score hide multi-dimensional structure? | — |

**Methods:**
- `sklearn.decomposition.PCA`
- StandardScaler normalization before PCA (despite same 0–3 scale, PCA benefits from standardization)
- `sklearn.preprocessing.StandardScaler`

## Output Files

All figures saved to `data/processed/` following existing convention:
- `fig_06_regime_timeline.png` through `fig_16_pca_biplot.png`
- DPI 150, bbox_inches='tight' (matches existing notebook convention)

## Dependencies

Standard conda `iconocracy` environment:
- pandas, numpy, scipy, scikit-learn, matplotlib, seaborn
- All already installed (used by existing notebooks 01–04)

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Pre-1850 data too sparse for temporal analysis | Misleading trend lines | Suppress stats on sparse decades; mark as illustrative only |
| Monocromatizacao dominates PCA | PCA uninterpretable | Test with and without; if it hijacks PC1, report both |
| Clustering finds no meaningful structure | Wasted analysis | Still valuable — report that regimes don't cluster, discuss implications |
| Selection bias in corpus | Temporal findings reflect archival availability, not history | Explicitly state this limitation in summary cell |
