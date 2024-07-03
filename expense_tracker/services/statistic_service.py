from typing import Set, TypedDict
import arrow
from arrow import Arrow
from pandera.typing import DataFrame

from expense_tracker.datasources import BaseDatasource
from expense_tracker.et_types import (
    TransactionsSchema,
    StatisticServiceFilter,
    StatisticServiceGroup, 
    StatisticServiceAggregationInterval
)

class Transaction(TypedDict):
    date: arrow.Arrow
    merchant: str
    description: str
    amount: int
    category: str
    location: str
    source: str
    tags: list[StatisticServiceFilter]

class StatisticService:
    datasource: BaseDatasource
    interval_format_mapping = {
        StatisticServiceAggregationInterval.MONTHLY: "YYYY-MM",
        StatisticServiceAggregationInterval.YEARLY: "YYYY"
    }

    def __init__(self, datasource):
        self.datasource = datasource

    def calculate(
        self,
        timeframe_start: Arrow,
        timeframe_end: Arrow,
        filter_by_set: Set[StatisticServiceFilter] = None,
        group_by_set: Set[StatisticServiceGroup] = None,
        interval: StatisticServiceAggregationInterval = None,
    ) -> list[dict]:
        if group_by_set is None:
            group_by_set = []
        if interval is None:
            interval = StatisticServiceAggregationInterval.MONTHLY

        df: DataFrame[TransactionsSchema] = self.datasource.get_transactions()
        
        # Filter by time
        df = df[(df['date'] >= timeframe_start) & (df['date'] <= timeframe_end)]
        
        # Filter by tags
        # NOTE: tags <= filter_by_set is a subset comparison checking if tags is a subset of filter_by_set
        if filter_by_set is not None:
            mask = df['tags'].apply(lambda tags: False if tags is None else tags <= filter_by_set)
            df = df[mask]
        
        # Aggregate by interval (eg: monthly, yearly) and group_by (eg: category, merchant)
        # NOTE: grouping by columns means ALL other columns will be lost (besides "date" which is overrided to group_by value and group_by_list)
        df = df\
            .assign(date=lambda df: df["date"].apply(lambda x: x.format(self.interval_format_mapping[interval])))\
            .groupby(['date'] + [group_by.value for group_by in group_by_set])[['amount']]\
            .mean()\
            .reset_index()
        
        return df.to_dict(orient='records')

    def get(
        self,
        timeframe_start: Arrow,
        timeframe_end: Arrow,
        filter_by_set: Set[StatisticServiceFilter],
    ) -> list[Transaction]:
        df: DataFrame[TransactionsSchema] = self.datasource.get_transactions()

        # Filter by time
        df = df[(df['date'] >= timeframe_start) & (df['date'] <= timeframe_end)]
        
        # Filter by tags
        # NOTE: tags <= filter_by_set is a subset comparison checking if tags is a subset of filter_by_set
        if filter_by_set is not None:
            mask = df['tags'].apply(lambda tags: False if tags is None else tags <= filter_by_set)
            df = df[mask]
        
        return df.to_dict(orient='records')
        