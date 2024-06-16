"""Trend contrarian agent tests"""

from unittest.mock import MagicMock, patch

import pytest

from agents import TrendContrarianAgent
from markets.card_market import CardMarket


@pytest.fixture
def setup_contrarian_agent():
    mock_market = MagicMock(spec=CardMarket)
    mock_market.current_price = 5.0
    agent = TrendContrarianAgent(mock_market, cash_balance=100.0)
    return agent, mock_market


@patch("random.random", return_value=0.7)
def test_contrarian_agent_buy_on_price_drop(_, setup_contrarian_agent):
    agent, mock_market = setup_contrarian_agent
    mock_market.get_price_change.return_value = 0.98

    agent.perform_action()

    assert agent.stock == 1
    assert agent.cash_balance == 95.0
    mock_market.buy.assert_called_once()


@patch("random.random", return_value=0.19)
def test_contrarian_agent_sell_on_price_stability(_, setup_contrarian_agent):
    agent, mock_market = setup_contrarian_agent
    mock_market.get_price_change.return_value = 1.0
    agent.stock = 1

    agent.perform_action()

    assert agent.stock == 0
    assert agent.cash_balance == 105.0
    mock_market.sell.assert_called_once()


@patch("random.random", return_value=0.9)
def test_contrarian_agent_do_nothing(_, setup_contrarian_agent):
    agent, mock_market = setup_contrarian_agent
    mock_market.get_price_change.return_value = 0.98

    agent.perform_action()

    assert agent.stock == 0
    assert agent.cash_balance == 100.0
    mock_market.buy.assert_not_called()
    mock_market.sell.assert_not_called()
