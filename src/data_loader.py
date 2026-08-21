import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_sales_data(filepath: str = "data/sample_sales_data.csv") -> pd.DataFrame:
    """Load and clean the sales dataset."""
    df = pd.read_csv(filepath, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()

    if "order_date" not in df.columns:
        raise ValueError(f"'order_date' column not found. Columns found: {list(df.columns)}")

    raw_dates = df["order_date"].astype(str)
    parsed = pd.to_datetime(raw_dates, format="%Y-%m-%d", errors="coerce")
    if parsed.isna().mean() > 0.5:
        parsed = pd.to_datetime(raw_dates, format="%d-%m-%Y", errors="coerce")

    df["order_date"] = parsed
    df = df.dropna(subset=["order_date"])

    if df.empty:
        raise ValueError("No valid rows remain after date parsing — check the CSV's date format.")

    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["year"] = df["order_date"].dt.year
    df = df[df["order_status"] != "Cancelled"].copy()
    return df