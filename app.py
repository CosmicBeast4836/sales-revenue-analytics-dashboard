import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_sales_data
from src.analytics import (
    total_sales, monthly_sales_trend, top_products, top_sales_rep,
    region_wise_sales, high_value_orders, average_order_value,
    category_wise_sales, rep_performance, region_month_heatmap,
    order_value_distribution, cumulative_revenue
)
from src.forecasting import forecast_next_months

st.set_page_config(page_title="Sales & Revenue Analytics Dashboard", layout="wide")

# ---------------- THEME DEFINITIONS ----------------
DARK_THEME_CSS = """
:root {
  --glow-color: #8b5cf6;
  --glass-bg: rgba(255, 255, 255, 0.05);
  --glass-border: rgba(139, 92, 246, 0.25);
  --glass-shadow: rgba(139, 92, 246, 0.3);
  --accent-1: #8b5cf6;
  --accent-2: #22d3ee;
  --accent-3: #f472b6;
  --input-bg: rgba(255,255,255,0.08);
  --input-text: #e5e7eb;
}
[data-testid="stAppViewContainer"] {
  background: linear-gradient(120deg, #0d0b1f, #171335, #1e1b4b, #0d0b1f);
  background-size: 300% 300%;
  animation: gradientShift 30s ease infinite;
}
[data-testid="stSidebar"] {
  background: linear-gradient(160deg, #14112b, #1e1b4b) !important;
  box-shadow: 4px 0 24px rgba(0,0,0,0.4);
}
[data-testid="stHeader"] {
  background: rgba(13, 11, 31, 0.7) !important;
}
"""

LIGHT_THEME_CSS = """
:root {
  --glow-color: #7c3aed;
  --glass-bg: rgba(255, 255, 255, 0.65);
  --glass-border: rgba(124, 58, 237, 0.18);
  --glass-shadow: rgba(124, 58, 237, 0.20);
  --accent-1: #7c3aed;
  --accent-2: #0891b2;
  --accent-3: #db2777;
  --input-bg: #ffffff;
  --input-text: #1f2937;
}
[data-testid="stAppViewContainer"] {
  background: linear-gradient(120deg, #ede9fe, #e0e7ff, #dbeafe, #f3e8ff);
  background-size: 300% 300%;
  animation: gradientShift 30s ease infinite;
}
[data-testid="stAppViewContainer"] *:not([data-testid="stDateInput"] *) {
  color: #1f2937;
}
[data-testid="stSidebar"] {
  background: linear-gradient(160deg, #ffffff, #f3e8ff) !important;
  box-shadow: 4px 0 24px rgba(124, 58, 237, 0.08);
}
[data-testid="stSidebar"] *:not([data-testid="stDateInput"] *) {
  color: #1f2937 !important;
}
[data-testid="stHeader"] {
  background: rgba(237, 233, 254, 0.7) !important;
}
[data-testid="stMetric"] {
  box-shadow:
    0 8px 24px rgba(124, 58, 237, 0.12),
    inset 0 1px 0 rgba(255,255,255,0.9) !important;
}
[data-testid="stVerticalBlockBorderWrapper"] {
  box-shadow:
    0 8px 24px rgba(124, 58, 237, 0.10),
    inset 0 1px 0 rgba(255,255,255,0.8) !important;
}
"""

def load_css(theme_mode: str, path: str = "assets/style.css"):
    with open(path) as f:
        base_css = f.read()
    theme_css = DARK_THEME_CSS if theme_mode == "dark" else LIGHT_THEME_CSS
    st.markdown(f"<style>{base_css}\n{theme_css}</style>", unsafe_allow_html=True)

def centered_title(text: str):
    st.markdown(f"<h3 style='text-align:center; margin-bottom:0.5rem;'>{text}</h3>", unsafe_allow_html=True)

ACCENT_SEQUENCE = ["#8b5cf6", "#22d3ee", "#f472b6", "#34d399", "#fbbf24", "#60a5fa"]

def apply_theme(fig, theme_mode: str):
    """Make chart background transparent and force readable text/grid colors per theme."""
    text_color = "#1f2937" if theme_mode == "light" else "#e5e7eb"
    grid_color = "rgba(0,0,0,0.12)" if theme_mode == "light" else "rgba(148,163,184,0.15)"

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_color),
        colorway=ACCENT_SEQUENCE,
        margin=dict(l=20, r=20, t=10, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=text_color)),
        coloraxis_colorbar=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color)),
    )
    fig.update_xaxes(
        showgrid=True, gridcolor=grid_color, zeroline=False,
        tickfont=dict(color=text_color), title_font=dict(color=text_color),
    )
    fig.update_yaxes(
        showgrid=True, gridcolor=grid_color, zeroline=False,
        tickfont=dict(color=text_color), title_font=dict(color=text_color),
    )
    return fig

# ---------------- SIDEBAR: LOGO + OUR OWN THEME TOGGLE ----------------
st.sidebar.markdown('<div class="sidebar-logo">⚡ SALESIQ</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-subtitle">REVENUE INTELLIGENCE</div>', unsafe_allow_html=True)

