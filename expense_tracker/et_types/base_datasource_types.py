from enum import Enum
from typing import Optional, TypedDict

import pandera as pa
from arrow import Arrow
from pandera.typing import Series

from expense_tracker.et_types.statistic_service_types import StatisticServiceFilter
from expense_tracker.utils.date_utils import validate_date_str


class CreditSource(Enum):
    CAPITAL_ONE = "Capital One"
    CHASE = "Chase"
    DISCOVER = "Discover"
    FIDELITY = "Fidelity"
    PAYPAL = "PayPal"
    MANUAL = "manual"
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class TransactionsSchema(pa.DataFrameModel):
    date: Series[Arrow] = pa.Field()
    source: Series[CreditSource] = pa.Field()
    tags: Series[set[StatisticServiceFilter]] = pa.Field()
    merchant: Series[str] = pa.Field()
    description: Series[str] = pa.Field()
    amount: Series[int] = pa.Field()
    category: Series[str] = pa.Field()
    location: Series[str] = pa.Field()

class TransactionDict(TypedDict):
    date: Arrow
    amount: int
    merchant: str
    category: str
    description: str | None
    source: CreditSource
    tags: set[StatisticServiceFilter] | None
    location: str


"""
NOTE: pandera does NOT recognize `Optional[str]` nor `str | None` (It works for DataFrame Schemas but not DataFrame Models like below)
"""
"""
class BaseTransactionsSchema(pa.DataFrameModel):
    raw_date: Series[str] = pa.Field()
    raw_source: Series[str] = pa.Field()
    raw_tags: Series[str] = pa.Field()
    merchant: Series[str] = pa.Field()
    description: Series[str] = pa.Field()
    amount: Series[int] = pa.Field()
    category: Series[str] = pa.Field()
    location: Series[str] = pa.Field()

    @pa.check("raw_date")
    def custom_check(cls, raw_date: Series[list[str]]) -> Series[bool]:
        return all(validate_date_str(date_str) for date_str in raw_date)

    @pa.check("raw_source")
    def custom_check(cls, raw_source: Series[list[str]]) -> Series[bool]:
        return all(item in CreditSource.list() for item in raw_source)

    @pa.check("raw_tags")
    def custom_check(cls, raw_tags: Series[list[str]]) -> Series[bool]:
        for tags_str in raw_tags:
            for tag in tags_str.split(','):
                if tag is not None and tag not in StatisticServiceFilter.list():
                    return False
        return True

@pa.check_types
def transform(df: DataFrame[BaseTransactionsSchema]) -> DataFrame[TransactionsSchema]:
    # add Date column for timeframe comparisons
    df = (
        df.assign(date=lambda df: df["raw_date"].apply(lambda x: arrow.get(x, "YYYY-MM-DD")))
        .drop("raw_date", axis=1)
    )

    # add Tags column for tag comparison in filters
    df = (
        df.assign(
            tags=df["tags"].apply(
                lambda x: None
                if x is None
                else set([StatisticServiceFilter(tag_str) for tag_str in x.split(",")])
            )
        ).drop("raw_tags", axis=1)
    )

    # add Source column for credit card filter
    df = (
        df.assign(
            source=df["source"].apply(lambda x: None if x is None else CreditSource(x))
        ).drop("raw_source", axis=1)
    )

    return df
"""