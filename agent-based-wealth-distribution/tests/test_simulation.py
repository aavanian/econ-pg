"""
Unit tests for Simulation class.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.simulation import Simulation


def test_simulation_creation():
    """Test basic simulation creation."""
    sim = Simulation(
        num_agents=10,
        initial_wealth_min=0.0,
        initial_wealth_max=100.0,
        aggregate_growth_per_step=5.0,
        wealth_change_std=2.0,
        random_seed=42,
    )
    assert sim.num_agents == 10
    assert len(sim.agents) == 10


def test_simulation_invalid_num_agents():
    """Test that invalid number of agents raises error."""
    with pytest.raises(ValueError):
        Simulation(num_agents=0)


def test_simulation_invalid_wealth_range():
    """Test that invalid wealth range raises error."""
    with pytest.raises(ValueError):
        Simulation(initial_wealth_min=100.0, initial_wealth_max=50.0)


def test_simulation_invalid_std():
    """Test that negative std raises error."""
    with pytest.raises(ValueError):
        Simulation(wealth_change_std=-1.0)


def test_initial_wealth_distribution():
    """Test that initial wealth is within specified range."""
    sim = Simulation(
        num_agents=100,
        initial_wealth_min=10.0,
        initial_wealth_max=20.0,
        random_seed=42,
    )
    wealths = sim.get_wealth_array()
    assert np.all(wealths >= 10.0)
    assert np.all(wealths <= 20.0)


def test_aggregate_growth_constraint():
    """Test that aggregate growth constraint is satisfied (percentage-based)."""
    sim = Simulation(
        num_agents=100,
        initial_wealth_min=100.0,
        initial_wealth_max=100.0,
        aggregate_growth_per_step=2.0,  # 2% growth
        random_seed=42,
    )

    initial_total = np.sum(sim.get_wealth_array())
    expected_growth = initial_total * 0.02  # 2% of initial total

    sim.step()
    final_total = np.sum(sim.get_wealth_array())

    # Check that total wealth increased by exactly the target percentage
    actual_growth = final_total - initial_total
    assert np.isclose(actual_growth, expected_growth, rtol=1e-10)


def test_simulation_run():
    """Test running simulation for multiple steps."""
    sim = Simulation(num_agents=10, random_seed=42)
    history = sim.run(num_steps=10, record_interval=1)

    # Should have 11 records (0 through 10)
    assert len(history["step"].unique()) == 11

    # Should have records for all agents
    assert len(history["agent_id"].unique()) == 10


def test_simulation_record_interval():
    """Test that record_interval works correctly."""
    sim = Simulation(num_agents=10, random_seed=42)
    history = sim.run(num_steps=10, record_interval=2)

    # Should have records at steps 0, 2, 4, 6, 8, 10
    expected_steps = [0, 2, 4, 6, 8, 10]
    actual_steps = sorted(history["step"].unique())
    assert actual_steps == expected_steps


def test_get_statistics():
    """Test statistics calculation."""
    sim = Simulation(num_agents=10, random_seed=42)
    stats = sim.get_statistics()

    # Check that all expected keys are present
    expected_keys = ["mean", "median", "std", "min", "max", "gini", "total_wealth"]
    for key in expected_keys:
        assert key in stats

    # Check that Gini is between 0 and 1
    assert 0 <= stats["gini"] <= 1


def test_reproducibility():
    """Test that simulations with same seed are reproducible."""
    sim1 = Simulation(num_agents=50, random_seed=123)
    sim1.run(num_steps=10)
    final_wealth_1 = sim1.get_wealth_array()

    sim2 = Simulation(num_agents=50, random_seed=123)
    sim2.run(num_steps=10)
    final_wealth_2 = sim2.get_wealth_array()

    # Should be identical
    assert np.allclose(final_wealth_1, final_wealth_2)


def test_wealth_non_negativity():
    """Test that wealth stays non-negative even with high volatility."""
    sim = Simulation(
        num_agents=100,
        initial_wealth_min=0.0,
        initial_wealth_max=10.0,
        wealth_change_std=20.0,  # High volatility
        aggregate_growth_per_step=5.0,
        random_seed=42,
    )

    sim.run(num_steps=50)
    wealths = sim.get_wealth_array()

    # All wealths should be non-negative
    assert np.all(wealths >= 0)


def test_compound_growth():
    """Test that compound growth works correctly over multiple periods."""
    sim = Simulation(
        num_agents=100,
        initial_wealth_min=100.0,
        initial_wealth_max=100.0,
        aggregate_growth_per_step=2.0,  # 2% growth
        wealth_change_std=5.0,
        random_seed=42,
    )

    initial_total = np.sum(sim.get_wealth_array())
    assert np.isclose(initial_total, 10000.0)  # 100 agents × 100 wealth

    # Run for 100 steps
    sim.run(num_steps=100)

    final_total = sim.get_statistics()["total_wealth"]
    expected_total = initial_total * (1.02 ** 100)

    # Should match compound growth formula within small tolerance
    assert np.isclose(final_total, expected_total, rtol=1e-8)
