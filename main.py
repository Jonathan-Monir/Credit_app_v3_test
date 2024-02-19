from invoice import Invoice
from file_uploader import FileUploader
import sqlite3
import pandas as pd
from contract import Contract
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

def make_contracts_dict(contracts_sheets,contract_activity):
        offers_dict = {}
        for contract_name, contract_data in contracts_sheets.items():
            offers_dict[contract_name] = Contract(contract_name, contract_data, contract_activity[contract_name])
        return offers_dict

df = FileUploader(r"test files\test2.xlsx")
statment = df.statment


contracts_sheets = df.contracts_sheets

offers_dict = make_contracts_dict(contracts_sheets,df.contracts_activity)

invoice = Invoice(df,offers_dict)

prices = Invoice(df,offers_dict).prices
date_prices = Invoice(df,offers_dict).Index_contract_date_range_dict

statment.loc[prices.keys(), "Total price"] = [round(price, 2) for price in list(prices.values())]


# statment.to_excel("output.xlsx", index=False)
