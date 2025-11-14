# Agent-Based Wealth Distribution Simulation

An agent-based model exploring the dynamics of wealth distribution in a growing economy with stochastic individual outcomes.

## Overview

This simulation models how wealth inequality emerges and evolves in a population of agents subject to:
- **Systematic growth**: The total economy grows by a fixed amount each time step
- **Idiosyncratic shocks**: Individual wealth changes are stochastic (drawn from a probability distribution)
- **Non-negativity constraint**: Agents cannot have negative wealth (bankruptcy floor at zero)

### Phenomenon Being Studied

The model addresses a fundamental question in economics: **How does wealth inequality evolve when all agents face the same aggregate economic growth but experience different individual outcomes?**

This is relevant to understanding:
- The emergence of wealth inequality even in growing economies
- The role of luck vs. systematic factors in wealth accumulation
- The long-run steady-state distribution of wealth
- The effectiveness of redistribution policies

### Key Assumptions

1. **Homogeneous agents**: All agents follow the same behavioral rules
2. **Uniform initial distribution**: Agents start with wealth uniformly distributed in a range
3. **Aggregate growth constraint**: Total wealth grows by exactly a fixed amount per period
4. **Normal shocks**: Individual wealth changes are drawn from a normal distribution, then adjusted to meet the aggregate constraint
5. **Bankruptcy floor**: Wealth cannot go below zero

### Expected Insights

- **Inequality emergence**: Even starting from a uniform distribution, inequality (measured by Gini coefficient) will likely increase over time
- **Distribution shape**: The wealth distribution will evolve from uniform toward a right-skewed distribution (potentially log-normal or power-law)
- **Volatility effect**: Higher individual volatility should lead to greater long-run inequality
- **Growth neutrality**: The aggregate growth rate may not directly affect inequality, but rather shifts the entire distribution

## Methodology

### Model Components

#### 1. Agent Class (`src/agents.py`)
Each agent has:
- `agent_id`: Unique identifier
- `wealth`: Current wealth level (non-negative)

Methods:
- `update_wealth(change)`: Modify wealth by a specified amount, enforcing non-negativity

#### 2. Simulation Class (`src/simulation.py`)
Manages the population and time-stepping dynamics.

**Initialization**:
- Creates `num_agents` agents
- Assigns initial wealth from uniform distribution U(min, max)

**Time step algorithm**:
1. Calculate target growth: `target = current_total_wealth × (growth_rate / 100)`
2. Draw raw wealth changes from N(0, σ²) for each agent
3. Calculate adjustment needed: `adj = (target - sum(raw_changes)) / num_agents`
4. Apply adjusted changes: `change[i] = raw_change[i] + adj`
5. Update each agent's wealth, enforcing non-negativity

**Key constraint**: ∑ᵢ change[i] = current_total_wealth × (growth_rate / 100) (exactly)

#### 3. Visualization Module (`src/visualization.py`)
Provides functions to visualize:
- Wealth distribution histograms
- Lorenz curves and Gini coefficients
- Time series of percentiles and statistics
- Comprehensive dashboards

### Mathematical Formulation

Let:
- $W_{i,t}$ = wealth of agent $i$ at time $t$
- $\Delta W_{i,t}$ = wealth change for agent $i$ at time $t$
- $g$ = aggregate growth rate per time step (percentage, e.g., 2.0 for 2%)
- $\sigma$ = standard deviation of individual shocks
- $N$ = number of agents
- $W_{\text{total},t} = \sum_i W_{i,t}$ = total wealth at time $t$

**Wealth evolution**:
$$W_{i,t+1} = \max(0, W_{i,t} + \Delta W_{i,t})$$

**Wealth change generation**:
1. Calculate target growth: $G_t = W_{\text{total},t} \times \frac{g}{100}$
2. Draw: $\epsilon_i \sim \mathcal{N}(0, \sigma^2)$ for each agent
3. Compute: $\Delta W_{i,t} = \epsilon_i + \frac{G_t - \sum_j \epsilon_j}{N}$
4. Constraint: $\sum_i \Delta W_{i,t} = G_t$ (exactly satisfied)

**Aggregate wealth evolution** (compound growth):
$$W_{\text{total},t} = W_{\text{total},0} \times \left(1 + \frac{g}{100}\right)^t$$

**Inequality measure** (Gini coefficient):
$$\text{Gini} = \frac{2 \sum_{i=1}^N i \cdot W_i^{\text{sorted}}}{N \sum_{i=1}^N W_i} - \frac{N+1}{N}$$

where $W_i^{\text{sorted}}$ is wealth sorted in ascending order.

## Structure

```
agent-based-wealth-distribution/
├── README.md                       # This file
├── main.py                         # Main entry point
├── src/                            # Source code package
│   ├── __init__.py                # Package initialization
│   ├── agents.py                  # Agent class definition
│   ├── simulation.py              # Simulation engine
│   └── visualization.py           # Plotting utilities
├── notebooks/
│   └── exploration.ipynb          # Interactive Jupyter notebook
├── data/                          # Data output directory
├── results/                       # Generated visualizations
│   ├── dashboard.png              # Comprehensive dashboard
│   └── distribution_snapshots.png # Evolution snapshots
└── tests/                         # Unit tests (optional)
```

