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
df.final_dict['contracts_activity'] = df.contracts_activity
df_dict = df.final_dict
# print(df.final_dict.keys())
# df.final_dict['statment'].to_excel('output_file.xlsx', index=False)
statment = df_dict['statment']
contract = df_dict['contract']
invoice = Invoice().oneContractDates(statment.iloc[0,:],contract)