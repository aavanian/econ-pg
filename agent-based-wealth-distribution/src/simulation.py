"""
Simulation engine for agent-based wealth distribution model.

This module orchestrates the time-stepping dynamics of the wealth distribution
simulation, ensuring aggregate wealth growth constraints are satisfied.
"""

from dataclasses import dataclass, field
from typing import Callable, Optional
import numpy as np
import pandas as pd

from .agents import Agent


@dataclass
class Simulation:
    """
    Manages the agent-based wealth distribution simulation.

    The simulation evolves a population of agents over discrete time steps,
    with each agent's wealth changing according to a stochastic process
    constrained by aggregate growth targets.

    Attributes:
        num_agents: Number of agents in the population
        initial_wealth_min: Minimum initial wealth (uniform distribution)
        initial_wealth_max: Maximum initial wealth (uniform distribution)
        aggregate_growth_per_step: Percentage growth rate per time step (e.g., 2.0 = 2%)
        wealth_change_std: Standard deviation of individual wealth changes
        random_seed: Seed for reproducibility (optional)
        agents: List of Agent objects (initialized automatically)
        history: DataFrame tracking wealth over time (populated during simulation)

    Economic Intuition:
        This model captures the dynamics of wealth distribution in an economy where:
        1. Agents start with heterogeneous initial endowments
        2. The economy grows at a fixed percentage rate (compound growth)
        3. Individual outcomes are stochastic, creating winners and losers
        4. The interplay between systematic growth and random shocks drives
           the evolution of inequality
    """

    num_agents: int = 100
    initial_wealth_min: float = 0.0
    initial_wealth_max: float = 100.0
    aggregate_growth_per_step: float = 2.0
    wealth_change_std: float = 5.0
    random_seed: Optional[int] = None
    agents: list[Agent] = field(default_factory=list, init=False, repr=False)
    history: pd.DataFrame = field(default_factory=pd.DataFrame, init=False, repr=False)

    def __post_init__(self):
        """Initialize the simulation and validate parameters."""
        if self.num_agents <= 0:
            raise ValueError("Number of agents must be positive")
        if self.initial_wealth_min < 0:
            raise ValueError("Minimum initial wealth cannot be negative")
        if self.initial_wealth_max < self.initial_wealth_min:
            raise ValueError("Maximum initial wealth must be >= minimum")
        if self.wealth_change_std < 0:
            raise ValueError("Standard deviation cannot be negative")

        # Set random seed for reproducibility
        if self.random_seed is not None:
            np.random.seed(self.random_seed)

        # Initialize agents with uniform wealth distribution
        self._initialize_agents()

    def _initialize_agents(self) -> None:
        """
        Create agents with uniformly distributed initial wealth.

        Economic Intuition:
            Starting with a uniform distribution provides a baseline to observe
            how inequality emerges purely from the stochastic dynamics, without
            being predetermined by initial conditions.
        """
        initial_wealths = np.random.uniform(
            self.initial_wealth_min, self.initial_wealth_max, self.num_agents
        )

        self.agents = [
            Agent(agent_id=i, wealth=wealth)
            for i, wealth in enumerate(initial_wealths)
        ]

    def _generate_wealth_changes(self) -> np.ndarray:
        """
        Generate wealth changes that satisfy the aggregate growth constraint.

        Returns:
            Array of wealth changes, one per agent

        Economic Intuition:
            Individual wealth changes are drawn from a normal distribution
            (representing idiosyncratic shocks), then normalized to ensure
            the aggregate equals the target growth rate. This creates a zero-sum
            component (relative gains/losses) plus systematic compound growth.

        Algorithm:
            1. Calculate target absolute growth: current_total × (rate / 100)
            2. Draw random changes from N(0, σ²)
            3. Adjust so sum equals target absolute growth:
               adjusted_change[i] = raw_change[i] + (target - sum(raw)) / n
        """
        # Calculate current total wealth
        current_total_wealth = np.sum([agent.wealth for agent in self.agents])

        # Calculate target absolute growth based on percentage rate
        target_growth = current_total_wealth * (self.aggregate_growth_per_step / 100.0)

        # Draw random changes from normal distribution (mean=0)
        raw_changes = np.random.normal(0, self.wealth_change_std, self.num_agents)

        # Calculate the adjustment needed to hit target aggregate growth
        current_sum = np.sum(raw_changes)
        adjustment = (target_growth - current_sum) / self.num_agents

        # Apply adjustment uniformly to all agents
        adjusted_changes = raw_changes + adjustment

        # Verify constraint is satisfied (within numerical precision)
        assert np.isclose(
            np.sum(adjusted_changes), target_growth
        ), "Aggregate growth constraint violated"

        return adjusted_changes

    def step(self) -> None:
        """
        Execute one time step of the simulation.

        Updates all agents' wealth according to the stochastic process
        while maintaining the aggregate growth constraint.
        """
        wealth_changes = self._generate_wealth_changes()

        for agent, change in zip(self.agents, wealth_changes):
            agent.update_wealth(change)

    def run(self, num_steps: int, record_interval: int = 1) -> pd.DataFrame:
        """
        Run the simulation for a specified number of time steps.

        Args:
            num_steps: Number of time steps to simulate
            record_interval: Record history every N steps (default: 1)

        Returns:
            DataFrame with columns [step, agent_id, wealth]

        Economic Intuition:
            Over many time steps, we can observe how wealth inequality evolves.
            Key questions: Does inequality increase over time? Do some agents
            accumulate vast wealth while others approach zero? What is the
            steady-state distribution?
        """
        if num_steps <= 0:
            raise ValueError("Number of steps must be positive")

        # Record initial state
        records = []
        if 0 % record_interval == 0:
            for agent in self.agents:
                records.append({"step": 0, "agent_id": agent.agent_id, "wealth": agent.wealth})

        # Run simulation
        for step in range(1, num_steps + 1):
            self.step()

            # Record state at specified intervals
            if step % record_interval == 0:
                for agent in self.agents:
                    records.append(
                        {"step": step, "agent_id": agent.agent_id, "wealth": agent.wealth}
                    )

        # Convert to DataFrame
        self.history = pd.DataFrame(records)
        return self.history

    def get_wealth_array(self) -> np.ndarray:
        """
        Get current wealth levels as a numpy array.

        Returns:
            Array of wealth values for all agents
        """
        return np.array([agent.wealth for agent in self.agents])

    def get_statistics(self) -> dict:
        """
        Calculate summary statistics of current wealth distribution.

        Returns:
            Dictionary with mean, median, std, min, max, gini coefficient

        Economic Intuition:
            The Gini coefficient measures inequality (0 = perfect equality,
            1 = one agent has all wealth). Other statistics provide a
            complete picture of the distribution shape.
        """
        wealths = self.get_wealth_array()
        wealths_sorted = np.sort(wealths)

        # Calculate Gini coefficient
        n = len(wealths)
        cumsum = np.cumsum(wealths_sorted)
        gini = (2 * np.sum((np.arange(n) + 1) * wealths_sorted)) / (n * cumsum[-1]) - (
            n + 1
        ) / n

        return {
            "mean": np.mean(wealths),
            "median": np.median(wealths),
            "std": np.std(wealths),
            "min": np.min(wealths),
            "max": np.max(wealths),
            "gini": gini,
            "total_wealth": np.sum(wealths),
        }

    def __repr__(self) -> str:
        """Human-readable representation of the simulation."""
        stats = self.get_statistics()
        return (
            f"Simulation(agents={self.num_agents}, "
            f"mean_wealth={stats['mean']:.2f}, "
            f"gini={stats['gini']:.3f})"
        )
