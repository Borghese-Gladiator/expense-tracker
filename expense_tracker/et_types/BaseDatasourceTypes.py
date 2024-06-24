from enum import Enum
from typing import Optional

import pandera as pa
import pandas as pd
from pandera.typing import Series
from pandera.extensions import CheckType

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

class Tag(Enum):
    RENT_APPLICABLE = "rent_applicable"


class TransactionsSchema(pa.DataFrameModel):
    date: Series[Annotated[pd.DatetimeTZDtype, "utc"]] = pa.Field()
    name: Series[str] = pa.Field()
    description: Optional[Series[str]] = pa.Field()
    amount: Series[int] = pa.Field()
    category: Series[str] = pa.Field()
    merchant: Series[str] = pa.Field()
    location: Series[str] = pa.Field()
    
    source: Series[CreditSource] = pa.Field()
    tags: Series[list[Tag]] = pa.Field()
    
    """
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