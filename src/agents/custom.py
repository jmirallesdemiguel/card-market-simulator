"""Custom agent class with special action algorithm"""

import random

from .base import BaseAgent


class CustomAgent(BaseAgent):
    """Custom agent with specific action algorithm

    Buys on both up and down trends on market price and sales more often otherwise.
    Always ends up with no cards.
    """

    def perform_action(self, remaining_iterations: int, *args, **kwargs) -> None:
        """Buy, sell or do nothing"""

        # Ensure ending without any stock
        if self.stock in [remaining_iterations, remaining_iterations - 1]:
            self.sell()
            return

        price_change = self.market.get_price_change()
        chance = random.random()

        if price_change is not None and price_change >= 1.01:
            if chance < 0.75:
                self.buy()
        elif price_change is not None and price_change <= 0.99:
            if chance < 0.75:
                self.buy()
        else:
            if chance < 0.40:
                self.sell()
