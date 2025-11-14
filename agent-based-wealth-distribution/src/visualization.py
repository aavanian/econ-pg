"""
Visualization utilities for wealth distribution analysis.

This module provides functions to visualize the evolution of wealth
distribution over time, including histograms, time series, Lorenz curves,
and multi-panel dashboards.
"""

from typing import Optional, List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation


def plot_wealth_distribution(
    wealths: np.ndarray,
    title: str = "Wealth Distribution",
    bins: int = 30,
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """
    Plot histogram of wealth distribution.

    Args:
        wealths: Array of wealth values
        title: Plot title
        bins: Number of histogram bins
        ax: Matplotlib axes (creates new if None)

    Returns:
        Matplotlib axes object

    Economic Intuition:
        The wealth distribution often becomes right-skewed over time,
        with a long tail of high-wealth agents and many low-wealth agents.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(wealths, bins=bins, edgecolor="black", alpha=0.7)
    ax.set_xlabel("Wealth")
    ax.set_ylabel("Number of Agents")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)

    # Add statistics text
    mean_wealth = np.mean(wealths)
    median_wealth = np.median(wealths)
    ax.axvline(mean_wealth, color="red", linestyle="--", linewidth=2, label=f"Mean: {mean_wealth:.2f}")
    ax.axvline(
        median_wealth, color="green", linestyle="--", linewidth=2, label=f"Median: {median_wealth:.2f}"
    )
    ax.legend()

    return ax


def plot_lorenz_curve(
    wealths: np.ndarray,
    title: str = "Lorenz Curve",
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """
    Plot Lorenz curve showing cumulative wealth distribution.

    Args:
        wealths: Array of wealth values
        title: Plot title
        ax: Matplotlib axes (creates new if None)

    Returns:
        Matplotlib axes object

    Economic Intuition:
        The Lorenz curve plots cumulative share of population (x-axis) vs
        cumulative share of wealth (y-axis). The diagonal represents perfect
        equality. The area between the curve and diagonal is the Gini coefficient.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))

    # Sort wealths and calculate cumulative shares
    wealths_sorted = np.sort(wealths)
    cum_wealth = np.cumsum(wealths_sorted)
    cum_wealth_share = cum_wealth / cum_wealth[-1]
    cum_pop_share = np.arange(1, len(wealths) + 1) / len(wealths)

    # Plot Lorenz curve
    ax.plot([0] + list(cum_pop_share), [0] + list(cum_wealth_share), linewidth=2, label="Lorenz Curve")

    # Plot perfect equality line
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Perfect Equality")

    # Calculate and display Gini coefficient
    n = len(wealths)
    gini = (2 * np.sum((np.arange(n) + 1) * wealths_sorted)) / (n * cum_wealth[-1]) - (n + 1) / n
    ax.text(0.6, 0.2, f"Gini = {gini:.3f}", fontsize=14, bbox=dict(boxstyle="round", facecolor="wheat"))

    ax.set_xlabel("Cumulative Share of Population")
    ax.set_ylabel("Cumulative Share of Wealth")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    return ax


def plot_wealth_evolution(
    history: pd.DataFrame,
    percentiles: List[int] = [10, 50, 90],
    title: str = "Wealth Evolution Over Time",
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """
    Plot time series of wealth percentiles.

    Args:
        history: DataFrame with columns [step, agent_id, wealth]
        percentiles: List of percentiles to plot (e.g., [10, 50, 90])
        title: Plot title
        ax: Matplotlib axes (creates new if None)

    Returns:
        Matplotlib axes object

    Economic Intuition:
        Tracking percentiles over time reveals whether inequality is increasing
        (spreading apart) or decreasing (converging). The median (50th percentile)
        shows the typical agent's trajectory.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))

    # Calculate percentiles for each time step
    percentile_data = history.groupby("step")["wealth"].quantile([p / 100 for p in percentiles]).unstack()
    percentile_data.columns = [f"{int(p*100)}th" for p in percentile_data.columns]

    # Plot each percentile
    for col in percentile_data.columns:
        ax.plot(percentile_data.index, percentile_data[col], linewidth=2, label=col)

    ax.set_xlabel("Time Step")
    ax.set_ylabel("Wealth")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()

    return ax


def plot_gini_evolution(
    history: pd.DataFrame,
    title: str = "Gini Coefficient Over Time",
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """
    Plot Gini coefficient evolution over time.

    Args:
        history: DataFrame with columns [step, agent_id, wealth]
        title: Plot title
        ax: Matplotlib axes (creates new if None)

    Returns:
        Matplotlib axes object

    Economic Intuition:
        The Gini coefficient measures inequality (0 = perfect equality,
        1 = one agent has all wealth). Tracking it over time shows whether
        the economy is becoming more or less unequal.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))

    # Calculate Gini for each time step
    def calculate_gini(wealths):
        wealths_sorted = np.sort(wealths)
        n = len(wealths)
        cumsum = np.cumsum(wealths_sorted)
        if cumsum[-1] == 0:
            return 0
        return (2 * np.sum((np.arange(n) + 1) * wealths_sorted)) / (n * cumsum[-1]) - (n + 1) / n

    gini_by_step = history.groupby("step")["wealth"].apply(calculate_gini)

    ax.plot(gini_by_step.index, gini_by_step.values, linewidth=2, color="darkred")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Gini Coefficient")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1)

    return ax


