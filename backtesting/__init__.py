"""
Backtesting Module

Contains vectorized backtesting engine and performance metrics.
"""

from .engine import backtest
from .metrics import sharpe_ratio, max_drawdown, compute_metrics

__all__ = ["backtest", "sharpe_ratio", "max_drawdown", "compute_metrics"]
