"""Exceptions for the markets domain"""


class OutOfStockException(Exception):
    """The market doesn't have any cards left"""
