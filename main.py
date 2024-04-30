"""
This script merges PDF files into one CSV
"""
from enum import Enum
from functools import reduce
from io import TextIOWrapper
from pathlib import Path
from typing import Any, List
import glob
import os

from pypdf import PdfReader
from loguru import logger
import pandas as pd

#=================
#   CONSTANTS
#=================
INPUT_FOLDER = Path('financial_transaction_history')
OUTPUT_FILE = Path('normalized_transactions.csv')


#=================
#   UTILS
#=================

# logging
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS zz}</green> | <level>{level: <8}</level> | <yellow>Line {line: >4} ({file}):</yellow> <b>{message}</b>"
logger.add("file.log", format=log_format, colorize=False, backtrace=True, diagnose=True)

# dataclass
# Transaction

# company enum
class Company(Enum):
    CAPITAL_ONE = "capital_one"
    CHASE = "chase"
    DISCOVER = "discover"
    FIDELITY = "fidelity"
def get_company(filename) -> Company:
    filename_lower = filename.lower()
    for company in Company:
        if company.value.lower() in filename_lower:
            return company
    return None
def get_headers(company: Company) -> list[str]:
    headers_dict: dict[Company, list[str]] = {
        Company.CAPITAL_ONE: ['Date', 'Merchant Name', 'Merchant Location', 'Price'],
    }
    return headers_dict[company]
        

def find_transactions_table(pdf_file: TextIOWrapper) -> list[Any]:
    company = get_company(pdf_file)
    headers = get_headers(company)
    
    reader = PdfReader(pdf_file)
    number_of_pages = len(reader.pages)
    page = reader.pages[9]
    text_list = page.extract_text().split('\n')
    
    logger.critical(pdf_file)
    transaction_list_1 = text_list[text_list.index('Card Ending in 1496') + 1:text_list.index('TOTAL CHARGES')]
    transaction_list_2 = text_list[text_list.index('Card Ending in 4449') + 1:text_list.index('TOTAL CHARGES')]
    
    tx_list = []
    for idx in range(0, len(transaction_list_1), 4):
        transaction = tuple(transaction_list_1[idx:idx+4])
        tx_list.append(transaction)
        # 0 4 04/24
        # 1 5 MARKET BASKET 00000729
        # 2 6 WESTFORD     MA
        # 3 7 $49.69
    logger.info(tx_list)
    # pd.Series(["04/24"], index=[
    #     "Date",
    #     "Merchant Name",
    #     "Merchant Location",
    #     "Prices"
    # ])
    df = pd.DataFrame(tx_list, columns=headers)
    logger.info(df.head())
    logger.info('\n' + df['Date'])
    
    # logger.info()
    # logger.info(str(text))
    # tables = camelot.read_pdf(pdf_file)
    # logger.critical(pdf_file)
    # for table in tables:
    #     logger.info("\n" + str(table))
    # logger.info(type(tables[0]))
    return tx_list

def normalize_transaction_df(df: pd.DataFrame) -> pd.DataFrame:
    company: Company = get_company(pdf_file)
    return df

#=================
#   MAIN
#=================

df_list: List[pd.DataFrame] = []

pdf_files = glob.glob(f'{INPUT_FOLDER}/*.pdf')
for pdf_file in pdf_files:
    try:
        df = find_transactions_table(pdf_file)
        df = normalize_transaction_df(df)
        df_list.append(df)
    except Exception as e:
        logger.error(e)
    break
    # Append extracted transactions to the DataFrame
    # all_transactions = all_transactions.append(transactions, ignore_index=True)

# Normalize the data (cleaning, formatting, etc.)
# Example: Convert 'Date' column to datetime format
# all_transactions['Date'] = pd.to_datetime(all_transactions['Date'], errors='coerce')

df_merged = reduce(lambda left,right: pd.merge(left, right, on=['DATE'], how='outer'), df_list)
df_merged.to_csv(OUTPUT_FILE, index=False)

logger.info("FINISHED expense aggregation!")