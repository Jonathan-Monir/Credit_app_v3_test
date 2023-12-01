from contract import Contract
from file_uploader import FileUploader
import pandas as pd

uploader = FileUploader('test files\Biblio- Siva.xlsx')
contract_sheets = uploader.contract_sheets
Contracts = {key: Contract(value) for key, value in contract_sheets.items()}
class InvoiceMapping:
    def __init__(self, statment):
        self.statment =  statment
        self.reservation_date = statment["Res_date"]
        self.Arrival = statment["Arrival"]
        self.Departure = statment["Departure"]
        self.valid_contracts = self.validate_contract()
        
    def validate_contract(self):
        validity_condition = {
            key: (contract.start_date <= self.statment['Res_date']) & (self.statment['Res_date'] <= contract.end_date)
            for key, contract in Contracts.items()
        }

        return pd.DataFrame(validity_condition)
        