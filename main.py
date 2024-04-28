"""
This script merges PDF files into one CSV
"""
from enum import Enum
from functools import reduce
from io import TextIOWrapper
from pathlib import Path
import glob
import os

import pandas as pd
import tabula
from loguru import logger

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

def find_transactions_table(pdf_file: TextIOWrapper) -> pd.DataFrame:
    company: Company = get_company(pdf_file)
    tables = tabula.read_pdf(pdf_file, pages='all')
    logger.critical(pdf_file)
    for table in tables:
        logger.info("\n" + str(table))
    logger.info(type(tables[0]))
    return tables[0]

def normalize_transaction_df(df: pd.DataFrame) -> pd.DataFrame:
    company: Company = get_company(pdf_file)
    return df

#=================
#   MAIN
#=================

df_list: list[pd.DataFrame] = []

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