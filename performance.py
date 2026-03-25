import yfinance as yf
import pandas as pd

def get_industry(ticker):
    try:
        return yf.Ticker(ticker).info.get("sector", "Unknown")
    except:
        return "Unknown"

def get_returns(tickers):
    periods = ["3mo", "6mo", "1y"]
    spy = yf.Ticker("SPY")

    results = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            row = {"ticker": ticker}

            for period in periods:
                hist = stock.history(period=period)
                spy_hist = spy.history(period=period)

                if len(hist) > 0 and len(spy_hist) > 0:
                    ret = (hist["Close"].iloc[-1] / hist["Close"].iloc[0]) - 1
                    spy_ret = (spy_hist["Close"].iloc[-1] / spy_hist["Close"].iloc[0]) - 1

                    row[period] = ret
                    row[f"{period}_vs_spy"] = ret - spy_ret

            results.append(row)

        except:
            continue

    return pd.DataFrame(results)
