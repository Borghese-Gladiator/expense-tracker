"""
MANUAL TEST SCRIPT
This script loads actual data from Lunch Money API and calculates statistics using the StatisticService class.
"""
import time
import os

import arrow
import pandas as pd
from dotenv import load_dotenv

from expense_tracker.et_types import StatisticServiceAggregationInterval, StatisticServiceGroup
from expense_tracker.datasources.lunch_money_datasource import LunchMoneyDatasource, LunchMoneyDatasourceSettings
from expense_tracker.et_types.lunch_money_datasource_types import LunchMoneyCategory, LunchMoneyFilterColumn, LunchMoneyGroupColumn, LunchMoneyTag
from expense_tracker.et_types.statistic_service_types import StatisticServiceFilter
from expense_tracker.services import StatisticService


#==================
#  CONSTANTS
#==================
load_dotenv()
LUNCH_MONEY_ACCESS_TOKEN = os.getenv('LUNCH_MONEY_API_KEY')
settings = LunchMoneyDatasourceSettings(access_token=LUNCH_MONEY_ACCESS_TOKEN)

datasource = LunchMoneyDatasource(settings)
service = StatisticService(datasource)

#==================
#  UTILS
#==================
def get_brother_rent_info() -> tuple[
    pd.DataFrame, # Last Month transactions table
    pd.DataFrame, # Last Month top categories
    pd.DataFrame, # Last Month top merchants
    pd.DataFrame, # YTD totals per month
    pd.DataFrame, # YTD groceries vs restaurants per month
    pd.DataFrame, # YTD top categories per month
    pd.DataFrame, # YTD top merchants per month
]:
    # filter_by_set = set([StatisticServiceFilter(filter_criteria=FilterCriteria.INCLUDE, tag_name=Tag.BROTHER_RENT)])
    filter_by_set = set([StatisticServiceFilter(column=LunchMoneyFilterColumn.TAGS, column_value=LunchMoneyTag.BROTHER_RENT)])
    last_month_txn_df, last_month_top_categories_df, last_month_top_merchants_df = get_last_month_info(filter_by_set)
    ytd_totals_per_month_df, ytd_groceries_vs_restaurants_per_month_df, ytd_top_categories_per_month_df, ytd_top_merchants_per_month = get_ytd_info(filter_by_set)
    return last_month_txn_df, last_month_top_categories_df, last_month_top_merchants_df, ytd_totals_per_month_df, ytd_groceries_vs_restaurants_per_month_df, ytd_top_categories_per_month_df, ytd_top_merchants_per_month

def get_total_rent_info() -> tuple[
    pd.DataFrame, # Last Month transactions table
    pd.DataFrame, # Last Month top categories
    pd.DataFrame, # Last Month top merchants
    pd.DataFrame, # YTD totals per month
    pd.DataFrame, # YTD groceries vs restaurants per month
    pd.DataFrame, # YTD top categories per month
    pd.DataFrame, # YTD top merchants per month
]:
    last_month_txn_df, last_month_top_categories_df, last_month_top_merchants_df = get_last_month_info()
    ytd_totals_per_month_df, ytd_groceries_vs_restaurants_per_month_df, ytd_top_categories_per_month_df, ytd_top_merchants_per_month = get_ytd_info()
    return last_month_txn_df, last_month_top_categories_df, last_month_top_merchants_df, ytd_totals_per_month_df, ytd_groceries_vs_restaurants_per_month_df, ytd_top_categories_per_month_df, ytd_top_merchants_per_month

