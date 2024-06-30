from enum import Enum


# TODO: dynamic tags based on datasource
# Currently hard coded tag names from Lunch Money
class StatisticServiceFilter(Enum):
    RENT_APPLICABLE = "rent_applicable"
    
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