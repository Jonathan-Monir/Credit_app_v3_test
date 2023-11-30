from contract import Contract
import price_cost
import invoice
from file_uploader import FileUploader
import sqlite3
import streamlit as st
import time

uploader = FileUploader('test files\Biblio- Siva.xlsx')

contract_sheets = uploader.contract_sheets
statment_sheet = uploader.statment
Contracts = {key: Contract(value) for key, value in contract_sheets.items()}
    
print(statment_sheet.columns)