from invoice import Invoice
from file_uploader import FileUploader
import sqlite3
import pandas as pd

import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

df = FileUploader(r"test files\test.xlsx")
statment = df.statment

main_contract = df.contracts_sheets['contract']
contracts_sheets = df.contracts_sheets
prices = Invoice(statment,contracts_sheets,df.contracts_activity).prices
date_prices = Invoice(statment,contracts_sheets,df.contracts_activity).Index_contract_date_range_dict


statment.loc[prices.keys(), "Total price"] = [round(price, 2) for price in list(prices.values())]



statment.to_excel("output.xlsx", index=False)