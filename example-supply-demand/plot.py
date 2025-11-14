"""
Visualization tools for supply and demand analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from market import Market


def plot_supply_demand(market: Market, save_path: str = None):
    """
    Plot supply and demand curves with equilibrium point.

    Args:
        market: Market instance to visualize
        save_path: Optional path to save the figure
    """
    # Calculate equilibrium
    eq_price, eq_quantity = market.equilibrium()

    # Generate quantity range for plotting
    # From 0 to slightly beyond equilibrium
    q_max = eq_quantity * 1.5
    quantities = np.linspace(0, q_max, 100)

    # Calculate prices along both curves
    demand_prices = market.demand_price(quantities)
    supply_prices = market.supply_price(quantities)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))

    # Plot supply and demand curves
    ax.plot(quantities, demand_prices, "b-", linewidth=2, label="Demand")
    ax.plot(quantities, supply_prices, "r-", linewidth=2, label="Supply")

    # Mark equilibrium point
    ax.plot(eq_quantity, eq_price, "go", markersize=12, label="Equilibrium", zorder=5)

    # Draw dashed lines to axes
    ax.plot([eq_quantity, eq_quantity], [0, eq_price], "g--", alpha=0.5, linewidth=1)
    ax.plot([0, eq_quantity], [eq_price, eq_price], "g--", alpha=0.5, linewidth=1)

    # Annotations
    ax.annotate(
        f"E: (Q*={eq_quantity:.1f}, P*={eq_price:.1f})",
        xy=(eq_quantity, eq_price),
        xytext=(eq_quantity * 1.15, eq_price * 1.1),
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="yellow", alpha=0.7),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3"),
    )

    # Shade consumer surplus (area under demand, above price)
    q_range = np.linspace(0, eq_quantity, 50)
    ax.fill_between(
        q_range,
        market.demand_price(q_range),
        eq_price,
        alpha=0.3,
        color="blue",
        label=f"Consumer Surplus = {market.consumer_surplus():.1f}",
    )

    # Shade producer surplus (area above supply, below price)
    ax.fill_between(
        q_range,
        market.supply_price(q_range),
        eq_price,
        alpha=0.3,
        color="red",
        label=f"Producer Surplus = {market.producer_surplus():.1f}",
    )

    # Labels and formatting
    ax.set_xlabel("Quantity (Q)", fontsize=12)
    ax.set_ylabel("Price (P)", fontsize=12)
    ax.set_title("Supply and Demand Market Equilibrium", fontsize=14, fontweight="bold")
    ax.legend(loc="best", fontsize=10)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.set_xlim(0, q_max)
    ax.set_ylim(0, max(market.demand_intercept, supply_prices[-1]) * 1.1)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Plot saved to {save_path}")

    plt.show()


def plot_comparative_statics(base_market: Market):
    """
    Show how equilibrium changes with parameter shifts.

    Args:
        base_market: Base market for comparison
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Left plot: Demand shift
    ax1 = axes[0]
    q_max = 50
    quantities = np.linspace(0, q_max, 100)

    # Original supply
    supply_prices = base_market.supply_price(quantities)
    ax1.plot(quantities, supply_prices, "r-", linewidth=2, label="Supply")

    # Different demand curves
    demand_shifts = [80, 100, 120]
    colors = ["blue", "green", "purple"]
    for intercept, color in zip(demand_shifts, colors):
        market = Market(
            demand_intercept=intercept,
            demand_slope=base_market.demand_slope,
            supply_intercept=base_market.supply_intercept,
            supply_slope=base_market.supply_slope,
        )
        demand_prices = market.demand_price(quantities)
        eq_price, eq_quantity = market.equilibrium()

        ax1.plot(quantities, demand_prices, color=color, linewidth=2, alpha=0.7)
        ax1.plot(eq_quantity, eq_price, "o", color=color, markersize=10)
        ax1.annotate(
            f"D={intercept}",
            xy=(eq_quantity, eq_price),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9,
        )

    ax1.set_xlabel("Quantity (Q)", fontsize=12)
    ax1.set_ylabel("Price (P)", fontsize=12)
    ax1.set_title("Effect of Demand Shifts", fontsize=13, fontweight="bold")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Right plot: Supply shift
    ax2 = axes[1]

    # Original demand
    demand_prices = base_market.demand_price(quantities)
    ax2.plot(quantities, demand_prices, "b-", linewidth=2, label="Demand")

    # Different supply curves
    supply_intercepts = [10, 20, 30]
    colors = ["red", "orange", "brown"]
    for intercept, color in zip(supply_intercepts, colors):
        market = Market(
            demand_intercept=base_market.demand_intercept,
            demand_slope=base_market.demand_slope,
            supply_intercept=intercept,
            supply_slope=base_market.supply_slope,
        )
        supply_prices = market.supply_price(quantities)
        eq_price, eq_quantity = market.equilibrium()

        ax2.plot(quantities, supply_prices, color=color, linewidth=2, alpha=0.7)
        ax2.plot(eq_quantity, eq_price, "o", color=color, markersize=10)
        ax2.annotate(
            f"S={intercept}",
            xy=(eq_quantity, eq_price),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9,
        )

    ax2.set_xlabel("Quantity (Q)", fontsize=12)
    ax2.set_ylabel("Price (P)", fontsize=12)
    ax2.set_title("Effect of Supply Shifts", fontsize=13, fontweight="bold")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.show()


def main():
    """Generate visualizations."""
    print("Generating supply and demand visualizations...\n")

    # Create market
    market = Market()

    # Basic equilibrium plot
    print("1. Basic equilibrium plot")
    plot_supply_demand(market)

    # Comparative statics
    print("\n2. Comparative statics (demand and supply shifts)")
    plot_comparative_statics(market)


if __name__ == "__main__":
    main()
