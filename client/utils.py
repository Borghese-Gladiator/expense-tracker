"""
How To Do YTD => aggregate on month
category = calculate(timeframe_start, timeframe_end, group_by=category, aggregate_by=MONTHLY)
top_five_merchants = calculate(timeframe_start, timeframe_end, group_by=merchant, sort_by=amount, aggregate_by=MONTHLY)
aggregate_by=MONTHLY

How To Do YTD (rent applicable) => aggregate on month, filter on rent_applicable tag
category = calculate(timeframe_start, timeframe_end, group_by=category, filter_by=Tag.RENT_APPLICABLE, aggregate_by=MONTHLY)
top_five_merchants = calculate(timeframe_start, timeframe_end, group_by=merchant, sort_by=amount, filter_by=Tag.RENT_APPLICABLE, aggregate_by=MONTHLY)
top_five_locations = calculate(timeframe_start, timeframe_end, group_by=location, filter_by=Tag.RENT_APPLICABLE, sort_by=(amount, DESC))

How to Do Last Month
category = calculate(timeframe_start, timeframe_end, group_by=category)
top_five_merchants = calculate(timeframe_start, timeframe_end, group_by=merchant, sort_by=(amount, DESC))
top_five_locations = calculate(timeframe_start, timeframe_end, group_by=location, sort_by=(amount, DESC))

How to Do Last Month (rent applicable)
category = calculate(timeframe_start, timeframe_end, group_by=category, filter_by=Tag.RENT_APPLICABLE,)
top_five_merchants = calculate(timeframe_start, timeframe_end, group_by=merchant, sort_by=(amount, DESC), filter_by=Tag.RENT_APPLICABLE,)
top_five_locations = calculate(timeframe_start, timeframe_end, group_by=location,  sort_by=(amount, DESC), filter_by=Tag.RENT_APPLICABLE,)

How to Do YTD Expenditure
spending = get(timeframe_start, timeframe_end)
rent_applicable_spending = get(timeframe_start, timeframe_end, filter_by=Tag.RENT_APPLICABLE)
"""
from datetime import datetime
from typing import Any

import arrow

from expense_tracker.et_types import StatisticServiceAggregationInterval, StatisticServiceGroup
from expense_tracker.datasources.lunch_money_datasource import LunchMoneyDatasource
from expense_tracker.services import StatisticService


#==================
#  CONSTANTS
#==================
start_date = arrow.get(datetime(datetime.now().year, 1, 1))
end_date = arrow.get().shift(days=2)

#==================
#  UTILS
#==================
datasource = LunchMoneyDatasource()
service = StatisticService(datasource)

#==================
#  MAIN
#==================
def get_avg_monthly_ytd(filter_by = list[Any] or None):
    if filter_by is None:
        filter_by = []
        # filter_by = [Tag.RENT_APPLICABLE]
    
    category_groups = service.calculate(
        start_date,
        end_date,
        group_by=StatisticServiceGroup.CATEGORY,
        filter_by=filter_by,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )
    top_merchant_groups = service.calculate(
        start_date,
        end_date,
        group_by=StatisticServiceGroup.MERCHANT,
        filter_by=filter_by,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )[:5]
    top_location_groups = service.calculate(
        start_date,
        end_date,
        group_by=StatisticServiceGroup.MERCHANT,
        filter_by=filter_by,
        interval=StatisticServiceAggregationInterval.MONTHLY
    )[:5]
    
    return category_groups, top_merchant_groups, top_location_groups
