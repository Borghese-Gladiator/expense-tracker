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
        Calculate statistics within a specified timeframe, optionally filtered and grouped by certain criteria.

        This method computes and returns a list of dictionaries representing the calculated statistics over the 
        specified timeframe. The results can be filtered, grouped, and aggregated based on the provided parameters.

        Args:
            timeframe_start (Arrow): The start of the timeframe for which to calculate statistics.
            timeframe_end (Arrow): The end of the timeframe for which to calculate statistics.
            filter_by_set (set[StatisticServiceFilter] | None, optional): A set of filters to apply when calculating 
                statistics. If None, no filtering is applied. Default is None.
            group_by_set (set[StatisticServiceGroup] | None, optional): A set of grouping criteria to apply when 
                calculating statistics. If None, no grouping is applied. Default is None.
            interval (StatisticServiceAggregationInterval | None, optional): The interval at which to aggregate 
                the statistics (e.g., daily, weekly, monthly). If None, no aggregation is applied. Default is None.

        Returns:
            list[dict]: A list of dictionaries containing the calculated statistics. Each dictionary represents 
                a set of statistics for a specific group (if grouping is applied) and/or interval (if aggregation 
                is applied).

        Example:
            >>> timeframe_start = Arrow.utcnow().shift(days=-30)
            >>> timeframe_end = Arrow.utcnow()
            >>> filters = {StatisticServiceFilter.USER, StatisticServiceFilter.COUNTRY}
            >>> groups = {StatisticServiceGroup.COUNTRY, StatisticServiceGroup.CATEGORY}
            >>> interval = StatisticServiceAggregationInterval.DAILY
            >>> stats = service.calculate(timeframe_start, timeframe_end, filters, groups, interval)
            >>> for stat in stats:
            ...     print(stat)

        Notes:
            - The Arrow type is used for datetime manipulation and representation.
            - StatisticServiceFilter, StatisticServiceGroup, and StatisticServiceAggregationInterval are 
            enums or classes representing specific filtering, grouping, and aggregation criteria, respectively.

        Raises:
            ValueError: If the timeframe_start is after timeframe_end.
            TypeError: If the filter_by_set or group_by_set contain invalid types.
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
        
        sorted_df = df.sort_values(by=['amount'], ascending=[False])

        df: DataFrame[FormattedTransactionsSchema] = self._format_transactions_df(sorted_df)
        return df.to_dict(orient='records')

    def get(
        self,
        timeframe_start: Arrow,
        timeframe_end: Arrow,
        filter_by_set: set[StatisticServiceFilter] | None = None,
    ) -> list[FormattedTransactionDict]:
        """
        Get transactions within a specified timeframe, optionally filtered by certain criteria.

        This method retrieves and returns a list of dictionaries representing the transactions within the specified
        timeframe. The results can be filtered based on the provided parameters.

        Args:
            timeframe_start (Arrow): The start of the timeframe for which to retrieve transactions.
            timeframe_end (Arrow): The end of the timeframe for which to retrieve transactions.
            filter_by_set (set[StatisticServiceFilter] | None, optional): A set of filters to apply when retrieving
                transactions. If None, no filtering is applied. Default is None.
        
        Returns:
            list[FormattedTransactionDict]: A list of dictionaries containing the retrieved transactions. Each dictionary
                represents a single transaction with formatted values.
        """
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

        sorted_df = df.sort_values(by=['amount'], ascending=[False])
        
        df: DataFrame[FormattedTransactionsSchema] = self._format_transactions_df(sorted_df)
        return df.to_dict(orient='records')
        
    def _format_transactions_df(self, df: DataFrame[TransactionsSchema]) -> DataFrame[FormattedTransactionsSchema]:
        """
        Format the transactions DataFrame to have human-readable str values for tables.

        This method formats the transactions DataFrame to have human-readable values for the date and tags columns.
        The date column is formatted as a string in the 'YYYY-MM-DD' format, and the tags column is formatted as a set
        of tag values.

        Args:
            df (DataFrame[TransactionsSchema]): The transactions DataFrame to format.
        
        Returns:
            DataFrame[FormattedTransactionsSchema]: The formatted transactions DataFrame with human-readable values.
        """
        if 'date' in df:
            df['date'] = df['date'].apply(lambda date: date.format('YYYY-MM-DD'))
        if 'tags' in df:
            df['tags'] = df['tags'].apply(lambda tags: None if tags is None else set([tag.value for tag in tags]))
        return df