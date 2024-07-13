"""
import sys
import os

# Print the current Python path
print("Current PYTHONPATH:")
for path in sys.path:
    print(path)

# Check if 'client' directory is in the Python path
client_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(f"\nExpected client path: {client_path}")
if client_path in sys.path:
    print("Client directory is in PYTHONPATH")
else:
    print("Client directory is NOT in PYTHONPATH. Adding it.")
    sys.path.insert(0, client_path)

# Try to import the client module and catch any exceptions
try:
    from client.utils import get_brother_rent_info, get_total_rent_info
    print("Imported client.utils successfully")
except ModuleNotFoundError as e:
    print(f"Error importing client.utils: {e}")
"""
# ========


import streamlit as st
import plotly.express as px

from utils.service_utils import get_brother_rent_info, get_total_rent_info

#==================
#  CONSTANTS
#==================
(
    last_month_txn_df,
    last_month_top_categories_df,
    last_month_top_merchants_df,
    ytd_totals_per_month_df,
    ytd_groceries_vs_restaurants_per_month_df,
    ytd_top_categories_per_month_df,
    ytd_top_merchants_per_month,
) = get_brother_rent_info()

# (
#     total_last_month_txn_df,
#     total_last_month_top_categories_df,
#     total_last_month_top_merchants_df,
#     total_ytd_totals_per_month_df,
#     total_ytd_groceries_vs_restaurants_per_month_df,
#     total_ytd_top_categories_per_month_df,
#     total_ytd_top_merchants_per_month,
# ) = get_total_rent_info()

#==================
#  MAIN
#==================
st.title("Timmy Expense Tracker")
st.caption("powered by Lunch Money (powered by Plaid)")

# **BROTHER Rent Applicable**
# LAST MONTH
st.subheader("LAST MONTH")

# Transaction Table
st.subheader("Transaction List")
st.dataframe(last_month_txn_df)

col1, col2 = st.columns(2)
with col1:
    # Top Categories
    st.plotly_chart(px.bar(last_month_top_categories_df, x='Category', y='Amount', title="Top Categories"), use_container_width=True)
with col2:
    # Top Merchants
    st.plotly_chart(px.bar(last_month_top_merchants_df, x='Merchant', y='Amount', title="Top Merchants"), use_container_width=True)

# YTD AVERAGES per MONTH
st.subheader("Year to Date Averages")

col3, col4 = st.columns(2)
with col3:
    # Totals per Month
    st.plotly_chart(px.bar(ytd_totals_per_month_df, x='Date', y='Amount', title="Totals per Month"), use_container_width=True)
with col4:
    # Groceries vs Restaurants per Month
    st.plotly_chart(px.bar(ytd_groceries_vs_restaurants_per_month_df, x='Date', y=['Amount_Groceries', 'Amount_Restaurants'], title="Groceries vs Restaurants per Month"), use_container_width=True)

col5, col6 = st.columns(2)
with col5:
    # Top Categories
    st.plotly_chart(px.bar(ytd_top_categories_per_month_df, x='Date', y='Amount', title="Top Categories per Month"), use_container_width=True)
with col6:
    # Top Merchants
    st.plotly_chart(px.bar(ytd_top_merchants_per_month, x='Date', y='Amount', title="Top Merchants per Month"), use_container_width=True)


