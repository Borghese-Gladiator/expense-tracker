import arrow
import streamlit as st
import plotly.express as px

from utils.service_utils import get_brother_rent_info, get_total_rent_info

#==================
#  CONSTANTS
#==================
RENT_REQUIRED = -1500  # expenses are negative 
(
    last_month_txn_df,
    last_month_top_categories_df,
    last_month_top_merchants_df,
    ytd_totals_per_month_df,
    ytd_groceries_vs_restaurants_per_month_df,
    ytd_top_categories_per_month_df,
    ytd_top_merchants_per_month,
    ytd_average_monthly_rent,
) = get_brother_rent_info()

# (
#     total_last_month_txn_df,
#     total_last_month_top_categories_df,
#     total_last_month_top_merchants_df,
#     total_ytd_totals_per_month_df,
#     total_ytd_groceries_vs_restaurants_per_month_df,
#     total_ytd_top_categories_per_month_df,
#     total_ytd_top_merchants_per_month,
#     average_monthly_rent,
# ) = get_total_rent_info()

success_btn_html = """
<div style="margin: 20px;">
    <a href="#" style="
        background-color: #28a745;
        border: none;
        color: white;
        padding: 10px 24px;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
    ">
        <i class="fa fa-check"></i> Rent Met!
    </a>
</div>
"""
x_btn_html = """
<div style="margin: 20px;">
    <a href="#" style="
        background-color: #dc3545;
        border: none;
        color: white;
        padding: 10px 24px;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
    ">
        <i class="fa fa-times"></i> Rent not met! :(
    </a>
</div>
"""

#==================
#  UTILS
#==================
# Load Font Awesome icons
st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">', unsafe_allow_html=True)

# Create Plotly charts
chart_last_month_top_categories_df = px.bar(last_month_top_categories_df, x='category', y='amount')
chart_last_month_top_merchants_df = px.bar(last_month_top_merchants_df, x='merchant', y='amount')
chart_ytd_totals_per_month_df = px.bar(ytd_totals_per_month_df, x='date', y='amount')
chart_ytd_groceries_vs_restaurants_per_month_df = px.bar(ytd_groceries_vs_restaurants_per_month_df, x='date', y=['amount_groceries', 'amount_restaurants'], barmode='group')
chart_ytd_top_categories_per_month_df = px.bar(ytd_top_categories_per_month_df, x='date', y='amount')
chart_ytd_top_merchants_per_month = px.bar(ytd_top_merchants_per_month, x='date', y='amount')

# Update the layout to remove x-axis and y-axis labels
chart_last_month_top_categories_df.update_layout(xaxis_title=None, yaxis_title=None)
chart_last_month_top_merchants_df.update_layout(xaxis_title=None, yaxis_title=None)
chart_ytd_totals_per_month_df.update_layout(xaxis_title=None, yaxis_title=None)
chart_ytd_groceries_vs_restaurants_per_month_df.update_layout(xaxis_title=None, yaxis_title=None)
chart_ytd_top_categories_per_month_df.update_layout(xaxis_title=None, yaxis_title=None)
chart_ytd_top_merchants_per_month.update_layout(xaxis_title=None, yaxis_title=None)


#==================
#  MAIN
#==================
st.title("(Brother Rent) Timmy Expense Tracker")
st.caption("powered by Lunch Money (powered by Plaid)")

# **BROTHER Rent Applicable**
# LAST MONTH
st.header(f"LAST MONTH ({arrow.now().shift(months=-1).format('MMMM')})")
st.markdown(f"Total Rent: ${last_month_txn_df['amount'].sum():,.2f}")
if last_month_txn_df['amount'].sum() <= RENT_REQUIRED:
    st.markdown(success_btn_html, unsafe_allow_html=True)
else:
    st.markdown(x_btn_html, unsafe_allow_html=True)

# Transaction Table
st.subheader("Transaction List")
st.dataframe(last_month_txn_df)

# Graphs
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top Categories")
    st.plotly_chart(chart_last_month_top_categories_df, use_container_width=True)
with col2:
    st.subheader("Top Merchants")
    st.plotly_chart(chart_last_month_top_merchants_df, use_container_width=True)

# YTD AVERAGES per MONTH
st.header("Year to Date Averages")
st.markdown(f"Average Rent: ${ytd_average_monthly_rent:,.2f}")
if ytd_average_monthly_rent <= RENT_REQUIRED:
    st.markdown(success_btn_html, unsafe_allow_html=True)
else:
    st.markdown(x_btn_html, unsafe_allow_html=True)

# Graphs
col3, col4 = st.columns(2)
with col3:
    st.subheader("Totals per Month")
    st.plotly_chart(chart_ytd_totals_per_month_df, use_container_width=True)
with col4:
    st.subheader("Groceries vs Restaurants per Month")
    st.plotly_chart(chart_ytd_groceries_vs_restaurants_per_month_df, use_container_width=True)

col5, col6 = st.columns(2)
with col5:
    st.subheader("Top Categories")
    st.plotly_chart(chart_ytd_top_categories_per_month_df, use_container_width=True)
with col6:
    st.subheader("Top Merchants")
    st.plotly_chart(chart_ytd_top_merchants_per_month, use_container_width=True)
