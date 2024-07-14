from typing import TypedDict
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
from expense_tracker.et_types.statistic_service_types import FormattedTransactionDict, FormattedTransactionsSchema, Timeframe

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
        filter_by_set: set[StatisticServiceFilter] | None = None,
        group_by_set: set[StatisticServiceGroup] | None = None,
        interval: StatisticServiceAggregationInterval | None = None,
    ) -> list[dict]:
        """
        returns list of formatted dicts aggregated by interval
        """
        if filter_by_set is None:
            filter_by_set = set()
        if group_by_set is None:
            group_by_set = set()
        if interval is None:
            interval = StatisticServiceAggregationInterval.MONTHLY

        df: DataFrame[TransactionsSchema] = self.datasource.get_transactions(Timeframe(timeframe_start, timeframe_end))
        
        # Filter by time
        df = df[(df['date'] >= timeframe_start) & (df['date'] <= timeframe_end)]
        
        # Filter by tags
        # NOTE: tags <= filter_by_set is a subset comparison checking if tags is a subset of filter_by_set
        if len(filter_by_set) > 0:
            mask = df['tags'].apply(lambda tags: False if tags is None else tags <= filter_by_set)
            df = df[mask]
        
        # Aggregate by interval (eg: monthly, yearly) and group_by (eg: category, merchant)
        # NOTE: grouping by columns means ALL other columns will be lost (besides "date" which is overrided to group_by value and group_by_list)
        df = df\
            .assign(date=lambda df: df["date"].apply(lambda x: x.format(self.interval_format_mapping[interval])))\
            .groupby(['date'] + [group_by.value for group_by in group_by_set])[['amount']]\
            .mean()\
            .reset_index()
        
        df: DataFrame[FormattedTransactionsSchema] = self._format_transactions_df(df)
        return df.to_dict(orient='records')

    def get(
        self,
        timeframe_start: Arrow,
        timeframe_end: Arrow,
        filter_by_set: set[StatisticServiceFilter] | None = None,
    ) -> list[FormattedTransactionDict]:
        if filter_by_set is None:
            filter_by_set = set()
        
        df: DataFrame[TransactionsSchema] = self.datasource.get_transactions(Timeframe(timeframe_start, timeframe_end))

        # Filter by time
        df = df[(df['date'] >= timeframe_start) & (df['date'] <= timeframe_end)]
        
        # Filter by tags
        # NOTE: tags <= filter_by_set is a subset comparison checking if tags is a subset of filter_by_set
        if len(filter_by_set) > 0:
            mask = df['tags'].apply(lambda tags: False if tags is None else tags <= filter_by_set)
            df = df[mask]
        
        df: DataFrame[FormattedTransactionsSchema] = self._format_transactions_df(df)
        return df.to_dict(orient='records')
        
    def _format_transactions_df(self, df: DataFrame[TransactionsSchema]) -> DataFrame[FormattedTransactionsSchema]:
        if 'date' in df:
            df['date'] = df['date'].apply(lambda date: date.format('YYYY-MM-DD'))
        if 'tags' in df:
            df['tags'] = df['tags'].apply(lambda tags: None if tags is None else set([tag.value for tag in tags]))
        return df