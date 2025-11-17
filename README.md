# Quant Strategies

A collection of systematic trading strategies.  
The goal of this project is to produce clean, modular, production-style implementations of classical and modern trading strategies, complete with backtesting, performance metrics, and data pipelines.

---

## Overview

This repository contains quantitative trading strategies written to replicate real-world research workflows used by quant funds.  
Each strategy follows the same structure:

- data ingestion  
- signal generation  
- position logic  
- backtesting  
- performance evaluation  

All code is organized to be reusable, readable, and extensible.

---

## Project Structure

quant-strategies/
│
├── data/                 # Sample datasets / cached data
│   └── sample_data.csv
│
├── notebooks/            # Jupyter notebooks for exploration and analysis
│   └── momentum_strategy.ipynb
│
├── src/                  # Core source code
│   ├── init.py
│   ├── data_loader.py    # Live market data loader (Yahoo Finance)
│   ├── metrics.py        # Sharpe Ratio, Max Drawdown, etc.
│   ├── utils.py          # Helper functions
│   └── strategies/
│       ├── init.py
│       ├── momentum.py   # Momentum strategy logic
│       └── mean_reversion.py
│
├── plots/                # Exported charts
│   └── .gitkeep
│
└── README.md 


## Current

- Repository structure completed  
- Data downloading module implemented  
- Initial notebook created (momentum strategy setup)  
- Strategy modules scaffolded  

---

## Strategy Modules (Planned Rollout)

- Momentum  
- Mean Reversion  
- Multi-Factor Momentum  
- Volatility Filters  
- RSI-based strategies  
- Breakout strategies  
- Statistical Arbitrage (Pairs Trading)  
- Machine Learning models  
- Portfolio optimization (Markowitz)  
- Risk and performance reporting  

Each addition will include:

- backtest implementation  
- performance metrics  
- plots  
- documentation  

## Requirements

- Python 3.10+  
- pandas  
- numpy  
- matplotlib  
- yfinance  
- jupyter  

Install dependencies:
pip install pandas numpy matplotlib yfinance jupyter
---

## Author

Gajanan Barve  
CS Major • Quant & FinTech Developer  
github.com/thebenmerlin


