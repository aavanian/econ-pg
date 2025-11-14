# Supply and Demand Equilibrium

A simple demonstration of market equilibrium using linear supply and demand curves.

## Overview

This example illustrates the fundamental microeconomic concept of market equilibrium. It models a market with linear supply and demand curves and calculates the equilibrium price and quantity where the two curves intersect. The analysis includes visualization and sensitivity analysis to parameter changes.

## Methodology

### Model

**Demand Curve (downward sloping):**
```
P = a - b*Q
```
- P: Price
- Q: Quantity demanded
- a: Price intercept (maximum willingness to pay)
- b: Slope (how responsive demand is to price)

**Supply Curve (upward sloping):**
```
P = c + d*Q
```
- P: Price
- Q: Quantity supplied
- c: Price intercept (minimum supply price)
- d: Slope (how responsive supply is to price)

**Equilibrium:**
At equilibrium, quantity demanded equals quantity supplied:
```
a - b*Q = c + d*Q
Q* = (a - c) / (b + d)
P* = a - b*Q*
```

## Structure

```
example-supply-demand/
├── README.md
├── market.py (core model)
├── plot.py (visualization)
└── notebooks/
    └── exploration.ipynb (interactive analysis)
```

## Installation

No additional dependencies required beyond the root project. From the root directory:

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

### Basic Usage

```bash
cd example-supply-demand
python market.py
```

This will calculate and display the equilibrium for default parameters.

### Creating Visualizations

```bash
python plot.py
```

Generates a plot showing supply and demand curves with equilibrium point.

### Interactive Exploration

```bash
jupyter notebook notebooks/exploration.ipynb
```

## Parameters

| Parameter | Description | Default | Notes |
|-----------|-------------|---------|-------|
| `demand_intercept` | Maximum price consumers will pay | 100 | Must be > 0 |
| `demand_slope` | Price responsiveness of demand | 2 | Must be > 0 |
| `supply_intercept` | Minimum price suppliers accept | 20 | Must be >= 0 |
| `supply_slope` | Price responsiveness of supply | 1.5 | Must be > 0 |

## Results

The analysis produces:
- Equilibrium price and quantity (numerical output)
- Supply and demand curve plot with equilibrium point marked
- Sensitivity analysis showing how equilibrium changes with parameters

## Examples

```python
from market import Market

# Create market with default parameters
market = Market()
price, quantity = market.equilibrium()
print(f"Equilibrium: P* = {price:.2f}, Q* = {quantity:.2f}")

# Create market with custom parameters
custom_market = Market(
    demand_intercept=150,
    demand_slope=3,
    supply_intercept=30,
    supply_slope=2
)
price, quantity = custom_market.equilibrium()
```

## References

- Mankiw, N. Gregory. *Principles of Economics*. Cengage Learning.
- Varian, Hal R. *Intermediate Microeconomics: A Modern Approach*. W. W. Norton & Company.

## Notes

This is a simplified example assuming:
- Perfect competition
- Linear supply and demand
- No externalities or market failures
- Instantaneous adjustment to equilibrium

Future extensions could include:
- Non-linear curves
- Tax/subsidy effects
- Price floors and ceilings
- Consumer and producer surplus calculations