"""
st.subheader("Rent Applicable - Transaction List")
st.dataframe(df, use_container_width=True)

# Category Graphs
st.subheader("Rent Applicable - Category Summary")
st.plotly_chart(
    px.bar(
        data_frame = category_groups_df,
        x = "date",
        y = ["category", "amount"],
        orientation = "v",
        barmode = 'group',
        title = 'YTD Monthly Average (all) - Category'
    )
)
st.plotly_chart(
    px.bar(
        data_frame = top_merchant_groups_df,
        x = "date",
        y = ["merchant", "amount"],
        orientation = "v",
        barmode = 'group',
        title = 'YTD Monthly Average (all) - Category'
    )
)

# YEAR TO DATE Rent Applicable
# Transaction Table
st.subheader("Transaction List")
st.dataframe(df, use_container_width=True)

# Category Graphs
st.subheader("Category Summary")
st.plotly_chart(
    px.bar(
        data_frame = category_groups_df,
        x = "date",
        y = ["category", "amount"],
        orientation = "v",
        barmode = 'group',
        title = 'YTD Monthly Average (all) - Category'
    )
)
st.plotly_chart(
    px.bar(
        data_frame = top_merchant_groups_df,
        x = "date",
        y = ["merchant", "amount"],
        orientation = "v",
        barmode = 'group',
        title = 'YTD Monthly Average (all) - Category'
    )
)
# -------------------------------------------

ytd_monthly_panel_all_panel
ytd_monthly_panel_rent_applicable_panel
last_month_all_panel
last_month_rent_applicable_panel

YTD Monthly Average (all)
- category - bar graph 
- top merchants - bar graph 
- top locations 

YTD Monthly Average (rent applicable)
- category 
- top merchants
- top locations

Last Month (May)
- category 
- top merchants
- top locations

Last Month (May + Rent Applicable)
- category 
- top merchants
- top locations

YTD Expenditure => requires all transactions (sorted) and continuously increase
- YTD Spending - line graph of each transaction 
- YTD Spending (rent applicable) - line graph

"""
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample DataFrame
# Replace this with your actual data loading code
data = {
    'date': pd.date_range(start='2023-01-01', periods=150, freq='D'),
    'category': np.random.choice(['Food', 'Transport', 'Rent', 'Utilities'], size=150),
    'merchant': np.random.choice(['Merchant A', 'Merchant B', 'Merchant C'], size=150),
    'location': np.random.choice(['Location 1', 'Location 2', 'Location 3'], size=150),
    'amount': np.random.uniform(10, 100, size=150),
    'rent_applicable': np.random.choice([True, False], size=150)
}
df = pd.DataFrame(data)

# Filter for rent applicable transactions
rent_df = df[df['rent_applicable']]

# YTD Monthly Average (all)
st.header('YTD Monthly Average (all)')
monthly_avg = df.groupby(df['date'].dt.to_period('M')).mean()
st.bar_chart(monthly_avg['amount'])

# Category Bar Graph
st.subheader('Category - Bar Graph')
category_avg = df.groupby('category')['amount'].mean()
st.bar_chart(category_avg)

# Top Merchants Bar Graph
st.subheader('Top Merchants - Bar Graph')
merchant_avg = df.groupby('merchant')['amount'].mean().nlargest(10)
st.bar_chart(merchant_avg)

# Top Locations Bar Graph
st.subheader('Top Locations - Bar Graph')
location_avg = df.groupby('location')['amount'].mean().nlargest(10)
st.bar_chart(location_avg)

# YTD Monthly Average (rent applicable)
st.header('YTD Monthly Average (rent applicable)')
monthly_avg_rent = rent_df.groupby(rent_df['date'].dt.to_period('M')).mean()
st.bar_chart(monthly_avg_rent['amount'])

# Category Bar Graph
st.subheader('Category - Bar Graph (Rent Applicable)')
category_avg_rent = rent_df.groupby('category')['amount'].mean()
st.bar_chart(category_avg_rent)

# Top Merchants Bar Graph
st.subheader('Top Merchants - Bar Graph (Rent Applicable)')
merchant_avg_rent = rent_df.groupby('merchant')['amount'].mean().nlargest(10)
st.bar_chart(merchant_avg_rent)

# Top Locations Bar Graph
st.subheader('Top Locations - Bar Graph (Rent Applicable)')
location_avg_rent = rent_df.groupby('location')['amount'].mean().nlargest(10)
st.bar_chart(location_avg_rent)

# Last Month (May)
may_df = df[df['date'].dt.month == 5]

# Category Bar Graph
st.header('Last Month (May)')
st.subheader('Category - Bar Graph')
category_may = may_df.groupby('category')['amount'].mean()
st.bar_chart(category_may)

# Top Merchants Bar Graph
st.subheader('Top Merchants - Bar Graph')
merchant_may = may_df.groupby('merchant')['amount'].mean().nlargest(10)
st.bar_chart(merchant_may)

# Top Locations Bar Graph
st.subheader('Top Locations - Bar Graph')
location_may = may_df.groupby('location')['amount'].mean().nlargest(10)
st.bar_chart(location_may)

# Last Month (May + Rent Applicable)
may_rent_df = may_df

"""