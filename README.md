# cellgrowth

A Python package for reproducible analysis and interactive visualization of cell growth data exported from high-content imaging plate readers.

---

## Background

Quantitative measurement of cell proliferation is central to a wide range of biomedical studies, from drug-response assays to cell-biology mechanistic research. High-content imaging (HCI) systems — such as the PerkinElmer Operetta/Opera — automatically acquire and segment images across multi-well plates over time, generating rich per-well metrics (cell count, morphology, texture, area) at each timepoint.

Despite the volume and quality of data these instruments produce, the analysis bottleneck lies **downstream** of the instrument software: researchers must manually export tabular data, wrangle timepoint metadata, aggregate replicates, compute statistics, and build publication-ready figures. This process is typically done in spreadsheets or with one-off scripts, making it difficult to reproduce, share, or scale.

Existing tools such as [CellProfiler](https://cellprofiler.org/) (Stirling *et al.*, 2021, *PLOS Biology*) are powerful pipelines for **image segmentation and feature extraction**, but they are not designed for the **downstream statistical aggregation and interactive visualization** of already-extracted plate-reader exports. General-purpose data-science libraries (pandas, matplotlib) require substantial boilerplate to handle the plate-map conventions (row-letter/column-number addressing), multi-timepoint structures, and per-sample grouping that HCI experiments produce.

**`cellgrowth`** fills this gap: it provides a lightweight, Jupyter-friendly Python layer that takes raw plate-reader exports and delivers clean, grouped, statistically annotated dataframes and interactive figures — with minimal code.

---

## Solution

`cellgrowth` sits between the instrument export and final reporting. It:

1. Reads the tabular `.txt` export produced by plate-reader software.
2. Converts raw timepoint indices to real elapsed hours, aligns well addresses to standard plate-map notation, and optionally reorders samples.
3. Aggregates replicate wells by sample and timepoint, computing means and standard deviations in a single call.
4. Renders interactive Plotly line graphs with dynamically toggled error bars, fully configurable axis and layout parameters, and colour-coded sample traces.

---

## Key Features

- **`DataProcessing` class**
  - `process_timepoints()` — converts raw timepoint indices to elapsed hours, sorts wells by row/column, and concatenates results into a tidy dataframe.
  - `grouped()` — auto-detects numerical columns, generates error-bar columns, and produces a grouped statistics table (mean ± SD per sample per timepoint) with a single method call.
- **`Graph` class**
  - `line_graph()` — creates an interactive Plotly line graph from a grouped dataframe; mirrors the full `px.line()` signature.
  - `update_parameters()` — update x-axis, y-axis, and layout settings at any point before or after the figure is created, without rebuilding the graph.
  - `add_toggle()` — dynamically attach or remove an error-bar on/off toggle button; works for any set of samples without hard-coding names.
- **Utility functions**
  - `map_num_to_letter()` — maps integer row indices to plate-map letter notation (A–Z).
  - `sample_order_sorter()` — reorders samples in a dataframe to a user-defined sequence, independent of original data ordering.
- **Jupyter-first workflow** — all classes and functions are designed to be used interactively in notebooks, returning figures and dataframes rather than rendering them implicitly.

---

## Installation

### Requirements

- Python ≥ 3.10
- Dependencies (installed automatically):

| Package | Version |
|---|---|
| pandas | ≥ 2.3.1 |
| numpy | ≥ 1.26.4 |
| plotly | ≥ 5.0.0 |
| matplotlib | ≥ 3.10.5 |
| seaborn | ≥ 0.13.2 |
| scipy | ≥ 1.15.2 |
| statsmodels | ≥ 0.14.0 |
| mplcursors | ≥ 0.5 |
| ipython | ≥ 7.0 |

### Install from source

```bash
git clone https://github.com/your-username/cell-growth-analyzer.git
cd cell-growth-analyzer
pip install .
```

Or install in editable mode during development:

```bash
pip install -e .
```

---

## Usage

Clone the repository and explore the analysis using the provided Jupyter notebook and sample dataset:

```bash
git clone https://github.com/your-username/cell-growth-analyzer.git
cd cell-growth-analyzer
jupyter notebook notebooks/cell_growth_visualization.ipynb
```

The notebook walks through the full workflow using a real plate-reader export located in `data/cell_growth_data.txt`:

```python
from cellgrowth.core import DataProcessing, Graph

# Load and process data
dp = DataProcessing(df)
df = dp.process_timepoints()
df_grouped = dp.grouped()

# Build an interactive line graph
g = Graph()
fig = g.line_graph(
    df_grouped=df_grouped,
    x="Hours",
    y="Texture A Selected - Region Area [µm²] - Sum per Well",
    color="Sample",
    color_discrete_map={"Neg Control": "black", "Parental": "green",
                        "LOW_uptake": "blue", "HIGH_uptake": "red"},
    error_y="cell_covered_area_std",
)

# Customize axes
g.update_parameters(
    xaxis={"range": (0, 100), "title_text": "Time (h)"},
    yaxis={"title_text": "Plate-well surface area covered by cell"},
    layout={"title": {"text": "Cell Growth Over Time", "font_size": 28, "x": 0.5}},
)

# Add/remove error-bar toggle button
g.add_toggle(df_grouped, error_col="cell_covered_area_std", color_col="Sample", show=True)

fig.show()
```

---

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

This project is funded by Marie Curie Actions under the European Union's Horizon 2020 research and innovation programme for project **proEVLifeCycle**, grant No **860303**.

Special thanks to the developers of [pandas](https://pandas.pydata.org/), [Plotly](https://plotly.com/python/), [NumPy](https://numpy.org/), [SciPy](https://scipy.org/), [statsmodels](https://www.statsmodels.org/), [Matplotlib](https://matplotlib.org/), and [Seaborn](https://seaborn.pydata.org/), whose open-source libraries form the analytical and visualisation backbone of this package.
