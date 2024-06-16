"""Random agent tests"""

from unittest.mock import MagicMock, patch

import pytest

from agents import RandomAgent
from markets.card_market import CardMarket


@pytest.fixture
def setup_random_agent():
    mock_market = MagicMock(spec=CardMarket)
    mock_market.current_price = 5.0
    agent = RandomAgent(mock_market, cash_balance=100.0)
    return agent, mock_market


@patch("random.random", return_value=0.19)
def test_random_agent_buy(_, setup_random_agent):
    agent, mock_market = setup_random_agent

    agent.perform_action()

    assert agent.stock == 1
    assert agent.cash_balance == 95.0
    mock_market.buy.assert_called_once()


@patch("random.random", return_value=0.3)
def test_random_agent_sell(_, setup_random_agent):
    agent, mock_market = setup_random_agent
    agent.stock = 1

    agent.perform_action()

    assert agent.stock == 0
    assert agent.cash_balance == 105.0
    mock_market.sell.assert_called_once()


@patch("random.random", return_value=0.6)
def test_random_agent_do_nothing(_, setup_random_agent):
    agent, mock_market = setup_random_agent

    agent.perform_action()

    assert agent.stock == 0
    assert agent.cash_balance == 100.0
    mock_market.buy.assert_not_called()
    mock_market.sell.assert_not_called()
