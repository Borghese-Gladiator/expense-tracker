from abc import ABC, abstractmethod

from arrow import Arrow
from pandera.typing import DataFrame

from expense_tracker.et_types import TransactionsSchema
from expense_tracker.et_types.statistic_service_types import Timeframe

class BaseDatasource(ABC):
    @abstractmethod
    def get_transactions(self, timeframe: Timeframe) -> DataFrame[TransactionsSchema]:
        """
        NOTE: `transform` converts raw values in BaseTransactionsSchema to enums in TransactionsSchema
        """
        pass
