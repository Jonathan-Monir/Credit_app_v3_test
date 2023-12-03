import time
from contract import Contract
import price_cost
from invoice import InvoiceMapping
from file_uploader import FileUploader
import sqlite3
import streamlit as st
start_time = time.time()


uploader = FileUploader('test files\Biblio- Resort 23-24 - Copy.xlsx')

contract_sheets = uploader.contract_sheets
Contracts = {key: Contract(value) for key, value in contract_sheets.items()}
statment_sheet = uploader.statment
print(InvoiceMapping(statment_sheet, Contracts).test)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
