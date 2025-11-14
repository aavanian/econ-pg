"""
Unit tests for Agent class.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import Agent


def test_agent_creation():
    """Test basic agent creation."""
    agent = Agent(agent_id=1, wealth=100.0)
    assert agent.agent_id == 1
    assert agent.wealth == 100.0


def test_agent_negative_wealth_initialization():
    """Test that negative initial wealth raises error."""
    with pytest.raises(ValueError):
        Agent(agent_id=1, wealth=-10.0)


def test_agent_update_wealth_positive():
    """Test wealth update with positive change."""
    agent = Agent(agent_id=1, wealth=100.0)
    agent.update_wealth(50.0)
    assert agent.wealth == 150.0


def test_agent_update_wealth_negative():
    """Test wealth update with negative change."""
    agent = Agent(agent_id=1, wealth=100.0)
    agent.update_wealth(-30.0)
    assert agent.wealth == 70.0


def test_agent_update_wealth_floor():
    """Test that wealth cannot go below zero."""
    agent = Agent(agent_id=1, wealth=50.0)
    agent.update_wealth(-100.0)  # Would be -50 without floor
    assert agent.wealth == 0.0


def test_agent_get_state():
    """Test get_state method."""
    agent = Agent(agent_id=5, wealth=123.45)
    state = agent.get_state()
    assert state["agent_id"] == 5
    assert state["wealth"] == 123.45


def test_agent_repr():
    """Test string representation."""
    agent = Agent(agent_id=1, wealth=100.0)
    repr_str = repr(agent)
    assert "Agent" in repr_str
    assert "id=1" in repr_str
    assert "100.00" in repr_str
