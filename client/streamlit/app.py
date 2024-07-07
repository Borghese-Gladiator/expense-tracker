import arrow
import streamlit as st
import plotly.express as px
import pandas as pd

from client.utils import get_avg_monthly_ytd


#==================
#  CONSTANTS
#==================
this_month_str: str = arrow.now().format("YYYY/MM")
category_groups_df, top_merchant_groups_df = get_avg_monthly_ytd()
print(category_groups_df.head())
print(top_merchant_groups_df.head())
# print(top_location_groups.head())

#==================
#  MAIN
#==================
st.title(f"Streamlit App for Expense Summary for {this_month_str}")

# TRANSACTION table
st.subheader("Transaction List")
st.dataframe(df, use_container_width=True)

# CATEGORY graphs
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

"""
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