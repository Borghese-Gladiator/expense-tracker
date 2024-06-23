import os
from dotenv import load_dotenv

load_dotenv()

LUNCH_MONEY_ACCESS_TOKEN = os.getenv('LUNCH_MONEY_API_KEY')