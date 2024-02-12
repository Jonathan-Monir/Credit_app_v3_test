from tkinter import *
import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import Scrollbar

class SetupContract(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        self.canvas = tk.Canvas(self, background="red", scrollregion=(0,0,self.winfo_width(),800))
        self.canvas.pack(expand=True, fill='both')

        self.contract_setting = ContractSetting(self)
        ttk.Label(self.contract_setting).pack()
        self.canvas.create_window((-1,0), window = self.contract_setting, anchor='nw', width=self.winfo_width(), height=270)
        
        # events
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60),'units'))
        self.bind('<Configure>', self.update_size)

    def update_size(self, event):
        self.canvas.create_window((-1,0), window = self.contract_setting, anchor='nw', width=self.winfo_width(), height=270)
        

class ExcelFileBrowserApp:
    def __init__(self, root):
        
        self.root = root

    
class ContractSetting(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)


        self.pack(expand=True,fill='both')
        ExcelFileBrowserApp(self)
