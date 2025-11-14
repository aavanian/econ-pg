# Contributing Guidelines

Thank you for contributing to the Economics Analysis Playground! This document provides guidelines for adding new analyses and experiments.

## Adding a New Analysis

1. **Create a descriptive folder name** using lowercase and hyphens:
   ```bash
   mkdir analysis-name
   cd analysis-name
   ```

2. **Copy the template README**:
   ```bash
   cp ../TEMPLATE_README.md README.md
   ```

3. **Fill in the README** with:
   - Clear description of the economic concept or question
   - Methodology and assumptions
   - Usage instructions
   - Expected results and outputs

4. **Organize your code**:
   ```
   your-analysis/
   ├── README.md
   ├── main.py or analysis.py (entry point)
   ├── notebooks/ (if using Jupyter)
   ├── data/ (if needed, add to .gitignore if large)
   ├── tests/ (recommended)
   └── pyproject.toml (optional, for specific dependencies)
   ```

5. **Document dependencies** either in:
   - The root `pyproject.toml` (if commonly useful)
   - A local `pyproject.toml` (if analysis-specific)
   - The analysis README

## Code Quality

- **Formatting**: Use `black` or `ruff format` for consistent style
- **Linting**: Run `ruff check` to catch common issues
- **Documentation**: Add docstrings to functions and classes
- **Type hints**: Use type annotations where helpful
- **Comments**: Explain economic intuition, not just code mechanics

Example:
```python
def calculate_equilibrium_price(
    demand_slope: float,
    supply_slope: float,
    demand_intercept: float,
    supply_intercept: float
) -> float:
    """
    Calculate market equilibrium price where supply equals demand.

    Assumes linear demand (P = a - bQ) and supply (P = c + dQ) curves.

    Args:
        demand_slope: Slope of demand curve (negative)
        supply_slope: Slope of supply curve (positive)
        demand_intercept: Price intercept of demand curve
        supply_intercept: Price intercept of supply curve

    Returns:
        Equilibrium price
    """
    # Solve for Q where demand = supply, then find P
    eq_quantity = (demand_intercept - supply_intercept) / (supply_slope - demand_slope)
    return supply_intercept + supply_slope * eq_quantity
```

## Jupyter Notebooks

- Place notebooks in a `notebooks/` subdirectory
- Clear all outputs before committing (unless results are important)
- Include markdown cells explaining the economic reasoning
- Keep notebooks focused and not too long

## Data

- **Small data** (<10MB): Can commit to repo in `data/` folder
- **Medium data** (10-100MB): Consider using Git LFS
- **Large data** (>100MB): Provide download instructions in README
- **Sensitive data**: Never commit, document how to obtain

## Testing

While not required, tests are encouraged:
```bash
mkdir tests
# Add test_*.py files
pytest
```

## Examples of Good Analysis Structure

### Simple Script Analysis
```
simple-monopoly/
├── README.md
├── monopoly.py
└── plot_outputs.py
```

### Notebook-Based Analysis
```
keynesian-cross/
├── README.md
├── notebooks/
│   ├── model.ipynb
│   └── sensitivity_analysis.ipynb
└── utils.py
```

### Complex Simulation
```
agent-based-market/
├── README.md
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── agents.py
│   ├── market.py
│   └── visualization.py
├── notebooks/
│   └── demo.ipynb
├── tests/
│   └── test_agents.py
├── web/
│   ├── index.html
│   └── app.js
└── main.py
```

## Commit Messages

Use clear, descriptive commit messages:
- `Add: Solow growth model implementation`
- `Update: Fix capital accumulation equation`
- `Docs: Add usage examples to README`

## Questions?

If you're unsure about anything, just start! You can always refine later. The goal is to explore and learn economics through code.
