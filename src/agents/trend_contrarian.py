"""Trend Contrarian agent"""

import random

from .base import BaseAgent


class TrendContrarianAgent(BaseAgent):
    """Trend Contrarian agent

    Buys more often when prices decrease in relation to previous iteration
    """

    def perform_action(self, *args, **kwargs) -> None:
        """Buy, sell or do nothing based on:

        If the price of the previous market iteration has decreased 1% or more:
            - 75% chance of buying
            - 25% chance of doing nothing

        Otherwise:
            - 20% chance of selling
            - 80% chance of doing nothing
        """
        price_change = self.market.get_price_change()

        if price_change is not None and price_change <= 0.99:
            if random.random() < 0.75:
                self.buy()
        else:
            if random.random() < 0.20:
                self.sell()
