from dataclasses import dataclass
from enum import Enum
from functools import cache

import arrow
import pandas as pd
import requests
from arrow import Arrow
from pandera.typing import DataFrame

from expense_tracker.et_types import TransactionsSchema
from expense_tracker.datasources.base_datasource import BaseDatasource, BaseDatasourceSettings
from expense_tracker.et_types.base_datasource_types import TransactionDict
from expense_tracker.et_types.statistic_service_types import StatisticServiceFilter, Timeframe


class TxnStatus(Enum):
    CLEARED = "cleared"
    UNCLEARED = "uncleared"

@dataclass
class LunchMoneyDatasourceSettings(BaseDatasourceSettings):
    access_token: str


class LunchMoneyDatasource(BaseDatasource):
    base_url: str = 'https://dev.lunchmoney.app'
    timeframe_format: str = "YYYY-MM-DD"

    def __init__(self, settings: LunchMoneyDatasourceSettings):
        self.access_token = settings.access_token
        self.default_headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    @cache
    def get_transactions(self, timeframe: Timeframe) -> DataFrame[TransactionsSchema]:
        """
        Gets transactions for given timeframe
        """
        # CONSTANTS
        endpoint = f'{self.base_url}/v1/transactions'
        headers = self.default_headers

        # PARAMS
        timeframe_start_str, timeframe_end_str = timeframe.format(self.timeframe_format)
        params = {
            "debit_as_negative": True,
            "start_date": timeframe_start_str,
            "end_date": timeframe_end_str,
            "status": TxnStatus.CLEARED.value,
        }
        try:
            resp = requests.get(endpoint, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            txn_list: list[TransactionDict] = self._transform_raw_to_transactions_list(data['transactions'])
            df: DataFrame[TransactionsSchema] = pd.DataFrame(txn_list)
            df.fillna("", inplace=True)
            return df
        except requests.HTTPError as e:
            # possibly check response for a message
            raise e
        except requests.Timeout as e:
            # request took too long
            raise e

    def _transform_raw_to_transactions_list(self, txn_list: list[dict]) -> list[TransactionDict]:
        """
        Transforms raw transactions list from Lunch Money into expected TransactionDict list
        """
        res: list[dict] = []
        for txn in txn_list:
            res.append({
                'date': arrow.get(txn['date'], self.timeframe_format),
                'amount': float(txn['amount']),
                'merchant': txn['payee'],
                'category': txn['category_name'],
                'description': txn['notes'],
                'source': "manual" if txn['source'] == 'manual' else txn["asset_display_name"],
                'tags': set([StatisticServiceFilter(tag["name"]) for tag in txn["tags"]]),
                # TODO(07/04/2024) - add "location" when lunch money adds it to API
            })
        return res
