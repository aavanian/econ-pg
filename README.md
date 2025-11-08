# Economics Analysis Playground

A collection of economic analyses, simulations, and experiments implemented in Python. This repository serves as a workspace for exploring various economic models, theories, and computational economics.

## Overview

This repository contains independent economics projects, each in its own directory with dedicated documentation. Projects range from theoretical models to empirical analyses and interactive simulations.

## Structure

Each analysis/simulation/experiment is contained in its own folder with:
- `README.md` - Detailed description, methodology, and usage instructions
- Python scripts and/or Jupyter notebooks
- Optional web interfaces (JavaScript/Pyiodide)
- Dependencies managed via `pyproject.toml`

```
econ-pg/
├── README.md (this file)
├── pyproject.toml (root dependencies)
├── .gitignore
├── analysis-name-1/
│   ├── README.md
│   ├── main.py
│   ├── notebooks/
│   └── pyproject.toml (optional, for specific dependencies)
├── analysis-name-2/
│   ├── README.md
│   ├── simulation.py
│   └── ...
└── ...
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

### Installing uv

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd econ-pg
```

2. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

3. Navigate to a specific analysis folder and follow its README for specific instructions.

## Running Analyses

Each analysis folder contains its own instructions. Generally:

```bash
# For Python scripts
cd <analysis-folder>
python main.py

# For Jupyter notebooks
jupyter notebook  # or jupyter lab
```

## Technologies

- **Python**: Primary language for models and simulations
- **uv**: Fast package management and dependency resolution
- **Jupyter**: Interactive notebooks for exploratory analysis
- **NumPy/SciPy**: Numerical computing
- **Pandas**: Data manipulation and analysis
- **Matplotlib/Plotly**: Visualization
- **Pyiodide** (optional): Running Python in the browser
- **JavaScript** (optional): Interactive web interfaces

## Project Ideas

This repository may include:
- Microeconomic models (supply/demand, market equilibrium, game theory)
- Macroeconomic simulations (IS-LM, DSGE models, growth models)
- Agent-based models (market dynamics, behavioral economics)
- Econometric analyses (regression, time series, causal inference)
- Computational economics (optimization, numerical methods)
- Interactive visualizations and educational tools

## Contributing

Feel free to add new analyses by creating a new folder with:
1. A descriptive name (use hyphens, e.g., `solow-growth-model`)
2. A comprehensive README.md
3. Well-documented code
4. A `pyproject.toml` if you have specific dependencies

## License

See [LICENSE](LICENSE) for details.

## Resources

- [QuantEcon](https://quantecon.org/) - Open source code for economic modeling
- [EconML](https://econml.azurewebsites.net/) - Machine learning for causal inference
- [Statsmodels](https://www.statsmodels.org/) - Statistical modeling in Python
