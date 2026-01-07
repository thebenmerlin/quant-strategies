"""
Quant Strategies Module

Contains implementations of trading strategies that generate signals
based on price data. Each strategy outputs signals in {-1, 0, 1} format.
"""

from .momentum import momentum_strategy
from .mean_reversion import mean_reversion_strategy

__all__ = ["momentum_strategy", "mean_reversion_strategy"]
