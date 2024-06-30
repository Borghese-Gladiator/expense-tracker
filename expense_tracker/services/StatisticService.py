import pandas as pd
from arrow import Arrow
from pandera.typing import DataFrame

from expense_tracker.datasources import BaseDatasource
from expense_tracker.et_types import (
    TransactionsSchema,
    StatisticServiceFilter,
    StatisticServiceGroup, 
    StatisticServiceAggregationInterval
)

class StatisticService:
    datasource: BaseDatasource

    def __init__(self, datasource):
        self.datasource = datasource

    def calculate(
        self,
        timeframe_start: Arrow,
        timeframe_end: Arrow,
        filter_by: StatisticServiceFilter,
        group_by: StatisticServiceGroup,
        interval: StatisticServiceAggregationInterval,
    ) -> list[dict]:
        df: DataFrame[TransactionsSchema] = self.datasource.get_transactions()
        # Filter by time
        df = df[(df['date'] >= timeframe_start) & (df['date'] <= timeframe_end)]
        # Filter by tags
        df = df if filter_by is None else df[df['tags'].apply(lambda tags: filter_by.value in tags)]
        # Group by columns Apply the group by columns (eg: category, merchant, location)
        df = df.groupby(group_by.value)
        # Apply the group by and aggregate by interval (eg: monthly, yearly)
        interval_mapping = {
            StatisticServiceAggregationInterval.MONTHLY: '%Y-%m',
            StatisticServiceAggregationInterval.YEARLY: '%Y'
        }
        df['period'] = pd.to_datetime(df['date']).dt.strftime(interval_mapping[interval])
        aggregated_df = df.groupby('period')['amount'].sum().reset_index()
        return aggregated_df.to_dict(orient='records')

    def get(
        self,
        timeframe_start: Arrow,
        timeframe_end: Arrow,
        filter_by: StatisticServiceFilter,
    ) -> list[dict]:
        df: DataFrame[TransactionsSchema] = self.datasource.get_transactions()
        # Apply the time filter
        df = df[(df['date'] >= timeframe_start) & (df['date'] <= timeframe_end)]
        # Apply the filter by 'tags'
        df = df[df['tags'].apply(lambda tags: filter_by in tags)]
        return df.to_dict(orient='records')
        