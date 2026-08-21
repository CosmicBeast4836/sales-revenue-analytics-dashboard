import pandas as pd

def total_sales(df: pd.DataFrame) -> float:
    return round(df["total_amount"].sum(), 2)

def monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("month")["total_amount"].sum().reset_index()

def top_products(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    return (df.groupby("product_name")["total_amount"]
              .sum().sort_values(ascending=False).head(n).reset_index())

def top_sales_rep(df: pd.DataFrame) -> pd.Series:
    return df.groupby("sales_rep")["total_amount"].sum().idxmax(), \
           df.groupby("sales_rep")["total_amount"].sum().max()

def region_wise_sales(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("region")["total_amount"].sum().reset_index().sort_values("total_amount", ascending=False)

def high_value_orders(df: pd.DataFrame, threshold: float = 10000) -> pd.DataFrame:
    return df[df["total_amount"] > threshold].sort_values("total_amount", ascending=False)

def order_status_breakdown(df: pd.DataFrame) -> pd.Series:
    return df["order_status"].value_counts()

def average_order_value(df: pd.DataFrame) -> float:
    return round(df["total_amount"].mean(), 2)

def category_wise_sales(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("product_category")["total_amount"]
              .sum().reset_index().sort_values("total_amount", ascending=False))

def rep_performance(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("sales_rep")["total_amount"]
              .sum().reset_index().sort_values("total_amount", ascending=True))

def region_month_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    pivot = df.pivot_table(index="region", columns="month", values="total_amount", aggfunc="sum", fill_value=0)
    return pivot

def order_value_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return df[["product_category", "total_amount"]]

def cumulative_revenue(df: pd.DataFrame) -> pd.DataFrame:
    daily = df.groupby("order_date")["total_amount"].sum().sort_index().cumsum().reset_index()
    daily.columns = ["order_date", "cumulative_revenue"]
    return daily