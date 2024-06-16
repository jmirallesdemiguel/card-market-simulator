"""Market tests"""

import pytest

from markets.card_market import CardMarket
from markets.exceptions import OutOfStockException


@pytest.fixture
def setup_market():
    return CardMarket(stock=100, starting_price=5.0)


def test_initialization(setup_market):
    market = setup_market
    assert market.stock == 100
    assert market.current_price == 5.0
    assert market.previous_price is None


def test_buy_reduces_stock_and_increases_price(setup_market):
    market = setup_market
    initial_stock = market.stock
    initial_price = market.current_price

    market.buy()

    assert market.stock == initial_stock - 1
    assert market.current_price == pytest.approx(initial_price * 1.001, rel=1e-3)


def test_buy_out_of_stock_raises_exception():
    market = CardMarket(stock=0, starting_price=5.0)

    with pytest.raises(OutOfStockException):
        market.buy()


def test_sell_increases_stock_and_decreases_price(setup_market):
    market = setup_market
    initial_stock = market.stock
    initial_price = market.current_price

    market.sell()

    assert market.stock == initial_stock + 1
    assert market.current_price == pytest.approx(initial_price * 0.999, rel=1e-3)


def test_get_price_change_with_no_previous_price(setup_market):
    market = setup_market
    assert market.get_price_change() is None


def test_get_price_change_with_previous_price(setup_market):
    market = setup_market
    market.previous_price = 4.9
    market.current_price = 5.0

    price_change = market.get_price_change()

    assert price_change == pytest.approx((5.0 - 4.9) / 4.9, rel=1e-3)