def plot_wealth_statistics(
    history: pd.DataFrame,
    title: str = "Wealth Statistics Over Time",
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """
    Plot mean, median, and other statistics over time.

    Args:
        history: DataFrame with columns [step, agent_id, wealth]
        title: Plot title
        ax: Matplotlib axes (creates new if None)

    Returns:
        Matplotlib axes object
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))

    # Calculate statistics for each time step
    stats_by_step = history.groupby("step")["wealth"].agg(["mean", "median", "std"])

    ax.plot(stats_by_step.index, stats_by_step["mean"], linewidth=2, label="Mean", color="blue")
    ax.plot(stats_by_step.index, stats_by_step["median"], linewidth=2, label="Median", color="green")

    # Add standard deviation as shaded area around mean
    ax.fill_between(
        stats_by_step.index,
        stats_by_step["mean"] - stats_by_step["std"],
        stats_by_step["mean"] + stats_by_step["std"],
        alpha=0.3,
        color="blue",
        label="±1 Std Dev",
    )

    ax.set_xlabel("Time Step")
    ax.set_ylabel("Wealth")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()

    return ax


def create_dashboard(
    history: pd.DataFrame,
    final_wealths: np.ndarray,
    figsize: tuple = (16, 12),
) -> Figure:
    """
    Create a comprehensive dashboard with multiple visualizations.

    Args:
        history: DataFrame with columns [step, agent_id, wealth]
        final_wealths: Array of final wealth values
        figsize: Figure size tuple (width, height)

    Returns:
        Matplotlib Figure object

    Economic Intuition:
        A dashboard provides a holistic view of wealth dynamics:
        - Distribution shape (histogram)
        - Inequality measurement (Lorenz curve, Gini)
        - Time evolution (percentiles, statistics)
    """
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

    # Top row: Final distribution and Lorenz curve
    ax1 = fig.add_subplot(gs[0, 0])
    plot_wealth_distribution(final_wealths, title="Final Wealth Distribution", ax=ax1)

    ax2 = fig.add_subplot(gs[0, 1])
    plot_lorenz_curve(final_wealths, title="Final Lorenz Curve", ax=ax2)

    # Middle row: Wealth percentiles and statistics
    ax3 = fig.add_subplot(gs[1, :])
    plot_wealth_evolution(history, ax=ax3)

    # Bottom left: Gini evolution
    ax4 = fig.add_subplot(gs[2, 0])
    plot_gini_evolution(history, ax=ax4)

    # Bottom right: Statistics evolution
    ax5 = fig.add_subplot(gs[2, 1])
    plot_wealth_statistics(history, ax=ax5)

    fig.suptitle("Wealth Distribution Dynamics Dashboard", fontsize=16, fontweight="bold")

    return fig


def plot_distribution_snapshots(
    history: pd.DataFrame,
    time_steps: List[int],
    bins: int = 30,
    figsize: tuple = (16, 10),
) -> Figure:
    """
    Plot wealth distribution histograms at multiple time steps.

    Args:
        history: DataFrame with columns [step, agent_id, wealth]
        time_steps: List of time steps to visualize
        bins: Number of histogram bins
        figsize: Figure size tuple

    Returns:
        Matplotlib Figure object

    Economic Intuition:
        Comparing distributions at different time points shows how
        the shape evolves - from uniform initial state to potentially
        highly skewed final state.
    """
    n_plots = len(time_steps)
    n_cols = min(3, n_plots)
    n_rows = (n_plots + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_plots == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    for i, step in enumerate(time_steps):
        step_data = history[history["step"] == step]["wealth"].values
        plot_wealth_distribution(
            step_data, title=f"Time Step {step}", bins=bins, ax=axes[i]
        )

    # Hide unused subplots
    for i in range(n_plots, len(axes)):
        axes[i].set_visible(False)

    fig.suptitle("Wealth Distribution Evolution", fontsize=16, fontweight="bold")
    plt.tight_layout()

    return fig
