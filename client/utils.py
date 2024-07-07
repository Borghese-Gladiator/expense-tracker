"""
How To Do YTD => aggregate on month
category = calculate(timeframe_start, timeframe_end, group_by_set=category, aggregate_by=MONTHLY)
top_five_merchants = calculate(timeframe_start, timeframe_end, group_by_set=merchant, sort_by=amount, aggregate_by=MONTHLY)
aggregate_by=MONTHLY

How To Do YTD (rent applicable) => aggregate on month, filter on rent_applicable tag
category = calculate(timeframe_start, timeframe_end, group_by_set=category, filter_by_set=Tag.BROTHER_RENT, aggregate_by=MONTHLY)
top_five_merchants = calculate(timeframe_start, timeframe_end, group_by_set=merchant, sort_by=amount, filter_by_set=Tag.BROTHER_RENT, aggregate_by=MONTHLY)
top_five_locations = calculate(timeframe_start, timeframe_end, group_by_set=location, filter_by_set=Tag.BROTHER_RENT, sort_by=(amount, DESC))

How to Do Last Month
category = calculate(timeframe_start, timeframe_end, group_by_set=category)
top_five_merchants = calculate(timeframe_start, timeframe_end, group_by_set=merchant, sort_by=(amount, DESC))
top_five_locations = calculate(timeframe_start, timeframe_end, group_by_set=location, sort_by=(amount, DESC))

How to Do Last Month (rent applicable)
category = calculate(timeframe_start, timeframe_end, group_by_set=category, filter_by_set=Tag.BROTHER_RENT,)
top_five_merchants = calculate(timeframe_start, timeframe_end, group_by_set=merchant, sort_by=(amount, DESC), filter_by_set=Tag.BROTHER_RENT,)
top_five_locations = calculate(timeframe_start, timeframe_end, group_by_set=location,  sort_by=(amount, DESC), filter_by_set=Tag.BROTHER_RENT,)

How to Do YTD Expenditure
spending = get(timeframe_start, timeframe_end)
rent_applicable_spending = get(timeframe_start, timeframe_end, filter_by_set=Tag.BROTHER_RENT)
"""
from datetime import datetime
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
def get_avg_monthly_ytd(filter_by_set: set[StatisticServiceFilter] | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # CONSTANTS
    start_date = arrow.get(datetime(datetime.now().year, 1, 1))
    end_date = arrow.now().floor('day')
    
    # MAIN
    transactions = service.get(
        start_date,
        end_date,
        filter_by_set=filter_by_set,
    )
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
    time.sleep(1)
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
