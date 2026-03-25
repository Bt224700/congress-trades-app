import requests
import pandas as pd

def fetch_house_trades():
    url = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"
    data = requests.get(url).json()

    df = pd.DataFrame(data)

    df = df.rename(columns={
        "representative": "name",
        "transaction_date": "date",
        "ticker": "ticker",
        "type": "transaction_type",
        "amount": "amount"
    })

    # Basic party tagging (improve later)
    democrat_names = [
        "Nancy Pelosi", "Chuck Schumer", "Alexandria Ocasio-Cortez",
        "Ro Khanna", "Adam Schiff", "Mark Warner"
    ]

    df["party"] = df["name"].apply(
        lambda x: "Democrat" if x in democrat_names else "Republican"
    )

    return df
