import arrow
import dash
from dash import (
    dcc,
    html,
    Dash,
    dash_table,
    Input, Output, no_update, callback
)
import dash_bootstrap_components as dbc
import plotly.express as px

from utils.constants import RENT_REQUIRED
from utils.service_utils import get_brother_rent_info, get_total_rent_info

#==================
#  CONSTANTS
#==================
last_month_name = arrow.now().shift(months=-1).format("MMMM")
curr_year_name = arrow.now().format("YYYY")

(
    df_last_month_txn,
    df_last_month_top_categories,
    df_last_month_top_merchants,
    df_ytd_totals_per_month,
    df_ytd_groceries_vs_restaurants_per_month,
    df_ytd_top_categories_per_month,
    df_ytd_top_merchants_per_month,
) = get_brother_rent_info()

# (
#     df_total_last_month_txn,
#     df_total_last_month_top_categories,
#     df_total_last_month_top_merchants,
#     df_total_ytd_totals_per_month,
#     df_total_ytd_groceries_vs_restaurants_per_month,
#     df_total_ytd_top_categories_per_month,
#     total_ytd_top_merchants_per_month,
# ) = get_total_rent_info()


success_btn_style = {
    'background-color': '#28a745',
    'border': 'none',
    'color': 'white',
    'padding': '10px 24px',
    'text-decoration': 'none',
    'display': 'inline-block',
    'font-size': '16px',
    'margin': '4px 2px',
    'cursor': 'pointer',
    'border-radius': '4px',
}
x_btn_style = {
    'background-color': '#dc3545',
    'border': 'none',
    'color': 'white',
    'padding': '10px 24px',
    'text-decoration': 'none',
    'display': 'inline-block',
    'font-size': '16px',
    'margin': '4px 2px',
    'cursor': 'pointer',
    'border-radius': '4px',
}

#==================
#  UTILS
#==================
last_month_rent_sum = df_last_month_txn['amount'].sum()
if last_month_rent_sum <= RENT_REQUIRED:
    last_month_rent_met_component = html.A(
        children=[html.I(className="fa fa-check"), " Rent Met!"],
        href="#",
        style=success_btn_style,
    )
else:
    last_month_rent_met_component = html.A(
        children=[html.I(className="fa fa-times"), " Rent not met! :("],
        href="#",
        style=x_btn_style,
    )

ytd_rent_avg = df_ytd_totals_per_month['amount'].mean()
if ytd_rent_avg <= RENT_REQUIRED:
    ytd_rent_met_component = html.A(
        children=[html.I(className="fa fa-check"), " Rent Met!"],
        href="#",
        style=success_btn_style,
    )
else:
    ytd_rent_met_component = html.A(
        children=[html.I(className="fa fa-times"), " Rent not met! :("],
        href="#",
        style=x_btn_style,
    )

# create Actual vs Expected for YTD Totals per Month
df_ytd_totals_per_month.rename(columns={'amount': 'actual'}, inplace=True)
df_ytd_totals_per_month['expected'] = RENT_REQUIRED

# drop Set column since Dash Data Table doesn't support it
df_last_month_txn = df_last_month_txn.drop('tags', axis=1)

# Create Plotly charts
chart_last_month_top_categories = px.bar(df_last_month_top_categories, title=f"{last_month_name} Top Categories", x='category', y='amount')
chart_last_month_top_merchants = px.bar(df_last_month_top_merchants, title=f"{last_month_name} Top Merchants", x='merchant', y='amount')
chart_ytd_totals_per_month = px.bar(df_ytd_totals_per_month, title=f"{curr_year_name} Totals per Month", x='date', y=['expected', 'actual'], barmode='group')
chart_ytd_groceries_vs_restaurants_per_month = px.bar(df_ytd_groceries_vs_restaurants_per_month, title=f"{curr_year_name} Groceries/Restaurants per Month", x='date', y=['amount_groceries', 'amount_restaurants'], barmode='group')
chart_ytd_top_categories_per_month = px.bar(df_ytd_top_categories_per_month, title=f"{curr_year_name} Top Categories", x='category', y='amount')
chart_ytd_top_merchants_per_month = px.bar(df_ytd_top_merchants_per_month, title=f"{curr_year_name} Top Merchants", x='merchant', y='amount')

# Update the layout to remove x-axis and y-axis labels
chart_last_month_top_categories.update_layout(xaxis_title=None, yaxis_title=None)
chart_last_month_top_merchants.update_layout(xaxis_title=None, yaxis_title=None)
chart_ytd_totals_per_month.update_layout(xaxis_title=None, yaxis_title=None)
chart_ytd_groceries_vs_restaurants_per_month.update_layout(xaxis_title=None, yaxis_title=None)
chart_ytd_top_categories_per_month.update_layout(xaxis_title=None, yaxis_title=None)
chart_ytd_top_merchants_per_month.update_layout(xaxis_title=None, yaxis_title=None)

#==================
#  MAIN
#==================
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
)
app.layout = html.Div(children=[
    html.H1(
        children='Jon and Timmy Expense Tracker',
        style={
            'textAlign': 'center',
        }
    ),
    
    html.H3(id='last-month-header', children=f"{last_month_name.upper()} Expenses"),
    html.P(id='last-month-rent-met-text', children=f"TOTAL: ${last_month_rent_sum:,.2f}"),
    last_month_rent_met_component,
    dash_table.DataTable(
        df_last_month_txn.to_dict('records'),
        [{"name": i, "id": i} for i in df_last_month_txn.columns],
    ),
    dcc.Graph(
        id='last-month-top-categories',
        figure=chart_last_month_top_categories
    ),
    dcc.Graph(
        id='last-month-top-merchants',
        figure=chart_last_month_top_merchants
    ),

    html.H3(id='ytd-header', children=f"{curr_year_name} Expenses"),
    ytd_rent_met_component,
    html.P(id='ytd-rent-met-text', children=f"${ytd_rent_avg:,.2f}"),
    dcc.Graph(
        id='ytd-totals-per-month',
        figure=chart_ytd_totals_per_month
    ),
    dcc.Graph(
        id='ytd-groceries-vs-restaurants-per-month',
        figure=chart_ytd_groceries_vs_restaurants_per_month
    ),
    dcc.Graph(
        id='ytd-top-categories-per-month',
        figure=chart_ytd_top_categories_per_month
    ),
    dcc.Graph(
        id='ytd-top-merchants-per-month',
        figure=chart_ytd_top_merchants_per_month
    ),
], style={
    'marginLeft': '30px',
    'marginRight': '30px',
})

"""
# TODO: run in prod
app = dash.Dash(__name__)
application = app.server
application.run(host='0.0.0.0', port='8080')
"""

if __name__ == '__main__':
    app.run_server(debug=True)