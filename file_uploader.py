
import pandas as pd
import numpy as np
class FileUploader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.final_dict = self.fix_file()[0]
        self.contracts_activity = self.fix_file()[1]
        self.num_rows = self.final_dict["statment"].shape[0]

    def to_df(self):
        # convert to excel
        excel_data = pd.read_excel(self.filepath, sheet_name=None)

        return excel_data

    def fix_empty(self, df, column):
        # get df that has empty rows
        df.loc[(df[column].isnull() | (df[column] == '')),column] = np.nan

        # get rows with nulls
        empty_rows = df[column].isna()
        
        # set activity of rows to 0
        df.loc[empty_rows, "activity"] = 0
        if "error_type" in df.columns:
            # type error in error type column
            if not df.loc[empty_rows, "error_type"].empty:
                df.loc[empty_rows, "error_type"] += f", empty in {column}"
            else:
                df.loc[empty_rows, "error_type"] = f"empty in {column}"
        return df

    def fix_date(self, df_date_fix, column):
        
        # classify error in date to nulls
        df_date_fix["date_check"] = pd.to_datetime(df_date_fix[column], errors="coerce")
        df_date_fix.loc[df_date_fix['date_check'].dt.year < 2012, 'date_check'] = np.nan

        # Identify rows with date errors and set "activity" to 0
        error_rows = df_date_fix["date_check"].isna()
        df_date_fix.loc[error_rows, "activity"] = 0

        if "error_type" in df_date_fix.columns:
            if not df_date_fix.loc[error_rows, "error_type"].empty:
                df_date_fix.loc[error_rows, "error_type"] += f", Date error in {column}"
            else:
                df_date_fix.loc[error_rows, "error_type"] = f"Date error in {column}"

        df_date_fix.drop("date_check", axis = 1, inplace = True)
        
        return df_date_fix

    def fix_numbers(self, statment_fix, columns_to_fix):
        for column in columns_to_fix:
            try:
                statment_fix["numeric_check"] = pd.to_numeric(statment_fix[column])
            except ValueError:
                # Identify rows with numeric errors and set "activity" to 0
                error_rows = pd.to_numeric(statment_fix[column], errors="coerce").isna()
                statment_fix.loc[error_rows, "activity"] = 0

                # Append the error_type with the column name
                if "error_type" in statment_fix.columns:
                    statment_fix.loc[error_rows, "error_type"] += f", Numeric error in {column}"
                else:
                    statment_fix.loc[error_rows, "error_type"] = f"Numeric error in {column}"
            
            statment_fix.drop("date_check", axis = 1, inplace = True)

        return statment_fix

    def fix_overlap(self, df):
        for sheet_name, sheet_data in df.items():
            if sheet_name != "statment":
                for row_index in range(len(sheet_data['second date'])-1):
                    if abs(sheet_data['second date'].iloc[row_index] - sheet_data['first date'][row_index+1]).days > 1:
                        # print(sheet_data.iloc[:row_index+1,:])
                        pass
    
    def check_statment(self, statment):

        if "Arrival" not in statment.iloc[0] or "Departure" not in statment.iloc[0]:

            # Identify the row where the column names are located
            header_row = statment[statment.apply(lambda row: row.notnull().all(), axis=1)].index[0]

            # Use the identified row as the header
            statment.columns = statment.iloc[header_row]
            statment = statment.drop(header_row)

            # Drop the null rows and reset the index
            statment = statment.dropna().reset_index(drop=True)
        
        
        columns_emtpy_to_fix = ["Rate code"]
        for column in columns_emtpy_to_fix:
            self.fix_empty(statment, column)

        columns_dates_to_fix = ["Res_date","Arrival","Departure"]
        for column in columns_dates_to_fix:
            statment = self.fix_date(statment, column)

        # columns_numeric_to_fix = ["Amount-hotel","Currency rate","Departure"]
        # statment = self.fix_numbers(statment, columns_numeric_to_fix)
        
        return statment

    def check_contract(self, df):
        
        contracts_activity = dict()

        for sheet_name, sheet_data in df.items():
            if sheet_name != "statment":
                
                columns_dates_to_fix = ["first date","second date"]
                for column in columns_dates_to_fix:
                    contract = self.fix_date(sheet_data, column)

                active = ~(contract["activity"] == 0).any()
                df[sheet_name], contracts_activity[sheet_name] = contract, active

        self.fix_overlap(df)
        return df, contracts_activity
    
    def fix_file(self):
        
        df = self.to_df()
        
        df["statment"]["activity"] = 1
        df["statment"]["error_type"] = ""


        for sheet_name, sheet_data in df.items():
            df[sheet_name] = sheet_data.dropna(axis=1, how="all")
            df[sheet_name]["activity"] = 1
            df[sheet_name]["error_type"] = ""

        df["statment"] = self.check_statment(df["statment"])

        contracts_activity = {sheet_name: 1 for sheet_name, sheet_data in df.items() if sheet_name != "statment"}
        
        df, contracts_activity = self.check_contract(df)

        return df, contracts_activity

    