from arrow import Arrow
from ..datasources.base import BaseDatasource
from ..types import StatisticServiceFilter, StatisticServiceGroup

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
    ):
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
        return
        