import pandas as pd

def load_price_series(
    filepath: str,
    price_col: str = "close",
    date_col: str = "date"
) -> pd.Series:
    """
    Loads price data from CSV and returns a clean price Series.

    filepath  : path to CSV file
    price_col : column containing prices
    date_col  : column containing dates
    """

    df = pd.read_csv(filepath)
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    prices = df.set_index(date_col)[price_col]
    prices = prices.dropna()

    return prices
