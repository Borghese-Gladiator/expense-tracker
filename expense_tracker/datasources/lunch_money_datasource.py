import arrow
import requests
import pandas as pd
from pandera.typing import DataFrame

from expense_tracker.et_types import TransactionsSchema
from expense_tracker.datasources.base_datasource import BaseDatasource
from expense_tracker.et_types.statistic_service_types import StatisticServiceFilter
from expense_tracker.utils.settings import LUNCH_MONEY_ACCESS_TOKEN
from expense_tracker.et_types.base_datasource_types import CreditSource


class LunchMoneyDatasource(BaseDatasource):
    base_url: str = 'https://dev.lunchmoney.app'
    default_headers = {
        'Authorization': f'Bearer {LUNCH_MONEY_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    def get_transactions(self) -> DataFrame[TransactionsSchema]:
        """
        endpoint = f'{self.base_url}/v1/transactions'
        headers = self.default_headers
        params = {}
        response = requests.get(endpoint, headers=headers, params=params)
        """
        from faker import Faker
        import random
        fake = Faker()
        num_records = 10
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
        df = pd.DataFrame(data)
        validated_df = TransactionsSchema.validate(df)
        return validated_df
