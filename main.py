from contract import Contract
from price_cost import Calculate
from invoice import Invoice
from file_uploader import FileUploader
import sqlite3
import streamlit as st
import pandas as pd


import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

df = FileUploader(r"test files\test.xlsx")
statment = df.statment

main_contract = df.contracts_sheets['contract']
contracts_sheets = df.contracts_sheets
prices = Invoice(statment,contracts_sheets,df.contracts_activity).invoicesMetrices()
print(prices)