def get_last_month_info(filter_by_set: set[StatisticServiceFilter] | None = None) -> tuple[
    pd.DataFrame, # Last Month transactions table
    pd.DataFrame, # Last Month top categories
    pd.DataFrame, # Last Month top merchants
]:
    # CONSTANTS
    today = arrow.now()
    curr_month_first_day = today.floor('month')
    last_month_first_day = curr_month_first_day.shift(months=-1)
    last_month_last_day = curr_month_first_day.shift(days=-1)
    start_date = last_month_first_day
    end_date = last_month_last_day

    # MAIN
    txn_df = service.get(
        start_date,
        end_date,
        filter_by_set=filter_by_set,
    )
    time.sleep(1)
    top_categories_df = service.calculate(
        start_date,
        end_date,
        group_by_set={StatisticServiceGroup(column=LunchMoneyGroupColumn.CATEGORY)},
        filter_by_set=filter_by_set,
        sort_by_set=None,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )
    top_categories_df = top_categories_df[:5]
    time.sleep(1)
    top_merchants_df = service.calculate(
        start_date,
        end_date,
        group_by_set={StatisticServiceGroup(column=LunchMoneyGroupColumn.MERCHANT)},
        filter_by_set=filter_by_set,
        sort_by_set=None,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )[:5]
    return txn_df, top_categories_df, top_merchants_df

def get_ytd_info(filter_by_set: set[StatisticServiceFilter] | None = None) -> tuple[
    pd.DataFrame, # YTD totals per month
    pd.DataFrame, # YTD groceries vs restaurants per month
    pd.DataFrame, # YTD top categories per month
    pd.DataFrame, # YTD top merchants per month
]:
    # CONSTANTS
    today = arrow.now()
    curr_year_first_day = today.floor('year')
    curr_day_floored = today.floor('day')
    start_date = curr_year_first_day
    end_date = curr_day_floored

    # MAIN
    totals_per_month_df = service.calculate(
        start_date,
        end_date,
        filter_by_set=filter_by_set,
        group_by_set=None,
        sort_by_set=None,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )
    time.sleep(1)
    top_categories_df = service.calculate(
        start_date,
        end_date,
        filter_by_set=filter_by_set,
        group_by_set={StatisticServiceGroup(column=LunchMoneyGroupColumn.CATEGORY)},
        sort_by_set=None,
        interval=StatisticServiceAggregationInterval.YEARLY
    )[:5]
    time.sleep(1)
    grocery_filter = {StatisticServiceFilter(column=LunchMoneyFilterColumn.CATEGORY, column_value=LunchMoneyCategory.GROCERIES)}
    groceries_per_month_df = service.calculate(
        start_date,
        end_date,
        filter_by_set=grocery_filter if filter_by_set is None else grocery_filter | filter_by_set,
        group_by_set={StatisticServiceGroup(column=LunchMoneyGroupColumn.CATEGORY)},
        sort_by_set=None,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )
    restaurant_filter = {StatisticServiceFilter(column=LunchMoneyFilterColumn.CATEGORY, column_value=LunchMoneyCategory.RESTAURANTS)}
    restaurants_per_month_df = service.calculate(
        start_date,
        end_date,
        filter_by_set=restaurant_filter if filter_by_set is None else restaurant_filter | filter_by_set,
        group_by_set={StatisticServiceGroup(column=LunchMoneyGroupColumn.CATEGORY)},
        sort_by_set=None,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )
    groceries_vs_restaurants_per_month_df =  pd.concat([groceries_per_month_df, restaurants_per_month_df], ignore_index=True, sort=False).sort_values(by=['date', 'category'], ignore_index=True)
    time.sleep(1)
    top_merchants_df = service.calculate(
        start_date,
        end_date,
        filter_by_set=filter_by_set,
        group_by_set={StatisticServiceGroup(column=LunchMoneyGroupColumn.MERCHANT)},
        sort_by_set=None,
        interval=StatisticServiceAggregationInterval.YEARLY
    )[:5]
    return totals_per_month_df, groceries_vs_restaurants_per_month_df, top_categories_df, top_merchants_df


#==================
#  MAIN
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

print(last_month_txn_df.head())
print()
print(last_month_top_categories_df.head())
print()
print(last_month_top_merchants_df.head())
print()
print(ytd_totals_per_month_df.head())
print()
print(ytd_groceries_vs_restaurants_per_month_df.head())
print()
print(ytd_top_categories_per_month_df.head())
print()
print(ytd_top_merchants_per_month.head())
print()