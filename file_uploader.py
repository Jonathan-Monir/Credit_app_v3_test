
import pandas as pd

class FileUploader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.final_df = self.complete_dataframe()
        self.num_rows = self.final_df.shape[0]

    def to_df(self):

        df = pd.read_excel(self.filepath)
        return df

    def fix_file(self, df):
        df = df.dropna(axis=1, thresh = df.shape[0]/4)

        if 'Arrival' not in df.iloc[0] or 'Departure' not in df.iloc[0]:

            # Identify the row where the column names are located
            header_row = df[df.apply(lambda row: row.notnull().all(), axis=1)].index[0]

            # Use the identified row as the header
            df.columns = df.iloc[header_row]
            df = df.drop(header_row)

            # Drop the null rows and reset the index
            df = df.dropna().reset_index(drop=True)

        return df

    def test_statment(df):
        pass

    def test_contract(df):
        pass
    
    def complete_dataframe(self):
        
        df = self.to_df()
        df_cleaned = self.fix_file(df)

        return df_cleaned