import yfinance as yf
import pandas as pd

def get_returns(tickers):
    periods = {
        "3mo": "3mo",
        "6mo": "6mo",
        "1y": "1y"
    }

    results = []

    spy = yf.Ticker("SPY")

    for ticker in tickers:
        stock = yf.Ticker(ticker)

        row = {"ticker": ticker}

        for label, period in periods.items():
            hist = stock.history(period=period)
            spy_hist = spy.history(period=period)

            if len(hist) > 0:
                ret = (hist["Close"][-1] / hist["Close"][0]) - 1
                spy_ret = (spy_hist["Close"][-1] / spy_hist["Close"][0]) - 1

                row[label] = ret
                row[f"{label}_vs_spy"] = ret - spy_ret

        results.append(row)

    return pd.DataFrame(results)
