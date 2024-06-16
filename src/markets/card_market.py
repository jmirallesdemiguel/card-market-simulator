"""Card market class"""

from .exceptions import OutOfStockException


class CardMarket:
    """Card market

    Keeps track on existing stock and price, that change on buy and sell operations.
    Also keeps track of the previous iteration final price.
    """

    def __init__(self, stock: int, starting_price: float) -> None:
        self.stock: int = stock
        self.current_price: float = starting_price
        self.previous_price: None | float = None

    def buy(self) -> None:
        """Buy a card from the market"""
        if self.stock == 0:
            raise OutOfStockException

        self.stock -= 1
        self.current_price *= 1.001

    def sell(self) -> None:
        """Sell a card to the market"""
        self.stock += 1
        self.current_price *= 0.999

    def get_price_change(self) -> None | float:
        """Return the price change with the previous market iteration, if available"""
        if self.previous_price is None:
            return None

        return (self.current_price - self.previous_price) / self.previous_price
