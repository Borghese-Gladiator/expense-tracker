import arrow
import requests
import pandas as pd
from pandera.typing import DataFrame

from expense_tracker.et_types import TransactionsSchema
from expense_tracker.datasources.BaseDatasource import BaseDatasource
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
        from faker import Faker
        import random
        from expense_tracker.et_types.BaseDatasourceTypes import CreditSource, Tag
        fake = Faker()
        num_records = 10
        data = {
            "date": [fake.date_time() for _ in range(num_records)],
            "name": [fake.company() for _ in range(num_records)],
            "description": [fake.sentence() if random.random() < 0.5 else None for _ in range(num_records)],
            "amount": [random.randint(10, 1000) for _ in range(num_records)],
            "category": [fake.word() for _ in range(num_records)],
            "merchant": [fake.company() for _ in range(num_records)],
            "location": [fake.address() for _ in range(num_records)],
            "source": [random.choice(list(CreditSource)) for _ in range(num_records)],
            "tags": [[random.choice(list(Tag)) for _ in range(random.randint(0, 3)) if random.random() < 0.8] for _ in range(num_records)]
        }
        df = pd.DataFrame(data)
        validated_df = TransactionsSchema.validate(df)
        return validated_df
        print("REACHED")
        """
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
        return validated_df
    
