from typing import TypedDict
import arrow
from arrow import Arrow
import pandas as pd
from pandera.typing import DataFrame

from expense_tracker.datasources import BaseDatasource
from expense_tracker.et_types import (
    TransactionsSchema,
    StatisticServiceFilter,
    StatisticServiceGroup, 
    StatisticServiceAggregationInterval
)
from expense_tracker.et_types.lunch_money_datasource_types import LunchMoneyFilterColumn, LunchMoneySortColumn
from expense_tracker.et_types.statistic_service_types import FormattedTransactionDict, FormattedTransactionsSchema, StatisticServiceSort, Timeframe

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
        sort_by_set: set[StatisticServiceSort] | None = None,
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
        if sort_by_set is None:
            sort_by_set = {
                StatisticServiceSort(column=LunchMoneySortColumn.DATE, ascending=True),
                StatisticServiceSort(column=LunchMoneySortColumn.AMOUNT, ascending=False)
            }
        if interval is None:
            interval = StatisticServiceAggregationInterval.MONTHLY

        df: DataFrame[TransactionsSchema] = self.datasource.get_transactions(Timeframe(timeframe_start, timeframe_end))
        
        # Filter by time
        df = df[(df['date_arrow'] >= timeframe_start) & (df['date_arrow'] <= timeframe_end)]
        
        # Filter by filter criteria (eg: tags)
        df = self._filter_transactions_df(df, filter_by_set)
        
        # Sort by passed sort columns
        df = self._sort_transactions_df(df, sort_by_set)
        
        # Aggregate by interval (eg: monthly, yearly) and group_by (eg: category, merchant)
        # NOTE: grouping by columns means ALL other columns will be lost (besides "date" which is overrided to group_by value and group_by_list)
        df = df\
            .assign(date=lambda df: df["date_arrow"].apply(lambda x: x.format(self.interval_format_mapping[interval])))\
            .groupby(['date'] + [group_by.column.value for group_by in group_by_set])[['amount']]\
            .mean()\
            .reset_index()

        df: DataFrame[FormattedTransactionsSchema] = self._format_transactions_df(df)
        return df.to_dict(orient='records')

    def get(
        self,
        timeframe_start: Arrow,
        timeframe_end: Arrow,
        filter_by_set: set[StatisticServiceFilter] | None = None,
        sort_by_set: set[StatisticServiceSort] | None = None,
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
        if sort_by_set is None:
            sort_by_set = {StatisticServiceSort(column=LunchMoneySortColumn.DATE, ascending=True)}
        
        df: DataFrame[TransactionsSchema] = self.datasource.get_transactions(Timeframe(timeframe_start, timeframe_end))

        # Filter by time
        df = df[(df['date_arrow'] >= timeframe_start) & (df['date_arrow'] <= timeframe_end)]
        
        # Filter by filter criteria (eg: tags)
        df = self._filter_transactions_df(df, filter_by_set)

        # Sort by passed sort columns
        df = self._sort_transactions_df(df, sort_by_set)
        
        df: DataFrame[FormattedTransactionsSchema] = self._format_transactions_df(df)
        return df.to_dict(orient='records')

    def _filter_transactions_df(self, df: DataFrame[TransactionsSchema], filter_by_set: set[StatisticServiceFilter]) -> DataFrame[TransactionsSchema]:
        """
        Filter the transactions DataFrame by building combined mask using provided filter criteria

        Args:
            df (DataFrame[TransactionsSchema]): The transactions DataFrame to filter.
            filter_by_set (set[StatisticServiceFilter]): The set of filter criteria to apply.
        
        Returns:
            DataFrame[TransactionsSchema]: The filtered transactions DataFrame.
        """
        if not filter_by_set:
            return df

        # start all values with mask of True
        combined_mask = pd.Series([True] * len(df), index=df.index)
        for filter_by in filter_by_set:
            if filter_by.column == LunchMoneyFilterColumn.TAGS:
                mask = df['tags'].apply(lambda tags: filter_by.column_value in tags if tags is not None else False)
            else:
                mask = df[filter_by.column.value] == filter_by.column_value
            if filter_by.exclude:
                mask = ~mask
            # combine the mask with the combined mask using logical AND
            combined_mask &= mask
        # apply combined mask
        return df[combined_mask]

    def _sort_transactions_df(self, df: DataFrame[TransactionsSchema], sort_by_set: set[StatisticServiceSort]) -> DataFrame[TransactionsSchema]:
        # temporary 'date' column to enable sorting
        df['date'] = df['date_arrow'].apply(lambda date: date.format('YYYY-MM-DD'))
        # apply sort
        df = df.sort_values(by=[sort_by.column.value for sort_by in sort_by_set], ascending=[sort_by.ascending for sort_by in sort_by_set])
        # remove temporary 'date' column
        df = df.drop('date', axis=1)
        
        return df

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
        if 'date_arrow' in df:
            df['date'] = df['date_arrow'].apply(lambda date_arrow: date_arrow.format('YYYY-MM-DD'))  # remove Arrow to enable pandas filtering, sorting
            df = df.drop('date_arrow', axis=1)
        if 'tags' in df:
            df['tags'] = df['tags'].apply(lambda tags: None if tags is None else set([tag.value for tag in tags]))
        return df