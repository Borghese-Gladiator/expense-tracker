from enum import Enum
from typing import Optional, TypedDict

import pandera as pa
from arrow import Arrow
from pandera.typing import Series

from expense_tracker.et_types.statistic_service_types import StatisticServiceFilter
from expense_tracker.utils.date_utils import validate_date_str

class TransactionsSchema(pa.DataFrameModel):
    amount: Series[int] = pa.Field()
    category: Series[str] = pa.Field()
    date: Series[Arrow] = pa.Field()
    description: Series[str] = pa.Field()
    location: Series[str] = pa.Field()
    merchant: Series[str] = pa.Field()
    source: Series[str] = pa.Field()
    tags: Series[set[StatisticServiceFilter]] = pa.Field()

class TransactionDict(TypedDict):
    amount: Arrow
    category: str
    date: str
    description: str | None
    location: str
    merchant: str
    source: str
    tags: set[StatisticServiceFilter] | None
