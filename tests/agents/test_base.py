"""Base agent tests"""

from unittest.mock import MagicMock

import pytest

from agents import BaseAgent
from markets import CardMarket
from markets.exceptions import OutOfStockException


@pytest.fixture
def market_mock():
    market = MagicMock(spec=CardMarket)
    market.current_price = 5.0
    return market


@pytest.fixture
def agent_fix(market_mock) -> BaseAgent:
    agent = BaseAgent(market_mock, cash_balance=100.0)
    return agent


def test_buy_with_sufficient_balance(market_mock: MagicMock, agent_fix: BaseAgent):
    initial_balance = agent_fix.cash_balance
    buying_price = market_mock.current_price

    agent_fix.buy()

    assert agent_fix.stock == 1
    assert agent_fix.cash_balance == initial_balance - buying_price
    market_mock.buy.assert_called_once()


def test_buy_out_of_stock(market_mock: MagicMock, agent_fix: BaseAgent):
    market_mock.buy.side_effect = OutOfStockException

    agent_fix.buy()

    assert agent_fix.stock == 0
    assert agent_fix.cash_balance == 100.0
    market_mock.buy.assert_called_once()


def test_buy_insufficient_balance(market_mock: MagicMock, agent_fix: BaseAgent):
    agent_fix.cash_balance = 3.0

    agent_fix.buy()

    assert agent_fix.stock == 0
    assert agent_fix.cash_balance == 3.0
    market_mock.buy.assert_not_called()


def test_sell_with_stock(market_mock: MagicMock, agent_fix: BaseAgent):
    agent_fix.stock = 2
    initial_balance = agent_fix.cash_balance
    selling_price = market_mock.current_price

    agent_fix.sell()

    assert agent_fix.stock == 1
    assert agent_fix.cash_balance == initial_balance + selling_price
    market_mock.sell.assert_called_once()


def test_sell_no_stock(market_mock: MagicMock, agent_fix: BaseAgent):
    agent_fix.sell()

    assert agent_fix.stock == 0
    assert agent_fix.cash_balance == 100.0
    market_mock.sell.assert_not_called()


def test_perform_action_not_implemented(agent_fix: BaseAgent):
    with pytest.raises(NotImplementedError):
        agent_fix.perform_action()
