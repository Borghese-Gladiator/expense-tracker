from enum import Enum


# TODO: dynamic tags based on datasource
class StatisticServiceFilter(Enum):
    RENT_APPLICABLE = "rent_applicable"    


# TODO: dynamic columns based on datasource
class StatisticServiceGroup(Enum):
    CATEGORY = "category"
    MERCHANT = "merchant"
    LOCATION = "location"

class StatisticServiceAggregationInterval(Enum):
    # WEEKLY = "weekly"  # TODO: add support for weekly
    MONTHLY = "monthly"
    YEARLY = "yearly"