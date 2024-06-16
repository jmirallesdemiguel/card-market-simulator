"""Custom agent tests"""

from unittest.mock import MagicMock, patch

import pytest

from agents import (CustomAgent, RandomAgent, TrendContrarianAgent,
                    TrendFollowerAgent)
from markets.card_market import CardMarket
from simulators import Simulator


@pytest.fixture
def setup_custom_agent():
    mock_market = MagicMock(spec=CardMarket)
    mock_market.current_price = 5.0
    mock_market.get_price_change = MagicMock(return_value=1.01)
    agent = CustomAgent(mock_market, cash_balance=100.0)
    return agent, mock_market


def test_custom_agent_sell_on_remaining_stock(setup_custom_agent):
    agent, mock_market = setup_custom_agent
    agent.stock = 5

    agent.perform_action(remaining_iterations=5)

    assert agent.stock == 4
    assert agent.cash_balance == 105.0
    mock_market.sell.assert_called_once()


@patch("random.random", return_value=0.7)
def test_custom_agent_buy_on_price_increase(_, setup_custom_agent):
    agent, mock_market = setup_custom_agent
    mock_market.get_price_change.return_value = 1.02

    agent.perform_action(remaining_iterations=10)

    assert agent.stock == 1
    assert agent.cash_balance == 95.0
    mock_market.buy.assert_called_once()


@patch("random.random", return_value=0.8)
def test_custom_agent_no_buy_on_high_random(_, setup_custom_agent):
    agent, mock_market = setup_custom_agent
    mock_market.get_price_change.return_value = 1.02

    agent.perform_action(remaining_iterations=10)

    assert agent.stock == 0
    assert agent.cash_balance == 100.0
    mock_market.buy.assert_not_called()


@patch("random.random", return_value=0.3)
def test_custom_agent_buy_on_price_decrease(_, setup_custom_agent):
    agent, mock_market = setup_custom_agent
    mock_market.get_price_change.return_value = 0.98

    agent.perform_action(remaining_iterations=10)

    assert agent.stock == 1
    assert agent.cash_balance == 95.0
    mock_market.buy.assert_called_once()


@patch("random.random", return_value=0.39)
def test_custom_agent_sell_on_stable_price(_, setup_custom_agent):
    agent, mock_market = setup_custom_agent
    mock_market.get_price_change.return_value = 1.0
    agent.stock = 1

    agent.perform_action(remaining_iterations=10)

    assert agent.stock == 0
    assert agent.cash_balance == 105.0
    mock_market.sell.assert_called_once()


def test_custom_agent_ends_with_no_cards():
    initial_stock = 100000
    initial_price = 5.0
    initial_cash = 100.0
    iterations = 1000

    market = CardMarket(stock=initial_stock, starting_price=initial_price)

    custom_agent = CustomAgent(market, initial_cash)
    random_agents = [RandomAgent(market, initial_cash) for _ in range(5)]
    trend_contrarian_agents = [
        TrendContrarianAgent(market, initial_cash) for _ in range(5)
    ]
    trend_follower_agents = [TrendFollowerAgent(market, initial_cash) for _ in range(5)]

    agents = (
        [custom_agent] + random_agents + trend_contrarian_agents + trend_follower_agents
    )

    Simulator.run_simulation(market, agents, iterations)

    assert (
        custom_agent.stock == 0
    ), f"Expected 0 cards for CustomAgent, but got {custom_agent.stock}"
