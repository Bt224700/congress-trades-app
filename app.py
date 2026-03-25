import streamlit as st
import pandas as pd
import plotly.express as px

from utils.fetch_data import fetch_house_trades
from utils.performance import get_returns
from utils.alerts import check_conflicts, send_email_alert

st.set_page_config(layout="wide")

st.title("🏛️ Congressional Stock Tracker (NANC vs KRUZ Style)")

# Load data
df = fetch_house_trades()

# Split parties
dems = df[df["party"] == "Democrat"]
reps = df[df["party"] == "Republican"]

# --- SIDE BY SIDE TABLES ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 Democrats")
    st.dataframe(dems.sort_values("date", ascending=False).head(20))

with col2:
    st.subheader("🔴 Republicans")
    st.dataframe(reps.sort_values("date", ascending=False).head(20))

# --- PERFORMANCE SECTION ---
st.subheader("📈 Performance vs SPY")

tickers = df["ticker"].dropna().unique().tolist()

perf_df = get_returns(tickers)

# Melt for plotting
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
    title="Stock Returns"
)

st.plotly_chart(fig, use_container_width=True)

# --- ALERTS ---
st.subheader("🚨 Conflict Alerts")

conflicts = check_conflicts(df)

if not conflicts.empty:
    st.warning("Potential conflicts detected!")
    st.dataframe(conflicts)
    send_email_alert(conflicts)
else:
    st.success("No conflicts detected.")
