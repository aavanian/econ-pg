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
    Manages the agent-based wealth distribution simulation with multiplicative growth.

    The simulation evolves a population of agents over discrete time steps,
    with each agent experiencing heterogeneous growth rates. Rich agents
    compound faster, leading to increasing inequality over time.

    Attributes:
        num_agents: Number of agents in the population
        initial_wealth_min: Minimum initial wealth (uniform distribution)
        initial_wealth_max: Maximum initial wealth (uniform distribution)
        aggregate_growth_per_step: Aggregate growth rate per time step in % (e.g., 2.0 = 2%)
        wealth_change_std: Standard deviation of individual growth rates in percentage
                          points (e.g., 5.0 means rates vary by ±5 percentage points)
        random_seed: Seed for reproducibility (optional)
        agents: List of Agent objects (initialized automatically)
        history: DataFrame tracking wealth over time (populated during simulation)

    Economic Intuition:
        This model captures wealth concentration dynamics:
        1. Agents start with heterogeneous initial endowments
        2. Each agent gets their own growth rate drawn from a distribution
        3. Growth is multiplicative: W[i,t+1] = W[i,t] × (1 + gr[i]/100)
        4. Rich agents gain more in absolute terms → inequality increases
        5. The wealth-weighted average of growth rates equals the target rate
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
        Generate wealth changes using multiplicative growth with heterogeneous rates.

        Returns:
            Array of wealth changes, one per agent

        Economic Intuition:
            Each agent experiences their own growth rate drawn from a distribution.
            Rich agents compound faster (multiplicative effect), leading to
            increasing inequality over time. The wealth-weighted average of
            individual growth rates equals the aggregate target rate.

        Algorithm:
            1. Draw individual growth rates: raw_gr[i] ~ N(0, σ²) in percentage points
            2. Calculate wealth-weighted average: avg = sum(W[i]×raw_gr[i]) / sum(W[i])
            3. Adjust to satisfy constraint: gr[i] = raw_gr[i] + (GR - avg)
            4. Calculate absolute changes: change[i] = W[i] × (gr[i] / 100)

        Constraint:
            sum(W[i] × gr[i]) / sum(W[i]) = aggregate_growth_per_step
        """
        # Get current wealth levels
        current_wealths = np.array([agent.wealth for agent in self.agents])
        total_wealth = np.sum(current_wealths)

        # Draw raw growth rates from normal distribution (in percentage points)
        raw_growth_rates = np.random.normal(0, self.wealth_change_std, self.num_agents)

        # Calculate wealth-weighted average growth rate
        weighted_avg = np.sum(current_wealths * raw_growth_rates) / total_wealth

        # Adjust growth rates to satisfy aggregate constraint
        # All rates shifted by same amount so wealth-weighted average = target
        adjustment = self.aggregate_growth_per_step - weighted_avg
        adjusted_growth_rates = raw_growth_rates + adjustment

        # Verify constraint (wealth-weighted average should equal target)
        verify_avg = np.sum(current_wealths * adjusted_growth_rates) / total_wealth
        assert np.isclose(
            verify_avg, self.aggregate_growth_per_step, rtol=1e-10
        ), f"Growth rate constraint violated: {verify_avg} != {self.aggregate_growth_per_step}"

        # Calculate absolute wealth changes using multiplicative growth
        # change[i] = W[i] × (gr[i] / 100)
        wealth_changes = current_wealths * (adjusted_growth_rates / 100.0)

        return wealth_changes

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
