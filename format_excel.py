import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import openpyxl
import xlsxwriter
from openpyxl.utils.dataframe import dataframe_to_rows



class FormatExcel:
    
    def __init__(self, df, output_file_path=None, columns=None):
        self.df = df.copy()  # Create a copy to avoid modifying the original DataFrame
        self.output_file_path = output_file_path
        self.columns = columns
        self.apply_format()

    def apply_format(self):
        if self.output_file_path:
            writer = pd.ExcelWriter(self.output_file_path, engine='openpyxl')
            self.df.to_excel(writer, sheet_name="Sheet1")
            workbook = xlsxwriter.Workbook(self.output_file_path)
            worksheet = workbook.add_worksheet()
            writer.save()
            
            # self.color_difference()
        
    def color_difference(self):
        
        format3 = self.workbook.add_format({
                'num_format': '0.00',
                'bg_color': 'FFFF00',
                'font_size': 15,   
                'bold': True,
                'font_name': 'Times New Roman',
                'left': 6,
                'right': 6,  # 1 means a solid border
                'bottom': 2,
                'align': 'center',
                'valign': 'vcenter'
            })

        num_rows = self.df.shape[0]
        num_cols = self.df.shape[1]

        # for row in range(1, num_rows + 1):  # Loop through rows (skip header)
        #     for col in range(num_cols):  # Loop through columns
        #         cell = self.worksheet.cell(row=row, column=col + 1)  # Get cell
        #         cell.font = openpyxl.styles.Font(bold=True, color='FF0000')

        for row in range(num_rows):
                for col in range(num_cols):
                    cell_value = df.iat[row, col]
                    if pd.notna(cell_value):  # Check if the cell contains any value
                        self.worksheet.write(row, col, cell_value, format3)

df = pd.read_excel(r"output\aBiblio- Resort 23-24.xlsx_output.xlsx")

# Specify the columns you want to highlight
columns_to_highlight = ['Difference']

FormatExcel(df, "output_file.xlsx", columns=columns_to_highlight)
