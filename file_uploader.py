import pandas as pd
import openpyxl

class FileUploader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.sheet_names = self.get_sheet_names()
        self.statment = self.to_statment()
        self.contract_sheets = self.to_sheets()
        
    def fix_file(df):
        pass
    
    def to_df(self, sheet_name):
        excel_file_path = self.filepath
        if not excel_file_path.endswith('.xlsx'):
            raise ValueError("File must have a '.xlsx' extension.")
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        return df
    
    def to_statment(self):
        
        try:
            return self.to_df("statment")
        except Exception as e:
            print("could not find statment sheet")
        
    def to_sheets(self):
        if self.sheet_names is None:
            raise ValueError("Sheet names are not available.")
        
        cleaned_sheet_names = [sheet for sheet in self.sheet_names if sheet != "statment"]
        
        contract_sheets = {contract: self.to_df(contract) for contract in cleaned_sheet_names}
            
        return contract_sheets
    
    def get_sheet_names(self):
        try:
            workbook = openpyxl.load_workbook(self.filepath)
            sheet_names = workbook.sheetnames
            workbook.close()

            return sheet_names

        except Exception as e:
            print(f"Error in reading sheet names: {e}")
            return None