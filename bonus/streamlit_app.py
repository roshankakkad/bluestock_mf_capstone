"""B2 - Streamlit dashboard alternative for Bluestock MF Capstone."""
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

st.set_page_config(page_title="Bluestock MF Dashboard", layout="wide")
st.title("Bluestock Mutual Fund Analytics")

funds = pd.read_csv(PROCESSED / "01_fund_master_clean.csv")
metrics = pd.read_csv(PROCESSED / "fund_scorecard.csv")
transactions = pd.read_csv(PROCESSED / "08_investor_transactions_clean.csv")

st.sidebar.header("Filters")
category = st.sidebar.multiselect("Fund Category", sorted(funds.get("fund_category", pd.Series()).dropna().unique()))
state = st.sidebar.multiselect("State", sorted(transactions.get("state", pd.Series()).dropna().unique()))

st.subheader("Fund Scorecard")
st.dataframe(metrics, use_container_width=True)

st.subheader("Investor Transactions")
if state and "state" in transactions.columns:
    transactions = transactions[transactions["state"].isin(state)]
st.dataframe(transactions.head(200), use_container_width=True)