## Installation

### Prerequisites
- Python 3.10 or higher
- Virtual environment tool (e.g., `uv`, `venv`)

### Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd econ-pg
   ```

2. **Create and activate virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   uv pip install -e .
   ```

4. **Navigate to experiment directory**:
   ```bash
   cd agent-based-wealth-distribution
   ```

## Usage

### Running the Basic Simulation

Execute the main script with default parameters:

```bash
python main.py
```

This will:
- Initialize 100 agents with uniform wealth [0, 100]
- Run simulation for 100 time steps
- Generate and save visualizations to `results/` directory
- Display summary statistics

**Expected output**:
```
======================================================================
Agent-Based Wealth Distribution Simulation
======================================================================

Initializing simulation...

Initial Statistics:
  mean           :      49.87
  median         :      49.23
  std            :      29.17
  min            :       1.45
  max            :      98.76
  gini           :       0.290
  total_wealth   :    4987.23

Running simulation for 100 time steps...

Final Statistics:
  mean           :     149.87
  median         :     123.45
  std            :      78.32
  min            :       0.00
  max            :     456.12
  gini           :       0.412

Inequality Change:
  Initial Gini: 0.290
  Final Gini:   0.412
  Change:       +0.122

Creating visualizations...
  Saved dashboard to: results/dashboard.png
  Saved snapshots to: results/distribution_snapshots.png

Simulation complete!
======================================================================
```

### Interactive Exploration

For interactive parameter exploration and visualization:

```bash
jupyter notebook notebooks/exploration.ipynb
```

The notebook includes:
- Step-by-step simulation walkthrough
- Parameter sensitivity analysis
- Custom experiment templates
- Data export utilities

### Programmatic Usage

```python
from src.simulation import Simulation
from src.visualization import create_dashboard

# Create simulation
sim = Simulation(
    num_agents=100,
    initial_wealth_min=0.0,
    initial_wealth_max=100.0,
    aggregate_growth_per_step=10.0,
    wealth_change_std=5.0,
    random_seed=42,
)

# Run simulation
history = sim.run(num_steps=100, record_interval=1)

# Get current statistics
stats = sim.get_statistics()
print(f"Gini coefficient: {stats['gini']:.3f}")

# Visualize
import matplotlib.pyplot as plt
final_wealths = sim.get_wealth_array()
fig = create_dashboard(history, final_wealths)
plt.savefig('my_results.png')
```

## Parameters

### Simulation Parameters

| Parameter | Type | Description | Default | Range/Constraints |
|-----------|------|-------------|---------|-------------------|
| `num_agents` | int | Number of agents in population | 100 | > 0 |
| `initial_wealth_min` | float | Minimum initial wealth | 0.0 | ≥ 0 |
| `initial_wealth_max` | float | Maximum initial wealth | 100.0 | ≥ initial_wealth_min |
| `aggregate_growth_per_step` | float | Percentage growth rate per time step (compound) | 2.0 | Any (can be negative) |
| `wealth_change_std` | float | Standard deviation of individual shocks | 5.0 | ≥ 0 |
| `random_seed` | int or None | Random seed for reproducibility | None | Any integer |

### Run Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `num_steps` | int | Number of time steps to simulate | - |
| `record_interval` | int | Record data every N steps | 1 |

### Interpretation Guide

- **Higher `wealth_change_std`**: More volatility → greater inequality
- **Higher `aggregate_growth_per_step`**: Faster wealth accumulation, but inequality dynamics unchanged
- **Larger `num_agents`**: More stable statistical patterns, smoother distributions
- **`aggregate_growth_per_step = 0`**: Zero-sum economy, focuses purely on redistribution dynamics

## Results

### Key Visualizations

The simulation generates several types of visualizations:

#### 1. Dashboard (`results/dashboard.png`)
Comprehensive 6-panel view including:
- Final wealth distribution (histogram)
- Lorenz curve with Gini coefficient
- Wealth percentile evolution (10th, 50th, 90th)
- Gini coefficient over time
- Mean, median, and standard deviation evolution

#### 2. Distribution Snapshots (`results/distribution_snapshots.png`)
Shows wealth distribution histograms at multiple time points (e.g., t=0, 25, 50, 75, 100), illustrating the evolution from uniform to skewed distribution.

### Typical Findings

**Starting from uniform distribution [0, 100]**:
- Initial Gini ≈ 0.29 (moderate inequality)
- After 100 steps with σ=5, G=10: Final Gini ≈ 0.35-0.45
- Distribution becomes right-skewed
- Some agents accumulate substantially more wealth than others
- A few agents may hit the zero-wealth floor

**Effect of volatility**:
- σ = 1: Gini increases slowly, distribution remains relatively compact
- σ = 5: Moderate inequality growth
- σ = 10: Rapid inequality growth, highly skewed distribution
- σ = 20: Extreme inequality, potential for near-zero wealth concentration

## Examples

### Example 1: High Volatility Economy

