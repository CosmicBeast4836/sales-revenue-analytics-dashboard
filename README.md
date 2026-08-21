# 📊 Sales & Revenue Analytics Dashboard

An interactive, glassmorphic sales analytics dashboard built with Streamlit — featuring live filtering, 9+ chart types, and ML-powered revenue forecasting using Prophet.

🔗Live Demo: (https://sales-revenue-analytics-dashboard-by726qlero7jlekea5soys.streamlit.app/)

[Dashboard Preview]
<img width="1917" height="907" alt="Preview_1" src="https://github.com/user-attachments/assets/23cf4e7f-bf8d-42b8-afab-a67b27a539c1" />
<img width="1913" height="910" alt="Preview_2" src="https://github.com/user-attachments/assets/bebfd822-10eb-4841-8fee-cc7870d4c26a" />
<img width="1917" height="901" alt="Preview_3" src="https://github.com/user-attachments/assets/6269bfac-4083-4783-81bc-528338ab2b42" />


## Overview

This project analyzes 2,500+ simulated retail orders across Indian regions, product categories, and sales reps to surface actionable business insights — total revenue, top performers, regional trends, seasonal patterns, and a 3-month revenue forecast.

Built as part of a Data Analytics / Data Science & AI-ML certification portfolio (IT Vedant), this project demonstrates end-to-end skills: data generation, cleaning, EDA, interactive visualization, time-series forecasting, and dashboard deployment.

## Features

- **9 interactive chart types**: line, area, bar, horizontal bar, donut, heatmap, box plot, and forecast trend
- **5 live filters**: date range, region, product category, sales rep, order status, plus a value-range slider — all cascading into every chart and KPI card
- **ML-powered forecasting**: 3-month revenue forecast using Facebook Prophet
- **Custom glassmorphism UI**: animated gradient background, blurred glass panels, glowing sidebar branding
- **Full dark/light theme support** with independently tuned color palettes for each
- **Cached data pipeline** for fast reruns on filter changes

## Tech Stack

| Category      | Tools                      |
|---------------|----------------------------|
| Language      | Python 3.11                |
| Data          | pandas, NumPy              |
| Visualization | Plotly Express             |
| Forecasting   | Prophet                    |
| Web App       | Streamlit                  |
| Styling       | Custom CSS (glassmorphism) |

## Project Structure

sales-revenue-analytics-dashboard/
├── assets/
│ └── style.css
├── data/
│ └── sample_sales_data.csv
├── notebook/
│ └── 01_eda.ipynb
├── src/
│ ├── data_loader.py
│ ├── analytics.py
│ └── forecasting.py
├── screenshots/
├── app.py
├── requirements.txt
└── README.md


## Key Insights (from EDA)

- Festive season (Oct–Dec) shows a **~40% revenue uplift** over baseline months
- Electronics is the highest-revenue category despite lower order volume than Groceries
- Top-performing sales rep drives disproportionately higher average order value

## Run Locally

```bash
git clone https://github.com/<your-username>/sales-revenue-analytics-dashboard.git
cd sales-revenue-analytics-dashboard
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
streamlit run app.py
```

## What I Learned

- Building cached, multi-filter interactive dashboards with Streamlit
- Time-series forecasting with Prophet, including handling seasonality
- Debugging cross-theme CSS specificity conflicts in a component-based framework
- Designing a cohesive custom UI system (glassmorphism) on top of a data tool, not just a static site
