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
from expense_tracker.services.statistic_service import Transaction

class TestStatisticService(unittest.TestCase):
    def setUp(self):
        self.mock_datasource = Mock(spec=BaseDatasource)
        self.service = StatisticService(self.mock_datasource)

        fake = Faker()
        data = {
            'date': [
                arrow.get('2023-01-01', "YYYY-MM-DD"),
                arrow.get('2023-02-15', "YYYY-MM-DD"),
                arrow.get('2023-03-10', "YYYY-MM-DD"),
                arrow.get('2023-03-30', "YYYY-MM-DD"),
                arrow.get('2023-03-10', "YYYY-MM-DD"),
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
            "source": [CreditSource.CAPITAL_ONE, CreditSource.CAPITAL_ONE, CreditSource.CAPITAL_ONE, CreditSource.FIDELITY, CreditSource.FIDELITY],
            "tags": [{StatisticServiceFilter.BROTHER_RENT}, None, None, None, {StatisticServiceFilter.BROTHER_RENT}]
        }
        self.df = pd.DataFrame(data)
        self.mock_datasource.get_transactions.return_value = pd.DataFrame(data)

    def test_calculate(self):
        timeframe_start = arrow.get('2023-01-01')
        timeframe_end = arrow.get('2023-12-31')
        monthly_interval = StatisticServiceAggregationInterval.MONTHLY

        # Validate TIMEFRAME respected
        self.assertEqual(self.service.calculate(
            arrow.get('2023-03-10'),
            arrow.get('2023-03-30'),
            None,
            None,
            monthly_interval
        ), [
            {'date': '2023-03', 'amount': 316.6666666666667},
        ])
        
        # Validate FILTER respected and non rent-applicable transactions are filtered out
        self.assertEqual(self.service.calculate(
            timeframe_start,
            timeframe_end,
            set([StatisticServiceFilter.BROTHER_RENT]),
            None,
            monthly_interval
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
            monthly_interval
        ), [
            {'date': '2023-01', 'category': 'Restaurants', 'amount': 100.0},
            {'date': '2023-02', 'category': 'Groceries', 'amount': 200.0},
            {'date': '2023-03', 'category': 'Gas', 'amount': 350.0},
            {'date': '2023-03', 'category': 'Groceries', 'amount': 250.0},
        ])
        
        # Validate YEARLY aggregation interval
        self.assertEqual(self.service.calculate(
            timeframe_start,
            timeframe_end,
            None,
            set([StatisticServiceGroup.CATEGORY]),
            StatisticServiceAggregationInterval.YEARLY
        ), [
            {'amount': 350.0, 'category': 'Gas', 'date': '2023'},
            {'amount': 225.0, 'category': 'Groceries', 'date': '2023'},
            {'amount': 100.0, 'category': 'Restaurants', 'date': '2023'}
        ])

    def test_get(self):
        def _convert_df_input_to_output(df: pd.DataFrame) -> list[Transaction]:
            return (
                df
                .assign(date=lambda df: df["date_str"].apply(lambda x: arrow.get(x, "YYYY-MM-DD")))
                .drop("date_str", axis=1)
                .to_dict(orient='records')
            )
            
        timeframe_start = arrow.get('2023-01-01')
        timeframe_end = arrow.get('2023-12-31')

        # Validate TIMEFRAME respected
        self.assertEqual(self.service.get(
            arrow.get('2023-03-10'),
            arrow.get('2023-03-30'),
            None,
        ), self.df.iloc[[2, 3, 4]].to_dict(orient='records'))
        
        # Validate FILTER respected and non rent-applicable transactions are filtered out
        self.assertEqual(self.service.get(
            timeframe_start,
            timeframe_end,
            set([StatisticServiceFilter.BROTHER_RENT]),
        ), self.df.iloc[[0, 4]].to_dict(orient='records'))
        # Validate with empty list of transactions
        self.mock_datasource.get_transactions.return_value = pd.DataFrame({
            'date': [],
            "merchant": [],
            "description": [],
            'amount': [],
            'category': [],
            "location": [],
            "source": [],
            "tags": []
        })
        self.assertEqual(self.service.get(
            timeframe_start,
            timeframe_end,
            set([StatisticServiceFilter.BROTHER_RENT]),
        ), [])

if __name__ == '__main__':
    unittest.main()
