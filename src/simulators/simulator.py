"""Simulator class to run on markets and agents"""

import logging
import random

from agents import BaseAgent
from markets.card_market import CardMarket


class Simulator:
    """Market-Agents trade simulator

    Based on a market and some agents, performs a simulation of their actions over
    a certain number of iterations.
    """

    @staticmethod
    def run_simulation(
        market: CardMarket, agents: list[BaseAgent], iterations: int
    ) -> None:
        """Run a simulation between the given market and agents over the specified iterations

        On each iteration the order of the agents is shuffled and then they all perform an action
        sequentially.
        """
        if not agents:
            logging.warning("No agents received. Simulation not starting")
            return None

        for i in range(iterations):
            for agent in random.sample(agents, len(agents)):
                agent.perform_action(remaining_iterations=iterations - i)

            market.previous_price = market.current_price
            logging.info(
                f"End of iteration number: {i + 1} - Price: {market.current_price} - Stock: {market.stock}"
            )

        logging.info("End of simulation")
