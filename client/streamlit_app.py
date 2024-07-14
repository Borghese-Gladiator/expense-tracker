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

import arrow
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

print(last_month_txn_df)
print()
print(last_month_top_categories_df)
print()
print(last_month_top_merchants_df)
print()
print(ytd_totals_per_month_df)
print()
print(ytd_groceries_vs_restaurants_per_month_df)
print()
print(ytd_top_categories_per_month_df)
print()
print(ytd_top_merchants_per_month)
print()

#==================
#  MAIN
#==================
st.title("Timmy Expense Tracker")
st.caption("powered by Lunch Money (powered by Plaid)")

# **BROTHER Rent Applicable**
# LAST MONTH
st.header(f"LAST MONTH ({arrow.now().shift(months=-1).format('MMMM')})")

# Transaction Table
st.subheader("Transaction List")
st.dataframe(last_month_txn_df)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Top Categories")
    st.plotly_chart(px.bar(last_month_top_categories_df, x='category', y='amount', title="Top Categories"), use_container_width=True)
with col2:
    st.subheader("Top Merchants")
    st.plotly_chart(px.bar(last_month_top_merchants_df, x='merchant', y='amount', title="Top Merchants"), use_container_width=True)

# YTD AVERAGES per MONTH
st.header("Year to Date Averages")

col3, col4 = st.columns(2)
with col3:
    st.subheader("Totals per Month")
    st.plotly_chart(px.bar(ytd_totals_per_month_df, x='date', y='amount', title="Totals per Month"), use_container_width=True)
with col4:
    st.subheader("Groceries vs Restaurants per Month")
    # st.plotly_chart(px.bar(ytd_groceries_vs_restaurants_per_month_df, x='date', y=['Amount_Groceries', 'Amount_Restaurants'], title="Groceries vs Restaurants per Month"), use_container_width=True)

col5, col6 = st.columns(2)
with col5:
    st.subheader("Top Categories")
    st.plotly_chart(px.bar(ytd_top_categories_per_month_df, x='date', y='amount', title="Top Categories per Month"), use_container_width=True)
with col6:
    st.subheader("Top Merchants")
    st.plotly_chart(px.bar(ytd_top_merchants_per_month, x='date', y='amount', title="Top Merchants per Month"), use_container_width=True)
