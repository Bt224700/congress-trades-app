import pandas as pd
import smtplib
from email.mime.text import MIMEText

def load_committee_map():
    return pd.read_csv("data/committee_map.csv")

def check_conflicts(trades_df):
    committee_df = load_committee_map()

    merged = trades_df.merge(committee_df, on="name", how="left")

    conflicts = merged[
        merged["industry"] == merged["committee_industry"]
    ]

    return conflicts

def send_email_alert(conflicts):
    if conflicts.empty:
        return

    body = conflicts.to_string()

    msg = MIMEText(body)
    msg["Subject"] = "Congressional Trade Conflict Alert"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = "target_email@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("your_email@gmail.com", "your_password")
        server.send_message(msg)
