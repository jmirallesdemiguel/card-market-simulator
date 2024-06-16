"""Base Agent class to be extended"""

from markets.card_market import CardMarket
from markets.exceptions import OutOfStockException


class BaseAgent:
    """Extendable base agent

    Can buy or sell from the market, which then increases or reduces stock and cash balance
    """

    def __init__(self, market: CardMarket, cash_balance: float) -> None:
        self.stock: int = 0
        self.market = market
        self.cash_balance = cash_balance

    def buy(self) -> None:
        """Buy a card from the market"""
        if self.cash_balance < self.market.current_price:
            return

        buying_price = self.market.current_price

        try:
            self.market.buy()
        except OutOfStockException:
            return

        self.stock += 1
        self.cash_balance -= buying_price

    def sell(self) -> None:
        """Sell a card from the market"""
        if self.stock == 0:
            return

        self.stock -= 1
        self.cash_balance += self.market.current_price
        self.market.sell()

    def perform_action(self, *args, **kwargs) -> None:
        """Buy, sell or do nothing"""
        raise NotImplementedError
