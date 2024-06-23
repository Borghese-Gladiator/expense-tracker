import arrow
import pandera as pa
from pandera import DataFrameSchema, Column, Check
from pandera import Series
from pandera.engines import pandas_engine

class CreditSource(Enum):
    CAPITAL_ONE = "capital_one"
    CHASE = "chase"
    DISCOVER = "discover"
    FIDELITY = "fidelity"
    PAYPAL = "paypal"

class Tag(Enum):
    RENT_APPLICABLE = "rent_applicable"

# Define the schema using pandera SchemaModel
class StatusListSchema(pa.SchemaModel):
    statuses: pa.Series[List[Status]] = pa.Field(
        check=pa.Check(lambda x: all(item in Status.__members__.values() for item in x))
    )

class TransactionsSchema(pa.SchemaModel):
    # TODO: do I get dates in UTC or EST?
    date: Series[
        pandas_engine.DateTime(
            to_datetime_kwargs = {"format":"%Y-%m-%dT%H:%M:%S"},
            tz = "UTC"
        )
    ] = pa.Field()
    name: Series[str] = pa.Field()
    description: Series[str] = pa.Field(required=False)
    amount: Series[int] = pa.Field()
    category: Series[str] = pa.Field()
    merchant: Series[str] = pa.Field()
    location: Series[str] = pa.Field()
    
    source: Series[CreditSource] = pa.Field()
    tags: pa.Series[pa.Nullable[list[Tag]]] = pa.Field(
        coerce=True,
        default_factory=list,  # transforms None into []
        check=pa.Check(lambda x: all(item in Tag.__members__.values() for item in x) if x is not None else None)
    )