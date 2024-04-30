"""
This script merges PDF files into one CSV
"""
from dataclasses import asdict, dataclass
from enum import Enum
from functools import reduce
from io import TextIOWrapper
from pathlib import Path
from typing import Any, Callable, List
import glob
# import itertools  ## itertools.chain
import re

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

# data format utils
@dataclass
class Transaction:
    date: str
    merchant_name: str
    location: str
    price: float
    company: str

class Document(Enum):
    CAPITAL_ONE = "capital_one"
    CAPITAL_ONE_YEARLY_SUMMARY = "capital_one_yearly_summary_"
    CHASE = "chase"
    DISCOVER = "discover"
    FIDELITY = "fidelity"

def get_document_type(filename) -> Document:
    filename_lower = filename.lower()
    for company in Document:
        if company.value.lower() in filename_lower:
            return company
    return None

# regex utils
def clean_raw_str(value):
    return re.sub(r'[^0-9.-]', '', value)  # Remove all characters except digits, minus sign, and decimal point
def clean_replace_multiple_spaces(text):
    return re.sub(r'\s+', ' ', text) # Use a regular expression to replace multiple spaces with a single space


#=================
#   MAIN
#=================

def get_doc_parse_func(company: Document):
    def parse_capital_one_yearly(cell_list: list[str]) -> list[Transaction]:
        headers = ['Date', 'Merchant Name', 'Merchant Location', 'Price']
        raw_tx_list_1: list[str] = cell_list[cell_list.index('Card Ending in 1496') + 1:cell_list.index('TOTAL CHARGES')]
        raw_tx_list_2: list[str] = cell_list[cell_list.index('Card Ending in 4449') + 1:cell_list.index('TOTAL CHARGES')]
        raw_tx_list = raw_tx_list_1 + raw_tx_list_2
        
        logger.debug("START parsing capital_one_yearly")
        tx_list = []
        for idx in range(0, len(raw_tx_list), 4):
            logger.info(raw_tx_list[idx:idx+4])
            tx = Transaction(
                date=raw_tx_list[idx + 0],
                merchant_name=raw_tx_list[idx + 1],
                location=clean_replace_multiple_spaces(raw_tx_list[idx + 2]),
                price=float(clean_raw_str(raw_tx_list[idx + 3])),
                company=company.value
            )
            logger.info(tx)
            tx_list.append(tx)
        logger.debug(f"FINISH parsing capital_one_yearly for {len(tx_list)} transactions")
        return tx_list
        
    company_parse_dict: dict[Document, Callable[[list[str]], list[Transaction]]] = {
        Document.CAPITAL_ONE: parse_capital_one_yearly,
    }
    return company_parse_dict[company]


def get_doc_page_numbers(doc: Document) -> list[int]:
    doc_page_num_dict: dict[Document, list[int]] = {
        Document.CAPITAL_ONE: [9, 10],
    }
    return doc_page_num_dict[doc]


def build_transactions_table(pdf_file: TextIOWrapper) -> list[Any]:
    reader = PdfReader(pdf_file)
    doc_type = get_document_type(pdf_file)
    parse_func = get_doc_parse_func(doc_type)
    page_num_list = get_doc_page_numbers(doc_type)
    
    logger.info(f"START building transactions for {pdf_file}")
    tx_list = []
    for page_num in page_num_list:
        logger.debug(f"test: {page_num}")
        page = reader.pages[page_num - 1]  # NOTE: -1 accounts for 0 based index compared to PDF which has 1 based index
        raw_text_list = page.extract_text().split('\n')
        tx_list += parse_func(raw_text_list)
    df = pd.DataFrame([asdict(tx) for tx in tx_list])
    logger.info(f"FINISH building transactions for {pdf_file}")
    return df


df_list: List[pd.DataFrame] = []

pdf_files = glob.glob(f'{INPUT_FOLDER}/*.pdf')
for pdf_file in pdf_files:
    try:
        pdf_file = "financial_transaction_history/capital_one_yearly_summary_Smry_2023_1496.pdf"
        df = build_transactions_table(pdf_file)
        df_list.append(df)
    except Exception as e:
        logger.error(e)
    break
    # Append extracted transactions to the DataFrame
    # all_transactions = all_transactions.append(transactions, ignore_index=True)

# Normalize the data (cleaning, formatting, etc.)
# Example: Convert 'Date' column to datetime format
# all_transactions['Date'] = pd.to_datetime(all_transactions['Date'], errors='coerce')

df_merged = reduce(lambda left, right: pd.merge(left, right, on=['DATE'], how='outer'), df_list)
df_merged.to_csv(OUTPUT_FILE, index=False)

logger.info("FINISHED expense aggregation!")