theme_choice = st.sidebar.radio("Appearance", ["🌙 Dark", "☀️ Light"], horizontal=True, label_visibility="collapsed")
theme_mode = "dark" if "Dark" in theme_choice else "light"

load_css(theme_mode)

st.title("📊 Sales & Revenue Analytics Dashboard")

df = load_sales_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.markdown("### 🔍 Filters")

min_date, max_date = df["order_date"].min(), df["order_date"].max()
date_range = st.sidebar.date_input("Order Date Range", value=(min_date, max_date),
                                    min_value=min_date, max_value=max_date)

regions = st.sidebar.multiselect("Region", sorted(df["region"].unique()), default=list(df["region"].unique()))
categories = st.sidebar.multiselect("Product Category", sorted(df["product_category"].unique()),
                                     default=list(df["product_category"].unique()))
reps = st.sidebar.multiselect("Sales Rep", sorted(df["sales_rep"].unique()), default=list(df["sales_rep"].unique()))
statuses = st.sidebar.multiselect("Order Status", sorted(df["order_status"].unique()), default=list(df["order_status"].unique()))

min_val, max_val = int(df["total_amount"].min()), int(df["total_amount"].max())
value_range = st.sidebar.slider("Order Value Range (₹)", min_val, max_val, (min_val, max_val))

# ---------------- APPLY FILTERS ----------------
if len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    df = df[(df["order_date"] >= start_date) & (df["order_date"] <= end_date)]

df = df[
    df["region"].isin(regions) &
    df["product_category"].isin(categories) &
    df["sales_rep"].isin(reps) &
    df["order_status"].isin(statuses) &
    df["total_amount"].between(value_range[0], value_range[1])
]

if df.empty:
    st.warning("No data matches the selected filters. Adjust filters in the sidebar.")
    st.stop()

# ---------------- KPI ROW ----------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹{total_sales(df):,.0f}")
col2.metric("Avg Order Value", f"₹{average_order_value(df):,.0f}")
rep, rep_amt = top_sales_rep(df)
col3.metric("Top Sales Rep", rep or "N/A", f"₹{rep_amt:,.0f}")
col4.metric("Total Orders", len(df))

st.divider()

# ---------------- ROW 1: Trend + Cumulative ----------------
c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        centered_title("Monthly Revenue Trend")
        trend = monthly_sales_trend(df)
        fig = px.line(trend, x="month", y="total_amount", markers=True)
        st.plotly_chart(apply_theme(fig, theme_mode), use_container_width=True)
with c2:
    with st.container(border=True):
        centered_title("Cumulative Revenue Over Time")
        cum = cumulative_revenue(df)
        fig = px.area(cum, x="order_date", y="cumulative_revenue")
        st.plotly_chart(apply_theme(fig, theme_mode), use_container_width=True)

# ---------------- ROW 2: Products + Region ----------------
c3, c4 = st.columns(2)
with c3:
    with st.container(border=True):
        centered_title("Top 5 Products")
        fig = px.bar(top_products(df), x="product_name", y="total_amount")
        st.plotly_chart(apply_theme(fig, theme_mode), use_container_width=True)
with c4:
    with st.container(border=True):
        centered_title("Region-wise Sales")
        fig = px.pie(region_wise_sales(df), names="region", values="total_amount", hole=0.4)
        st.plotly_chart(apply_theme(fig, theme_mode), use_container_width=True)

# ---------------- ROW 3: Category + Rep performance ----------------
c5, c6 = st.columns(2)
with c5:
    with st.container(border=True):
        centered_title("Category-wise Revenue")
        fig = px.bar(category_wise_sales(df), x="product_category", y="total_amount", color="product_category")
        st.plotly_chart(apply_theme(fig, theme_mode), use_container_width=True)
with c6:
    with st.container(border=True):
        centered_title("Sales Rep Performance")
        fig = px.bar(rep_performance(df), x="total_amount", y="sales_rep", orientation="h")
        st.plotly_chart(apply_theme(fig, theme_mode), use_container_width=True)

# ---------------- ROW 4: Heatmap + Distribution ----------------
c7, c8 = st.columns(2)
with c7:
    with st.container(border=True):
        centered_title("Region vs Month Revenue Heatmap")
        heat = region_month_heatmap(df)
        fig = px.imshow(heat, aspect="auto", color_continuous_scale="Purples")
        st.plotly_chart(apply_theme(fig, theme_mode), use_container_width=True)
with c8:
    with st.container(border=True):
        centered_title("Order Value Distribution by Category")
        fig = px.box(order_value_distribution(df), x="product_category", y="total_amount")
        st.plotly_chart(apply_theme(fig, theme_mode), use_container_width=True)

# ---------------- Forecast ----------------
with st.container(border=True):
    centered_title("Revenue Forecast (Next 3 Months)")
    with st.spinner("Training forecast model..."):
        forecast = forecast_next_months(df)
    fig = px.line(forecast, x="ds", y="yhat")
    st.plotly_chart(apply_theme(fig, theme_mode), use_container_width=True)
# ---------------- Table ----------------
with st.container(border=True):
    centered_title("High-Value Orders (Filtered)")
    st.dataframe(high_value_orders(df), use_container_width=True)