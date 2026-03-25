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

    # Party tagging (basic — improve later)
    democrat_keywords = ["Pelosi", "Schumer", "AOC"]
    df["party"] = df["name"].apply(
        lambda x: "Democrat" if any(k in x for k in democrat_keywords) else "Republican"
    )

    return df
