"""
Simple supply and demand market equilibrium model.

This module provides a basic implementation of market equilibrium
using linear supply and demand curves.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class Market:
    """
    A simple market with linear supply and demand curves.

    Attributes:
        demand_intercept: Price intercept of demand curve (a in P = a - bQ)
        demand_slope: Slope of demand curve (b in P = a - bQ), must be positive
        supply_intercept: Price intercept of supply curve (c in P = c + dQ)
        supply_slope: Slope of supply curve (d in P = c + dQ), must be positive
    """

    demand_intercept: float = 100.0
    demand_slope: float = 2.0
    supply_intercept: float = 20.0
    supply_slope: float = 1.5

    def __post_init__(self):
        """Validate parameters."""
        if self.demand_intercept <= 0:
            raise ValueError("Demand intercept must be positive")
        if self.demand_slope <= 0:
            raise ValueError("Demand slope must be positive")
        if self.supply_intercept < 0:
            raise ValueError("Supply intercept must be non-negative")
        if self.supply_slope <= 0:
            raise ValueError("Supply slope must be positive")
        if self.demand_intercept <= self.supply_intercept:
            raise ValueError("Demand intercept must exceed supply intercept for equilibrium")

    def demand_price(self, quantity: float) -> float:
        """
        Calculate price on the demand curve for a given quantity.

        Args:
            quantity: Quantity demanded

        Returns:
            Price consumers are willing to pay
        """
        return self.demand_intercept - self.demand_slope * quantity

    def supply_price(self, quantity: float) -> float:
        """
        Calculate price on the supply curve for a given quantity.

        Args:
            quantity: Quantity supplied

        Returns:
            Price suppliers require
        """
        return self.supply_intercept + self.supply_slope * quantity

    def equilibrium(self) -> Tuple[float, float]:
        """
        Calculate market equilibrium price and quantity.

        At equilibrium: demand_price(Q*) = supply_price(Q*)
        Solving: a - bQ = c + dQ
                 Q* = (a - c) / (b + d)
                 P* = a - bQ*

        Returns:
            Tuple of (equilibrium_price, equilibrium_quantity)
        """
        eq_quantity = (self.demand_intercept - self.supply_intercept) / (
            self.demand_slope + self.supply_slope
        )
        eq_price = self.demand_price(eq_quantity)

        return eq_price, eq_quantity

    def consumer_surplus(self) -> float:
        """
        Calculate consumer surplus at equilibrium.

        Consumer surplus is the area under the demand curve above the equilibrium price.
        For a linear demand curve, this is a triangle: 0.5 * base * height

        Returns:
            Consumer surplus value
        """
        eq_price, eq_quantity = self.equilibrium()
        # Height: difference between max willingness to pay and equilibrium price
        # Base: equilibrium quantity
        return 0.5 * eq_quantity * (self.demand_intercept - eq_price)

    def producer_surplus(self) -> float:
        """
        Calculate producer surplus at equilibrium.

        Producer surplus is the area above the supply curve below the equilibrium price.
        For a linear supply curve, this is a triangle: 0.5 * base * height

        Returns:
            Producer surplus value
        """
        eq_price, eq_quantity = self.equilibrium()
        # Height: difference between equilibrium price and minimum supply price
        # Base: equilibrium quantity
        return 0.5 * eq_quantity * (eq_price - self.supply_intercept)

    def total_surplus(self) -> float:
        """
        Calculate total surplus (sum of consumer and producer surplus).

        Returns:
            Total economic surplus
        """
        return self.consumer_surplus() + self.producer_surplus()

    def __repr__(self) -> str:
        """String representation of the market."""
        eq_price, eq_quantity = self.equilibrium()
        return (
            f"Market(\n"
            f"  Demand: P = {self.demand_intercept} - {self.demand_slope}Q\n"
            f"  Supply: P = {self.supply_intercept} + {self.supply_slope}Q\n"
            f"  Equilibrium: P* = {eq_price:.2f}, Q* = {eq_quantity:.2f}\n"
            f"  Consumer Surplus: {self.consumer_surplus():.2f}\n"
            f"  Producer Surplus: {self.producer_surplus():.2f}\n"
            f"  Total Surplus: {self.total_surplus():.2f}\n"
            f")"
        )


def main():
    """Demonstrate basic market equilibrium calculation."""
    print("Simple Supply and Demand Market\n" + "=" * 40 + "\n")

    # Create market with default parameters
    market = Market()
    print(market)

    print("\n" + "=" * 40)
    print("\nSensitivity Analysis: Effect of Demand Shift\n")

    # Show how equilibrium changes with demand shift
    for intercept in [80, 100, 120]:
        shifted_market = Market(demand_intercept=intercept)
        price, quantity = shifted_market.equilibrium()
        print(f"Demand intercept = {intercept}: P* = {price:.2f}, Q* = {quantity:.2f}")


if __name__ == "__main__":
    main()
