from enum import Enum
from typing import Optional

import pandera as pa
import pandas as pd
from pandera import Timestamp
from pandera.typing import Series

from expense_tracker.utils.date_utils import validate_date_str

try:
    from typing import Annotated  # python 3.9+
except ImportError:
    from typing_extensions import Annotated


class CreditSource(Enum):
    CAPITAL_ONE = "capital_one"
    CHASE = "chase"
    DISCOVER = "discover"
    FIDELITY = "fidelity"
    PAYPAL = "paypal"
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class Tag(Enum):
    RENT_APPLICABLE = "rent_applicable"
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class TransactionsSchema(pa.DataFrameModel):
    date_str: Series[str] = pa.Field()
    merchant: Series[str] = pa.Field()
    description: Optional[Series[str]] = pa.Field()
    amount: Series[int] = pa.Field()
    category: Series[str] = pa.Field()
    location: Series[str] = pa.Field()
    source: Series[str] = pa.Field()
    tags: Series[Optional[str]] = pa.Field()

    @pa.check("date_str")
    def custom_check(cls, date_str: Series[list[str]]) -> Series[bool]:
        return all(validate_date_str(single_date_str) for single_date_str in date_str)

    @pa.check("source")
    def custom_check(cls, source: Series[list[str]]) -> Series[bool]:
        return all(item in CreditSource.list() for item in source)

    @pa.check("tags")
    def custom_check(cls, tags: Series[list[str]]) -> Series[bool]:
        for tags_str in tags:
            for tag in tags_str.split(','):
                if tag is not None and tag not in Tag.list():
                    return False
        return True
    
    """
    # date: Series[Annotated[pd.DatetimeTZDtype, 's', 'America/New_York']] = pa.Field()

    source: Series[CreditSource] = pa.Field()

    source: Series[] = pa.Field() # pa.Field[pa.Enum[CreditSource]]
    tags: pa.Field[pa.Set[pa.Enum[Tag]]]
    tags: Series[str] = pa.Field()  # CSV str to parse
    tags: Series[list[Tag]] = pa.Field(
        coerce=True,
        check_name=list,  # transforms None into []
    )
    @pa.check("tags", name="foobar")
    def custom_check(cls, tags: Series[list[Tag]]) -> Series[bool]:
        if tags is None:
            return []
        return all(item in Tag.__members__.values() for item in tags)
    """