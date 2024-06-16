"""Random agent"""

import random

from .base import BaseAgent


class RandomAgent(BaseAgent):
    """Random agent

    Buy, sell or do nothing only based on random chance
    """

    def perform_action(self, *args, **kwargs) -> None:
        """Buy, sell or do nothing with:
        - 25% chance of buying
        - 25% chance of selling
        - 50% chance of doing nothing
        """
        chance = random.random()

        if chance < 0.25:
            self.buy()
        elif chance < 0.5:
            self.sell()
