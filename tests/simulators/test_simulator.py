"""Simulator tests"""

from unittest.mock import MagicMock

import pytest

from agents import (CustomAgent, RandomAgent, TrendContrarianAgent,
                    TrendFollowerAgent)
from markets import CardMarket
from simulators import Simulator


@pytest.fixture
def setup_simulator():
    market = CardMarket(stock=100, starting_price=5.0)
    agents = [
        MagicMock(spec=CustomAgent, market=market, cash_balance=100.0),
        MagicMock(spec=RandomAgent, market=market, cash_balance=100.0),
        MagicMock(spec=TrendContrarianAgent, market=market, cash_balance=100.0),
        MagicMock(spec=TrendFollowerAgent, market=market, cash_balance=100.0),
    ]
    return market, agents


def test_simulation_updates_prices_and_previous_price(setup_simulator):
    market, agents = setup_simulator

    Simulator.run_simulation(market, agents, iterations=10)

    for agent in agents:
        assert agent.perform_action.call_count == 10

    assert market.previous_price == market.current_price


def test_simulation_calls_agents_in_random_order(mocker, setup_simulator):
    market, agents = setup_simulator

    random_sample = mocker.patch("random.sample", return_value=agents)

    Simulator.run_simulation(market, agents, iterations=10)

    random_sample.assert_called_with(agents, len(agents))


def test_simulation_with_empty_agents_list(mocker, setup_simulator):
    market, _ = setup_simulator
    agents = []

    random_sample = mocker.patch("random.sample", return_value=agents)

    Simulator.run_simulation(market, agents, iterations=10)

    random_sample.assert_not_called()


def test_simulation_respects_remaining_iterations(setup_simulator):
    market, agents = setup_simulator

    Simulator.run_simulation(market, agents, iterations=5)

    for agent in agents:
        assert agent.perform_action.call_count == 5
        call_args_list = agent.perform_action.call_args_list
        for i, call_args in enumerate(call_args_list):
            remaining_iterations = call_args[1]["remaining_iterations"]
            assert remaining_iterations == 5 - i
