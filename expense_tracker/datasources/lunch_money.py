import requests

from expense_tracker.datasources.base import BaseDatasource
from ..utils.settings import LUNCH_MONEY_ACCESS_TOKEN

class LunchMoneyDatasource(BaseDatasource):
    base_url: str = 'https://dev.lunchmoney.app'
    default_headers = {
        'Authorization': f'Bearer {LUNCH_MONEY_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    def get_transactions(self):
        endpoint = f'{self.base_url}/v1/transactions'
        headers = self.default_headers
        params = {}
        response = requests.get(endpoint, headers=headers, params=params)


