"""
Main entry point for agent-based wealth distribution simulation.

This script runs a simulation with default parameters and generates
visualizations of the wealth distribution evolution.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.simulation import Simulation
from src.visualization import (
    create_dashboard,
    plot_distribution_snapshots,
)
import matplotlib.pyplot as plt


def main():
    """
    Run simulation with default parameters and create visualizations.

    Economic Setup:
        - Population: 100 agents
        - Initial wealth: Uniformly distributed between 0 and 100
        - Aggregate growth: 10 units per time step
        - Individual volatility: Standard deviation of 5
        - Time horizon: 100 steps
    """
    print("=" * 70)
    print("Agent-Based Wealth Distribution Simulation")
    print("=" * 70)

    # Create simulation with default parameters
    print("\nInitializing simulation...")
    sim = Simulation(
        num_agents=100,
        initial_wealth_min=0.0,
        initial_wealth_max=100.0,
        aggregate_growth_per_step=10.0,
        wealth_change_std=5.0,
        random_seed=42,
    )

    # Display initial statistics
    print("\nInitial Statistics:")
    initial_stats = sim.get_statistics()
    for key, value in initial_stats.items():
        print(f"  {key:15s}: {value:10.2f}")

    # Run simulation
    print("\nRunning simulation for 100 time steps...")
    num_steps = 100
    history = sim.run(num_steps=num_steps, record_interval=1)

    # Display final statistics
    print("\nFinal Statistics:")
    final_stats = sim.get_statistics()
    for key, value in final_stats.items():
        print(f"  {key:15s}: {value:10.2f}")

    # Calculate change in inequality
    initial_gini = initial_stats["gini"]
    final_gini = final_stats["gini"]
    print(f"\nInequality Change:")
    print(f"  Initial Gini: {initial_gini:.3f}")
    print(f"  Final Gini:   {final_gini:.3f}")
    print(f"  Change:       {final_gini - initial_gini:+.3f}")

    # Create visualizations
    print("\nCreating visualizations...")

    # Dashboard with all metrics
    final_wealths = sim.get_wealth_array()
    fig_dashboard = create_dashboard(history, final_wealths)
    dashboard_path = Path(__file__).parent / "results" / "dashboard.png"
    dashboard_path.parent.mkdir(exist_ok=True)
    fig_dashboard.savefig(dashboard_path, dpi=150, bbox_inches="tight")
    print(f"  Saved dashboard to: {dashboard_path}")

    # Distribution snapshots at key time points
    time_steps = [0, 25, 50, 75, 100]
    fig_snapshots = plot_distribution_snapshots(history, time_steps)
    snapshots_path = Path(__file__).parent / "results" / "distribution_snapshots.png"
    fig_snapshots.savefig(snapshots_path, dpi=150, bbox_inches="tight")
    print(f"  Saved snapshots to: {snapshots_path}")

    print("\nSimulation complete!")
    print("=" * 70)

    # Optionally display plots
    # plt.show()


if __name__ == "__main__":
    main()
