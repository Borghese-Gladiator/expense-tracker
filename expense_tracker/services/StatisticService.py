import pandas as pd
from arrow import Arrow
from pandera.typing import DataFrame

from expense_tracker.datasources.base import BaseDatasource
from expense_tracker.et_types import StatisticServiceFilter, StatisticServiceGroup, TransactionsSchema


class StatisticService:
    datasource: BaseDatasource

    def __init__(self, datasource):
        self.datasource = datasource

    def calculate(
        self,
        timeframe_start: Arrow,
        timeframe_end: Arrow,
        filter_by: StatisticServiceFilter,
        group_by: StatisticServiceGroup
    ) -> list[dict]:
        transactions: DataFrame[TransactionsSchema] = self.datasource.get_transactions()
        """
        get all stats
        filter timeframe
        filter by filter_by
        group by group_by
        """
        return
    
    def get(
        self,
        timeframe_start: Arrow,
        timeframe_ens: Arrow,
        filter_by: StatisticServiceFilter,
    ):
        """
        """
        transactions: pd.DataFrame = self.datasource.get_transactions()
        return
        