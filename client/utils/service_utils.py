"""
How To Do YTD => aggregate on month
category = calculate(timeframe_start, timeframe_end, group_by_set=category, aggregate_by=MONTHLY)
top_five_merchants = calculate(timeframe_start, timeframe_end, group_by_set=merchant, sort_by=amount, aggregate_by=MONTHLY)
aggregate_by=MONTHLY

How To Do YTD (rent applicable) => aggregate on month, filter on rent_applicable StatisticServiceFilter
category = calculate(timeframe_start, timeframe_end, group_by_set=category, filter_by_set=StatisticServiceFilter.BROTHER_RENT, aggregate_by=MONTHLY)
top_five_merchants = calculate(timeframe_start, timeframe_end, group_by_set=merchant, sort_by=amount, filter_by_set=StatisticServiceFilter.BROTHER_RENT, aggregate_by=MONTHLY)
top_five_locations = calculate(timeframe_start, timeframe_end, group_by_set=location, filter_by_set=StatisticServiceFilter.BROTHER_RENT, sort_by=(amount, DESC))

How to Do Last Month
category = calculate(timeframe_start, timeframe_end, group_by_set=category)
top_five_merchants = calculate(timeframe_start, timeframe_end, group_by_set=merchant, sort_by=(amount, DESC))
top_five_locations = calculate(timeframe_start, timeframe_end, group_by_set=location, sort_by=(amount, DESC))

How to Do Last Month (rent applicable)
category = calculate(timeframe_start, timeframe_end, group_by_set=category, filter_by_set=StatisticServiceFilter.BROTHER_RENT,)
top_five_merchants = calculate(timeframe_start, timeframe_end, group_by_set=merchant, sort_by=(amount, DESC), filter_by_set=StatisticServiceFilter.BROTHER_RENT,)
top_five_locations = calculate(timeframe_start, timeframe_end, group_by_set=location,  sort_by=(amount, DESC), filter_by_set=StatisticServiceFilter.BROTHER_RENT,)

How to Do YTD Expenditure
spending = get(timeframe_start, timeframe_end)
rent_applicable_spending = get(timeframe_start, timeframe_end, filter_by_set=StatisticServiceFilter.BROTHER_RENT)
"""
import time
import os

import arrow
import pandas as pd
from dotenv import load_dotenv

from expense_tracker.et_types import StatisticServiceAggregationInterval, StatisticServiceGroup
from expense_tracker.datasources.lunch_money_datasource import LunchMoneyDatasource, LunchMoneyDatasourceSettings
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
    filter_by_set = set([StatisticServiceFilter.BROTHER_RENT])
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
    print(start_date, end_date)
    print(type(start_date), type(end_date))

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
        group_by_set={StatisticServiceGroup.CATEGORY},
        filter_by_set=filter_by_set,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )[:5]
    time.sleep(1)
    top_merchants_df = service.calculate(
        start_date,
        end_date,
        group_by_set={StatisticServiceGroup.MERCHANT},
        filter_by_set=filter_by_set,
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
        group_by_set=None,
        filter_by_set=filter_by_set,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )
    time.sleep(1)
    categories_df = service.calculate(
        start_date,
        end_date,
        group_by_set={StatisticServiceGroup.CATEGORY},
        filter_by_set=filter_by_set,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )
    groceries_vs_restaurants_per_month_df = categories_df # TODO: implement here OR update service to be able to select by other columns besides "tags"
    top_categories_df = categories_df[:5]
    time.sleep(1)
    top_merchants_df = service.calculate(
        start_date,
        end_date,
        group_by_set={StatisticServiceGroup.MERCHANT},
        filter_by_set=filter_by_set,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )[:5]
    return totals_per_month_df, groceries_vs_restaurants_per_month_df, top_categories_df, top_merchants_df

"""
def get_ytd_transactions_and_summary(filter_by_set: set[StatisticServiceFilter] | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    today = arrow.utcnow().date()
    curr_year_first_day = arrow.get(today).floor('year').date()
    curr_day_floored = today.floor('day')
    return get_txn_and_summary(curr_year_first_day, curr_day_floored, filter_by_set)

def get_last_month_transactions_and_summary(filter_by_set: set[StatisticServiceFilter] | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    today = arrow.utcnow().date()
    curr_month_first_day = arrow.get(today).floor('month')
    last_month_first_day = curr_month_first_day.shift(months=-1).date()
    last_month_last_day = curr_month_first_day.shift(days=-1).date()
    return get_txn_and_summary(last_month_first_day, last_month_last_day, filter_by_set)

def get_txn_and_summary(start_date, end_date, filter_by_set: set[StatisticServiceFilter] | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # MAIN
    transactions = service.get(
        start_date,
        end_date,
        filter_by_set=filter_by_set,
    )
    time.sleep(1)
    category_groups = service.calculate(
        start_date,
        end_date,
        group_by_set={StatisticServiceGroup.CATEGORY},
        filter_by_set=filter_by_set,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )
    time.sleep(1)
    top_merchant_groups = service.calculate(
        start_date,
        end_date,
        group_by_set={StatisticServiceGroup.MERCHANT},
        filter_by_set=filter_by_set,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )[:5]
    #$ top_location_groups = service.calculate(
    #$     start_date,
    #$     end_date,
    #$     group_by_set={StatisticServiceGroup.MERCHANT},
    #$     filter_by_set=filter_by_set,
    #$     interval=StatisticServiceAggregationInterval.MONTHLY
    #$ )[:5]
    
    return (
        pd.DataFrame(transactions),
        pd.DataFrame(category_groups),
        pd.DataFrame(top_merchant_groups),
        # pd.DataFrame(top_location_groups),
    )

"""