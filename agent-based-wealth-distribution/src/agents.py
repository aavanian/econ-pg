"""
Agent-based model components for wealth distribution simulation.

This module defines the Agent class representing individuals in the economy
with wealth that evolves over time according to stochastic processes.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Agent:
    """
    Represents an individual agent in the wealth distribution simulation.

    Each agent has a unique ID and maintains a wealth level that changes
    over time through random shocks and systematic growth.

    Attributes:
        agent_id: Unique identifier for the agent
        wealth: Current wealth level (non-negative)

    Economic Intuition:
        Agents represent individuals or households in an economy. Their wealth
        evolves through a combination of systematic growth (representing
        economic growth or returns) and idiosyncratic shocks (representing
        individual luck, business success/failure, etc.).
    """

    agent_id: int
    wealth: float

    def __post_init__(self):
        """Validate agent parameters."""
        if self.wealth < 0:
            raise ValueError(f"Agent {self.agent_id}: Wealth cannot be negative")

    def update_wealth(self, change: float) -> None:
        """
        Update agent's wealth by a specified amount.

        Args:
            change: The change in wealth (can be positive or negative)

        Raises:
            ValueError: If the update would result in negative wealth

        Economic Intuition:
            This represents the wealth change from various economic processes:
            income, returns on investment, consumption, losses, etc.
        """
        new_wealth = self.wealth + change
        if new_wealth < 0:
            # Allow wealth to go to zero but not negative
            # This represents bankruptcy or hitting a floor
            self.wealth = 0.0
        else:
            self.wealth = new_wealth

    def get_state(self) -> dict:
        """
        Return agent's current state.

        Returns:
            Dictionary containing agent's ID and wealth
        """
        return {"agent_id": self.agent_id, "wealth": self.wealth}

    def __repr__(self) -> str:
        """Human-readable representation of the agent."""
        return f"Agent(id={self.agent_id}, wealth={self.wealth:.2f})"
