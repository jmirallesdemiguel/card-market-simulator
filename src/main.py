"""Entry module of the project"""

import logging

from agents import (CustomAgent, RandomAgent, TrendContrarianAgent,
                    TrendFollowerAgent)
from markets import CardMarket
from simulators import Simulator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

if __name__ == "__main__":
    logging.info("Starting market simulation!")

    stock = 100000
    price = 5.0
    market = CardMarket(stock, price)
    logging.info(
        f"Created market with {stock} units of stock and a base price of {price}$"
    )

    cash_balance = 100.0
    agents = (
        [CustomAgent(market, cash_balance)]
        + [RandomAgent(market, cash_balance) for _ in range(51)]
        + [TrendContrarianAgent(market, cash_balance) for _ in range(24)]
        + [TrendFollowerAgent(market, cash_balance) for _ in range(24)]
    )
    logging.info(
        f"Created {len(agents)} agents with a starting cash balance of {cash_balance}$"
    )

    iterations = 1000
    logging.info(f"Starting simulation with {iterations} iterations")
    Simulator.run_simulation(market, agents, iterations)
