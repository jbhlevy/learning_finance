import yfinance as yf
import pandas as pd


def batch_query_stock_price(
    tickers: list,
    start_date: str = "2022-01-01",
    end_date: str = "2023-12-31",
    interval: str = "1d",
) -> dict:
    stocks = yf.Tickers(tickers).tickers
    stocks_price = {
        ticker: yf_object.history(start=start_date, end=end_date, interval=interval)[
            "Close"
        ]
        for ticker, yf_object in stocks.items()
    }

    return stocks_price


if __name__ == "__main__":
    tickers_list = ["AAPL", "AMZN", "NKE"]
    prices = batch_query_stock_price(tickers_list)
    for k, v in prices.items():
        print(k, v)
        print()
