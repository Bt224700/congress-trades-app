import streamlit as st
import pandas as pd
import plotly.express as px

from utils.fetch_data import fetch_house_trades
from utils.performance import get_returns, get_industry
from utils.alerts import check_conflicts, send_email_alert

st.set_page_config(layout="wide")
st.title("🏛️ Congressional Stock Tracker")

# Load data
df = fetch_house_trades()

# Add industry data
df["industry"] = df["ticker"].apply(lambda x: get_industry(x) if pd.notnull(x) else "Unknown")

# Split parties
dems = df[df["party"] == "Democrat"]
reps = df[df["party"] == "Republican"]

# --- TABLES ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 Democrats")
    st.dataframe(dems.sort_values("date", ascending=False).head(20))

with col2:
    st.subheader("🔴 Republicans")
    st.dataframe(reps.sort_values("date", ascending=False).head(20))

# --- PERFORMANCE ---
st.subheader("📈 Performance vs SPY")

tickers = df["ticker"].dropna().unique().tolist()
perf_df = get_returns(tickers)

if not perf_df.empty:
    plot_df = perf_df.melt(
        id_vars=["ticker"],
        value_vars=["3mo", "6mo", "1y"],
        var_name="period",
        value_name="return"
    )

    fig = px.bar(
        plot_df,
        x="ticker",
        y="return",
        color="period",
        barmode="group",
        hover_data=["ticker"]
    )

    st.plotly_chart(fig, use_container_width=True)

# --- ALERTS ---
st.subheader("🚨 Committee Conflict Alerts")

conflicts = check_conflicts(df)

if not conflicts.empty:
    st.warning("Conflicts detected!")
    st.dataframe(conflicts)
    send_email_alert(conflicts)
else:
    st.success("No conflicts detected.")
