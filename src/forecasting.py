import pandas as pd
import streamlit as st
import logging

# Suppress Prophet/cmdstanpy's verbose console logging (also reduces overhead)
logging.getLogger("prophet").setLevel(logging.WARNING)
logging.getLogger("cmdstanpy").setLevel(logging.WARNING)

from prophet import Prophet

@st.cache_data(show_spinner=False)
def forecast_next_months(df: pd.DataFrame, periods: int = 3) -> pd.DataFrame:
    """Forecast future monthly revenue using Prophet. Cached so repeated
    filter changes with the same data don't re-fit the model."""
    monthly = df.groupby(df["order_date"].dt.to_period("M"))["total_amount"].sum().reset_index()
    monthly["order_date"] = monthly["order_date"].dt.to_timestamp()
    monthly.columns = ["ds", "y"]

    model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    model.fit(monthly)

    future = model.make_future_dataframe(periods=periods, freq="MS")
    forecast = model.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]