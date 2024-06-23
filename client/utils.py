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