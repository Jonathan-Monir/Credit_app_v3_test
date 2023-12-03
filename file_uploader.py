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
    
    def insert_key_after(self):
        # Create a new OrderedDict
        all_indices = []

        # Iterate through the original OrderedDict
        for key, contract in self.contract_sheets.items():
            
            compared_contract = contract.copy()
            compared_contract['first date'] = contract['first date'].shift(-1)
            
            compared_contract = compared_contract.drop(compared_contract.index[-1])
            
            compared_contract['days'] = abs((compared_contract['first date'] - compared_contract['second date']).dt.days)
            if key == "spo 12.7":
                pass
            indices = compared_contract[compared_contract['days'] > 1].index.tolist()
            if len(indices) > 0:
                
                for i in range(len(indices)):
                    if i == 0:
                        cut_contract = contract.iloc[:indices[i]+1]
                        
                    if i == len(indices) - 1:
                        cut_contract = contract.iloc[indices[i]+1:]
                        
                    else:
                        cut_contract = contract.iloc[indices[i]+1:indices[i+1]+1]
                        
            all_indices.append(indices)
        return all_indices