import unittest
from unittest.mock import Mock

import arrow
import pandas as pd
from faker import Faker

from expense_tracker.datasources import BaseDatasource
from expense_tracker.et_types import (
    StatisticServiceFilter,
    StatisticServiceGroup, 
    StatisticServiceAggregationInterval
)
from expense_tracker.et_types.base_datasource_types import CreditSource
from expense_tracker.services import StatisticService

class TestStatisticService(unittest.TestCase):
    def setUp(self):
        self.mock_datasource = Mock(spec=BaseDatasource)
        self.service = StatisticService(self.mock_datasource)

        fake = Faker()
        data = {
            'date_str': [
                '2023-01-01',
                '2023-02-15',
                '2023-03-10',
                '2023-03-30',
                '2023-03-10',
            ],
            "merchant": [
                "Stop & Shop",
                "Chipotle",
                "CVS",
                "Stop & Shop",
                "Stop & Shop",
            ],
            "description": [fake.sentence(), fake.sentence(), fake.sentence(), fake.sentence(), fake.sentence()],
            'amount': [100.0, 200.0, 300.0, 400.0, 250.0],
            'category': ['Restaurants', 'Groceries', 'Gas', 'Gas', 'Groceries'],
            "location": [fake.address(), fake.address(), fake.address(), fake.address(), fake.address()],
            "source": [CreditSource.CAPITAL_ONE.value, CreditSource.CAPITAL_ONE.value, CreditSource.CAPITAL_ONE.value, CreditSource.FIDELITY.value, CreditSource.FIDELITY.value],
            "tags": [StatisticServiceFilter.RENT_APPLICABLE.value, None, None, None, StatisticServiceFilter.RENT_APPLICABLE.value]
        }
        self.df = pd.DataFrame(data)
        self.mock_datasource.get_transactions.return_value = pd.DataFrame(data)

    def test_calculate_monthly(self):
        timeframe_start = arrow.get('2023-01-01')
        timeframe_end = arrow.get('2023-12-31')
        interval = StatisticServiceAggregationInterval.MONTHLY

        # Validate TIMEFRAME respected
        self.assertEqual(self.service.calculate(
            arrow.get('2023-03-10'),
            arrow.get('2023-03-30'),
            None,
            None,
            interval
        ), [
            {'date': '2023-03', 'amount': 316.6666666666667},
        ])
        
        # Validate FILTER respected and non rent-applicable transactions are filtered out
        self.assertEqual(self.service.calculate(
            timeframe_start,
            timeframe_end,
            set([StatisticServiceFilter.RENT_APPLICABLE]),
            None,
            interval
        ), [
            {'date': '2023-01', 'amount': 100.0},
            {'date': '2023-03', 'amount': 250.0},
        ])

        # Validate CATEGORY groups as expected and amounts are grouped by interval + category
        self.assertEqual(self.service.calculate(
            timeframe_start,
            timeframe_end,
            None,
            set([StatisticServiceGroup.CATEGORY]),
            interval
        ), [
            {'date': '2023-01', 'category': 'Restaurants', 'amount': 100.0},
            {'date': '2023-02', 'category': 'Groceries', 'amount': 200.0},
            {'date': '2023-03', 'category': 'Gas', 'amount': 350.0},
            {'date': '2023-03', 'category': 'Groceries', 'amount': 250.0},
        ])


    def test_calculate_yearly(self):
        timeframe_start = arrow.get('2023-01-01')
        timeframe_end = arrow.get('2023-12-31')
        interval = StatisticServiceAggregationInterval.YEARLY
        
        self.assertEqual(self.service.calculate(
            timeframe_start,
            timeframe_end,
            None,
            set([StatisticServiceGroup.CATEGORY]),
            interval
        ), [
            {'amount': 350.0, 'category': 'Gas', 'date': '2023'},
            {'amount': 225.0, 'category': 'Groceries', 'date': '2023'},
            {'amount': 100.0, 'category': 'Restaurants', 'date': '2023'}
        ])

    def test_get_with_tag_filter(self):
        timeframe_start = arrow.get('2023-01-01')
        timeframe_end = arrow.get('2023-12-31')
        filter_by = StatisticServiceFilter.RENT_APPLICABLE

        expected_output = self.df[self.df['tags'].apply(lambda tags: filter_by.value in tags)].to_dict(orient='records')

        result = self.service.get(
            timeframe_start,
            timeframe_end,
            set([filter_by])
        )

        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
