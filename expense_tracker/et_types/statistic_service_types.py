from dataclasses import dataclass
from enum import Enum

from arrow import Arrow


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