# High-Throughput Compound Screening Analysis

## Background

High-throughput compound screening (HTS) is a cornerstone of modern drug discovery, enabling researchers to test thousands of small molecules against a biological target in a short period of time. Despite the scale and complexity of HTS experiments, the bioinformatics tooling available to biologists remains fragmented. Most existing solutions are either tied to proprietary instrument software, require extensive programming expertise, or lack the flexibility to handle the full analytical pipeline — from raw plate reader output to biologically interpretable hits. As a result, researchers frequently rely on ad-hoc spreadsheet workflows that are difficult to reproduce, error-prone, and poorly suited to multi-plate experiments where systematic plate-to-plate variation can confound results.

## Solution

This package provides a lightweight, open-source Python library purpose-built for end-to-end HTS data analysis. It takes raw tab-separated output files directly from plate readers and carries them through cleaning, normalization, hit classification, and visualization — all within a reproducible, notebook-friendly workflow. By encoding domain-specific knowledge (plate layouts, control well positions, normalization strategies, and hit thresholds) into well-documented functions and classes, the package removes the need for manual data wrangling and makes screening analyses transparent and repeatable across experiments.

## Key Features

- **Multi-plate data loading** — Ingests raw `PlateResults.txt` files from multiple measurement folders and concatenates them into a single structured DataFrame, with automatic plate ID tracking.
- **Plate-to-plate normalization** — Corrects for systematic inter-plate variation by computing per-plate normalization factors from the untreated control group and applying them consistently across both control and compound-treated samples.
- **SD-based hit classification** — The `Categorizer` class automatically determines upper and lower thresholds (mean/median ± N standard deviations) from the control population and classifies each compound well as an inhibitor, inducer, or normal responder.
- **Plate heatmap visualization** — Renders individual plates as well-shaped heatmaps that mirror the physical plate layout, making spatial artifacts and edge effects immediately visible.
- **Flexible aggregation** — Normalization and threshold calculations support both mean- and median-based strategies, allowing the workflow to be adapted to assay-specific noise characteristics.
- **Compound library support** — Ships with predefined control well maps and validated hit lists for standard screening libraries (LOPAC and Prestwick), enabling direct comparison against known bioactive compounds.
- **Notebook-first design** — The package is structured for use in Jupyter notebooks, with concise APIs and informative print summaries at each analysis step to support interactive, exploratory workflows.

## Installation

To install the required dependencies, ensure you have Python 3.10 or later installed. Then, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd high-throughput-compound-screening
   ```
3. Open the Jupyter notebooks in the `notebooks/` directory to explore the data analysis workflows.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

This project is funded by Marie Curie Actions under the European Union’s Horizon 2020 research and innovation program for project proEVLifeCycle, grant No 860303.

Special thanks to the open-source community for providing the foundational libraries (e.g., Pandas, Matplotlib, Seaborn) that make this project possible.