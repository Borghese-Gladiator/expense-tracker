import arrow
import requests
import pandas as pd
from pandera.typing import DataFrame

from expense_tracker.et_types import TransactionsSchema
from expense_tracker.datasources.base import BaseDatasource
from expense_tracker.utils.settings import LUNCH_MONEY_ACCESS_TOKEN


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
        import faker
        import random
        from expense_tracker.et_types.BaseDatasourceTypes import CreditSource, Tag
        num_records = 10
        data = {
            "date": [faker.date_time_this_year(tzinfo=None, before_now=True) for _ in range(num_records)],
            "name": [faker.company() for _ in range(num_records)],
            "description": [faker.sentence() if random.random() < 0.5 else None for _ in range(num_records)],
            "amount": [random.randint(10, 1000) for _ in range(num_records)],
            "category": [faker.word() for _ in range(num_records)],
            "merchant": [faker.company() for _ in range(num_records)],
            "location": [faker.address() for _ in range(num_records)],
            "source": [random.choice(list(CreditSource)) for _ in range(num_records)],
            "tags": [[random.choice(list(Tag)) for _ in range(random.randint(0, 3)) if random.random() < 0.8] for _ in range(num_records)]
        }
        df = pd.DataFrame(data)
        validated_df = TransactionsSchema.validate(df)
        return validated_df
