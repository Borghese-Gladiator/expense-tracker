from dataclasses import dataclass
from enum import Enum
from typing import TypedDict

import pandera as pa
from arrow import Arrow
from pandera.typing import Series


# TODO: dynamic tags based on datasource
# Currently hard coded tag names from Lunch Money
class StatisticServiceFilter(Enum):
    BROTHER_RENT = "Brother Rent"
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


# TODO: dynamic columns based on datasource
# Currently hard coded names used in base_datasource_types
class StatisticServiceGroup(Enum):
    CATEGORY = "category"
    MERCHANT = "merchant"
    LOCATION = "location"

class StatisticServiceAggregationInterval(Enum):
    # WEEKLY = "weekly"  # TODO: add support for weekly
    MONTHLY = "monthly"
    YEARLY = "yearly"

@dataclass
class Timeframe:
    start: Arrow
    end: Arrow

    def format(self, format_str: str) -> tuple[str, str]:
        return self.start.format(format_str), self.end.format(format_str)

    def __hash__(self):
        """
        Compute hash based on attributes (required to use @cache)
        """
        return hash((self.start, self.end))

class FormattedTransactionsSchema(pa.DataFrameModel):
    amount: Series[int] = pa.Field()
    category: Series[str] = pa.Field()
    date: Series[str] = pa.Field()
    description: Series[str] = pa.Field()
    location: Series[str] = pa.Field()
    merchant: Series[str] = pa.Field()
    source: Series[str] = pa.Field()
    tags: Series[set[str]] = pa.Field()

class FormattedTransactionDict(TypedDict):
    amount: int
    category: str
    date: str
    description: str | None
    location: str
    merchant: str
    source: str
    tags: set[str] | None