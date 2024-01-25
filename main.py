from contract import Contract
import price_cost
import invoice
from file_uploader import FileUploader
import sqlite3
import streamlit as st

df = FileUploader(r"test files\shift_down_test.xlsx")

print(df.final_df)

