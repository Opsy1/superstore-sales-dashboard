# Superstore Sales Dashboard

A Streamlit dashboard for exploring Superstore sales performance from 2011 to 2014. The app uses the provided superstore.csv dataset to show sales, profit, customer, product, and regional performance through interactive charts and filters.

## Project Overview

This project analyzes retail sales data and presents the results in a dark-themed Streamlit dashboard. Users can filter the dashboard by year and region, download the dataset as a CSV, and switch between several dashboard views.

## Features

- Sales overview with total sales, profit, average sales, quantity sold, and profit margin KPIs
- Sales charts by region, category, sub-category, product, and month
- Year-over-year sales forecast based on recent annual growth
- Profit analysis by region, year, city, and profit margin
- Customer and geographical analysis by segment, state, and top customers
- Business insights section with recommended focus areas
- Sidebar filters for year and region
- CSV download button for the sales dataset


## Project Structure

```text
sales_dashboard_project/
|-- dashboard/
|   `-- app.py
|-- data/
|   `-- superstore.csv
|-- notebooks.ipynb
|-- README.md
|-- requirements.txt
```


## Tools and Libraries

- Python
- Streamlit
- Pandas
- Plotly Express


## Setup Instructions

1. Clone or download this project.

2. Open a terminal in the project root:

   ```powershell
   cd sales_dashboard_project
   ```

3. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

4. Install the required packages:

   ```powershell
   pip install streamlit pandas plotly
   ```

5. Run the dashboard from the project root:

   ```powershell
   streamlit run dashboard\app.py
   ```

6. Open the local Streamlit URL shown in the terminal, usually:

   ```text
   http://localhost:8501
   ```


## Dashboard Pages

### Sales Analysis

Shows core business KPIs and visualizations for sales by region, category, sub-category, product, and month. It also includes a year-over-year forecast.

### Profit Analysis

Shows total profit, profit margin by region, yearly profit trends, and the top cities by profit.

### Customer & Geographical Analysis

Shows customer segment performance, sales by state, segment profitability, and top customers by sales.

### Business Insights

Summarizes key observations from the dashboard and suggests areas of focus for sales growth, profitability, product strategy, and customer retention.


