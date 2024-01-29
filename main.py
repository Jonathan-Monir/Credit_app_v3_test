from contract import Contract
import price_cost
import invoice
from file_uploader import FileUploader
import sqlite3
import streamlit as st
import pandas as pd


import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

df = FileUploader(r"test files\test.xlsx")
df.final_dict['contracts_activity'] = df.contracts_activity
print(df.final_dict.keys())

# df.final_dict['statment'].to_excel('output_file.xlsx', index=False)