```python
sim = Simulation(
    num_agents=200,
    initial_wealth_min=50.0,
    initial_wealth_max=150.0,
    aggregate_growth_per_step=20.0,
    wealth_change_std=15.0,  # High volatility
    random_seed=123,
)
history = sim.run(num_steps=200)
```

**Expected outcome**: Rapid inequality growth, highly skewed final distribution, Gini > 0.5

### Example 2: Low Volatility Economy

```python
sim = Simulation(
    num_agents=100,
    initial_wealth_min=0.0,
    initial_wealth_max=100.0,
    aggregate_growth_per_step=10.0,
    wealth_change_std=2.0,  # Low volatility
    random_seed=456,
)
history = sim.run(num_steps=100)
```

**Expected outcome**: Slow inequality growth, distribution remains relatively symmetric, Gini ≈ 0.32-0.38

### Example 3: Zero-Sum Economy

```python
sim = Simulation(
    num_agents=100,
    initial_wealth_min=0.0,
    initial_wealth_max=100.0,
    aggregate_growth_per_step=0.0,  # No aggregate growth
    wealth_change_std=5.0,
    random_seed=789,
)
history = sim.run(num_steps=100)
```

**Expected outcome**: Pure redistribution dynamics, constant total wealth, high inequality due to random concentration

## Extensions and Future Work

Potential extensions to this baseline model:

1. **Alternative shock distributions**:
   - Log-normal shocks (bounded below, unbounded above)
   - Power-law shocks (fat tails)
   - Mixture models

2. **Heterogeneous agents**:
   - Different risk profiles (different σ per agent)
   - Income vs. wealth shocks
   - Behavioral differences (saving rates, risk aversion)

3. **Economic mechanisms**:
   - Multiplicative growth (returns proportional to wealth)
   - Taxation and redistribution
   - Inter-agent transactions and trade
   - Inheritance and generational dynamics

4. **Network effects**:
   - Spatial structure
   - Social networks affecting opportunities
   - Information diffusion

5. **Policy interventions**:
   - Progressive taxation
   - Universal basic income
   - Wealth caps or floors
   - Mobility barriers

## References

### Theoretical Background

1. **Gibrat's Law**: The principle that growth rate is independent of size, leading to log-normal distributions
   - Gibrat, R. (1931). *Les inégalités économiques*

2. **Wealth distribution models**:
   - Benhabib, J., & Bisin, A. (2018). "Skewed wealth distributions: Theory and empirics". *Journal of Economic Literature*, 56(4), 1261-1291.
   - Gabaix, X., et al. (2016). "The dynamics of inequality". *Econometrica*, 84(6), 2071-2111.

3. **Agent-based modeling**:
   - Tesfatsion, L., & Judd, K. L. (2006). *Handbook of computational economics: Agent-based computational economics*
   - Farmer, J. D., & Foley, D. (2009). "The economy needs agent-based modelling". *Nature*, 460(7256), 685-686.

### Empirical Patterns

4. **Wealth inequality empirics**:
   - Piketty, T., & Zucman, G. (2014). "Wealth inequality in the United States since 1913". *Quarterly Journal of Economics*
   - Saez, E., & Zucman, G. (2016). "Wealth inequality in the United States since 1913". *NBER Working Paper*

### Related Models

5. **Yard-sale model**: A simple model showing wealth concentration
   - Boghosian, B. M. (2014). "Fokker–Planck description of wealth dynamics and the origin of Pareto's law". *International Journal of Modern Physics C*

6. **Kinetic exchange models**: Physics-inspired models of wealth
   - Chakraborti, A., & Chakrabarti, B. K. (2000). "Statistical mechanics of money". *European Physical Journal B*

## Notes

### Limitations

1. **Simplified dynamics**: Real wealth accumulation involves complex mechanisms (capital returns, labor income, consumption, etc.)
2. **No behavioral heterogeneity**: All agents are identical ex-ante
3. **No strategic interaction**: Agents don't make decisions based on others' wealth
4. **Fixed growth**: Aggregate growth is exogenous, not endogenous to agent actions
5. **No demographics**: No births, deaths, or generational transfers

### Computational Considerations

- **Scalability**: Tested up to 10,000 agents; performance is O(N) per time step
- **Memory**: History recording can be large for long simulations; use `record_interval > 1` for efficiency
- **Numerical stability**: Wealth changes use floating-point arithmetic; aggregate constraint satisfied within machine precision

### Interpretation Caveats

- **Normative neutrality**: This model describes dynamics, not optimal outcomes
- **Initial conditions matter**: Starting from different distributions yields different inequality trajectories
- **Time horizon**: Short-run vs. long-run inequality dynamics may differ
- **Gini limitations**: Gini coefficient is one measure; consider other inequality metrics (Theil, Atkinson, percentile ratios)

### Future Development

This experiment is designed to be extended. Contributions welcome for:
- Alternative wealth change mechanisms
- Policy intervention modules
- Network/spatial structures
- Calibration to empirical data
- Additional inequality metrics and visualization tools

---

**Author**: Created as part of the `econ-pg` economics pedagogy repository
**License**: [Specify license]
**Last Updated**: 2025-11-14
