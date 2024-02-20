from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilenames
import pandas as pd
from tkinter import Scrollbar
from file_uploader import FileUploader
from tkcalendar import Calendar, DateEntry
from PIL import Image, ImageTk
from contract import Contract
import sqlite3
from datetime import datetime
from invoice import Invoice
import os


global_setup_name = "" 

class MainFrame(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")
        
        global container
        container = []
        self.canvas = tk.Canvas(self, background="#F68497", scrollregion=(0,0,self.winfo_width(),800))
        self.canvas.pack(expand=True, fill='both')

        self.welcome = Welcome(self)
        ttk.Label(self.welcome).pack()
        self.canvas.create_window((-1,0), window = self.welcome, anchor='nw', width=self.winfo_width(), height=270)
        
        # events
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60),'units'))
        self.bind('<Configure>', self.update_size)

    def update_size(self, event):
        self.canvas.create_window((-1,0), window = self.welcome, anchor='nw', width=self.winfo_width(), height=270)
        

class ExcelFileBrowserApp:
    def __init__(self, root):
        
        self.root = root
        self.files = []

        self.list_frame = tk.Frame(root)
        self.list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.list_frame, text="Selected Files:")
        self.label.pack()

        self.scrollbar = Scrollbar(self.list_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.list_frame, selectmode=tk.MULTIPLE, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X)

        self.browse_button = tk.Button(self.buttons_frame, text="Browse", command=self.browse_files)
        self.browse_button.pack(side=tk.LEFT)
        

        self.remove_button = tk.Button(self.buttons_frame, text="Remove Selected", command=self.remove_selected_files)
        self.remove_button.pack(side=tk.LEFT)

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Excel Files", "*.xlsx *.xls")])
        for file_path in file_paths:
            self.files.append(file_path)
            self.listbox.insert(tk.END, file_path.split('/')[-1])
            
        global container
        container =  [FileUploader(file_path) for file_path in self.files]
        print(len(container), "Successfully installer")
    def remove_selected_files(self):
        selected_indices = self.listbox.curselection()
        for i in selected_indices[::-1]:  # Reversing the list to avoid shifting indexes
            self.listbox.delete(i)
            del self.files[i]
            del container[i]
            

class Welcome(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)


        self.pack(expand=True,fill='both')
        ExcelFileBrowserApp(self)

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################







class SetupContract(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        self.canvas = tk.Canvas(self, background="red", scrollregion=(0,0,self.winfo_width(),20000))
        self.canvas.pack(expand=True, fill='both')

        self.contract_setting = ContractSetting(self)
        
        # self.canvas.create_window((-1,0), window = self.contract_setting, anchor='nw', width=self.winfo_width(), height=20000)
        
        self.scrollbar = ttk.Scrollbar(self, orient= "vertical",command=self.canvas.yview)
        self.scrollbar.place(relx=1,rely=0,relheight=1,anchor='ne')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # events
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60),'units'))
        self.bind('<Configure>', self.update_size)

        self.container = container
        

    def update_size(self, event):
        self.canvas.create_window((-1,0), window = self.contract_setting, anchor='nw', width=self.winfo_width(), height=20000)
        
    
class ContractSetting(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.pack(expand=True,fill='both')

        self.name_contract_dict = {contract.filename:contract for contract in container}
        self.current_file = None
        

        
        tk.Label(self, text="choose setup file", font=("Helvetica", 10, "underline")).grid(row=0, column=0, sticky="w", padx=5, pady=10)
        
        self.setup_file = tk.Listbox(self, listvariable=tk.StringVar(value=[file.filename for file in container]))
        self.setup_file.bind('<Double-1>', self.refresh_page)   # Bind to selection event
        self.setup_file.grid(row=1, column=0, sticky="w", padx=5, pady=10,rowspan=8)  # Corrected this line
        
        self.contract_frame = ContractFrame(self)
        self.contract_frame.grid(column = 0, columnspan=2)

    def refresh_page(self, event):
        self.contract_frame.destroy()
        self.current_file = self.name_contract_dict[self.setup_file.get(self.setup_file.curselection()[0])]
        self.contract_frame = ContractFrame(self, self.current_file)
        self.contract_frame.grid(column = 0, columnspan=2)

# import tkinter as tk
from tkinter import messagebox

class ContractFrame(tk.Frame):
    def __init__(self, master=None, current_file=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        if not current_file:
            
            tk.Label(self, text="Please choose a file to make the setup", font=("Helvetica", 24)).grid(row=0, column=0, sticky="w", padx=0, pady=0)

        else:

            tk.Label(self, text="Setup name", font=("Helvetica", 10, "underline")).grid(row=1, column=0, sticky="w", padx=0, pady=0)
            self.setup_name = tk.Text(self, height = 1, width = 15)
            self.setup_name.grid(row=2, column=0, sticky="w", padx=5, pady=10)


            self.current_file = current_file
            #down
            pathtophoto = Image.open(r"images\RD.png").resize((25,25))
            Down = ImageTk.PhotoImage(pathtophoto)
            panel1 = Label(self, image=Down)
            panel1.image = Down #keep a reference

            #up
            pathtophoto = Image.open(r"images\RU.png").resize((25,25))
            Up = ImageTk.PhotoImage(pathtophoto)
            panel1 = Label(self, image=Up)
            panel1.image = Up #keep a reference

            #up
            pathtophoto = Image.open(r"images\Delete.png").resize((25,25))
            Delete = ImageTk.PhotoImage(pathtophoto)
            panel1 = Label(self, image=Delete)
            panel1.image = Delete #keep a reference

            max_iter = len(current_file.contracts_sheets)
            rank = 1 

            statment_columns = current_file.statment.columns
            self.entries_dict = {}
            
            
            
            # self.combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)
            tk.Label(self, text="change setup", font=("Helvetica", 10, "underline")).grid(column=0, sticky="w", padx=0, pady=0)
            self.initialize_with_setup = ttk.Combobox(self, values=list(ApplySetup.get_tables(self).keys()))
            self.initialize_with_setup.grid(column=0, sticky="w", padx=5, pady=10)
            
            for contract_name, contract_sheet in current_file.contracts_sheets.items():
                self.entries_dict[contract_name] = create_widgets(self, contract_name=contract_name, contract_sheet=contract_sheet, rank=rank, max_iter=max_iter, Down=Down, Up=Up, Delete=Delete, statment_columns=statment_columns)
                self.entries_dict[contract_name].grid(pady=20)
                rank+=1
            
            # self.reductions = {}
            # for prop in ["enable","amount","column"]:
            #     if prop == "enable":
            #         self.reductions["rwa " + prop] = tk.BooleanVar()
            #         self.reductions["rwp " + prop] = tk.BooleanVar()
            #         self.reductions["ewa " + prop] = tk.BooleanVar()
            #     if prop == "amount":
            #         self.reductions["rwa " + prop] = tk.Entry()
            #         self.reductions["rwp " + prop] = tk.Entry()
            #         self.reductions["ewa " + prop] = tk.Entry()

            # # reduction amount
            # tk.Label(self, text="Reduction with amount", font=("Helvetica", 10, "underline")).grid(row=100, column=0, sticky="w", padx=5, pady=5)

            # tk.Label(self, text="Enable").grid(row=101, column=0, sticky="w", padx=5, pady=5)
            # tk.Checkbutton(self, variable=self.reductions["rwa enable"]).grid(row=101, column=1, sticky="w", padx=5, pady=5)

            # tk.Label(self, text="amount").grid(row=102, column=0, sticky="w", padx=5, pady=5)
            # self.reductions["rwa amount"].grid(row=102, column=1, sticky="w", padx=5, pady=5)

            # tk.Label(self, text="column").grid(row=102, column=2, sticky="w", padx=5, pady=5)
            # self.reductions["rwa column"] = ttk.Combobox(self, values=list(statment_columns))
            # self.reductions["rwa column"].grid(row=102, column=3)
            
            # # reduction percentage
            # tk.Label(self, text="Reduction with percentage", font=("Helvetica", 10, "underline")).grid(row=103, column=0, sticky="w", padx=5, pady=5)

            # tk.Label(self, text="Enable").grid(row=104, column=0, sticky="w", padx=5, pady=5)
            # tk.Checkbutton(self, variable=self.reductions["rwp Enable"]).grid(row=104, column=1, sticky="w", padx=5, pady=5)

            # tk.Label(self, text="percentage").grid(row=105, column=0, sticky="w", padx=5, pady=5)
            # self.reductions["rwp amount"].grid(row=105, column=1, sticky="w", padx=5, pady=5)

            # tk.Label(self, text="column").grid(row=106, column=2, sticky="w", padx=5, pady=5)
            # self.reductions["rwp Column"] = ttk.Combobox(self, values=list(statment_columns))
            # self.reductions["rwp Column"].grid(row=106, column=3)
            
            # extra amount
            # tk.Label(self, text="Reduction 1", font=("Helvetica", 10, "underline")).grid(row=107, column=0, sticky="w", padx=5, pady=5)

            # tk.Label(self, text="Enable").grid(row=108, column=0, sticky="w", padx=5, pady=5)
            # tk.Checkbutton(self, variable=self.entries["Reduc1 Enable"]).grid(row=108, column=1, sticky="w", padx=5, pady=5)

            # tk.Label(self, text="Reduction 1 percentage").grid(row=109, column=0, sticky="w", padx=5, pady=5)
            # self.entries["Reduc1 Percentage"].grid(row=109, column=1, sticky="w", padx=5, pady=5)

            # tk.Label(self, text="Reduction 1 column").grid(row=109, column=2, sticky="w", padx=5, pady=5)
            # self.entries["Reduc1 Column"] = ttk.Combobox(self, values=list(statment_columns))
            # self.entries["Reduc1 Column"].grid(row=109, column=3)

            # Button
            self.submit_button = tk.Button(self, text="Submit", command=self.submit)
            self.submit_button.grid(columnspan=2, pady=10)
            

    def save_to_database(self, all_offer_contract_dict):
        # Connect to the SQLite database
        conn = sqlite3.connect('setups.db')
        c = conn.cursor()
        
        # Create a table to store the data

        # Insert data into the table
        for offer_name, offer_data in all_offer_contract_dict.items():
            c.execute(f'''CREATE TABLE IF NOT EXISTS {offer_name}
                (contract_name TEXT PRIMARY KEY,
                offer_name TEXT,
                offer_data TEXT,
                eb1_enable BOOLEAN,
                eb1_percentage REAL,
                eb1_date DATE,
                eb2_enable BOOLEAN,
                eb2_percentage REAL,
                eb2_date DATE,
                reduc1_enable BOOLEAN,
                reduc1_percentage REAL,
                reduc1_column TEXT,
                reduc2_enable BOOLEAN,
                reduc2_percentage REAL,
                reduc2_column TEXT,
                lt_enable BOOLEAN,
                lt_percentage REAL,
                lt_days INTEGER,
                senior_enable BOOLEAN,
                senior_percentage REAL,
                senior_column TEXT,
                combinations_eb_lt TEXT,
                combinations_eb_reduc TEXT,
                combinations_eb_senior TEXT,
                start_date DATE,
                end_date DATE,
                active INTEGER)''')
            for contract_name, contract_data in offer_data.items():
                eb1_enable = contract_data["eb1"]["enable"]
                eb1_percentage = contract_data["eb1"]["percentage"]
                eb1_date = contract_data["eb1"]["date"]
                
                eb2_enable = contract_data["eb2"]["enable"]
                eb2_percentage = contract_data["eb2"]["percentage"]
                eb2_date = contract_data["eb2"]["date"]
                
                reduc1_enable = contract_data["reduc1"]["enable"]
                reduc1_percentage = contract_data["reduc1"]["percentage"]
                reduc1_column = contract_data["reduc1"]["column"]
                
                reduc2_enable = contract_data["reduc2"]["enable"]
                reduc2_percentage = contract_data["reduc2"]["percentage"]
                reduc2_column = contract_data["reduc2"]["column"]
                
                lt_enable = contract_data["lt"]["enable"]
                lt_percentage = contract_data["lt"]["percentage"]
                lt_days = contract_data["lt"]["days"]
                
                senior_enable = contract_data["senior"]["enable"]
                senior_percentage = contract_data["senior"]["percentage"]
                senior_column = contract_data["senior"]["column"]
                
                start_date = contract_data["start_date"]
                end_date = contract_data["end_date"]

                combinations_eb_lt = contract_data["combinations"]["eb_lt"]
                combinations_eb_recuc = contract_data["combinations"]["eb_reduc"]
                combinations_eb_senior = contract_data["combinations"]["eb_senior"]
                
                c.execute(f"INSERT INTO {offer_name} (offer_name, contract_name, offer_data, eb1_enable, eb1_percentage, eb1_date, eb2_enable, eb2_percentage, eb2_date, reduc1_enable, reduc1_percentage, reduc1_column, reduc2_enable, reduc2_percentage, reduc2_column, lt_enable, lt_percentage, lt_days, senior_enable, senior_percentage, senior_column, combinations_eb_lt, combinations_eb_reduc, combinations_eb_senior, start_date, end_date, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (offer_name, contract_name, str(contract_data), eb1_enable, eb1_percentage, eb1_date, eb2_enable, eb2_percentage, eb2_date, reduc1_enable, reduc1_percentage, str(reduc1_column), reduc2_enable, reduc2_percentage, str(reduc2_column), lt_enable, lt_percentage, lt_days, senior_enable, senior_percentage, str(senior_column), combinations_eb_lt, combinations_eb_recuc, combinations_eb_senior, start_date, end_date, 1))

        # Commit changes and close the connection
        conn.commit()
        conn.close()
      
    def submit(self):
        contract_params = {}
        global global_setup_name

        eb1 = {"enable":False,"percentage":0,"date":pd.to_datetime("01/11/2026")}
        eb2 = {"enable":False,"percentage":0,"date":pd.to_datetime("01/11/2026")}
        lt = {"enable":False,"percentage":0,"days":0}
        senior = {"enable":False,"column":"","percentage":0}
        reduc1 = {"enable":False,"column":"","percentage":0}
        reduc2 = {"enable":False,"column":"","percentage":0}
        extra = {"enable":False,"amount":0}
        combinations = {"eb_lt":False,"eb_reduc":False}

        start_date = {"date":pd.to_datetime("01/11/2026")}
        end_date = {"date":pd.to_datetime("01/11/2026")}
        
        self.contract_activities = self.current_file.contracts_activity
        
        all_offer_contract_dict = {}
        
        offers_per_contract = {}
        for contract_name, contract_sheet in self.current_file.contracts_sheets.items():
            offers = {}
            eb1 = {}
            eb2 = {}
            lt = {}
            senior = {}
            reduc1 = {}
            reduc2 = {}
            combinations = {}  # Assuming this is defined elsewhere in your code
            start_date = None  # Initialize to None
            end_date = None    # Initialize to None

            for name, entry in self.entries_dict[contract_name].get_entries().items():
                
                if name == "EB1 Enable":
                    eb1["enable"] = entry
                    
                if name == "EB1 Percentage":
                    eb1["percentage"] = entry

                if name == "EB1 Date":
                    eb1["date"] = entry

                if name == "EB2 Enable":
                    eb2["enable"] = entry

                if name == "EB2 Percentage":
                    eb2["percentage"] = entry

                if name == "EB2 Date":
                    eb2["date"] = entry

                if name == "LT Enable":
                    lt["enable"] = entry

                if name == "LT Percentage":
                    lt["percentage"] = entry

                if name == "LT Days":
                    lt["days"] = entry

                if name == "Senior Enable":
                    senior["enable"] = entry

                if name == "Senior Percentage":
                    senior["percentage"] = entry

                if name == "Senior Column":
                    senior["column"] = entry

                if name == "Reduc1 Enable":
                    reduc1["enable"] = entry

                if name == "Reduc1 Column":
                    reduc1["column"] = entry

                if name == "Reduc1 Percentage":
                    reduc1["percentage"] = entry

                if name == "Reduc2 Enable":
                    reduc2["enable"] = entry

                if name == "Reduc2 Column":
                    reduc2["column"] = entry

                if name == "Reduc2 Percentage":
                    reduc2["percentage"] = entry
                
                if name == "Combinations EB_LT":
                    combinations["eb_lt"] = entry
                
                if name == "Combinations EB_Reduc":
                    combinations["eb_reduc"] = entry

                if name == "Combinations EB_Senior":
                    combinations["eb_senior"] = entry

                if name == "From date":
                    start_date = entry

                if name == "To date":
                    end_date = entry

            offers["eb1"]=eb1
            offers["eb2"]=eb2
            offers["lt"]=lt
            offers["senior"]=senior
            offers["reduc1"]=reduc1
            offers["reduc2"]=reduc2
            offers["combinations"]=combinations
            offers["start_date"]=start_date
            offers["end_date"]=end_date
            
            offers_per_contract[contract_name] = offers
            
        all_offer_contract_dict[self.setup_name.get("1.0", "end-1c")] = offers_per_contract
        

        self.save_to_database(all_offer_contract_dict)
        
class create_widgets(tk.Frame):
    def __init__(self, master, contract_name, contract_sheet, rank, max_iter, Down, Up, Delete, statment_columns):
        super().__init__(master)
        
        labels = ["EB1 Enable", "EB1 Percentage", "EB1 Date",
                    "EB2 Enable", "EB2 Percentage", "EB2 Date",
                    "LT Enable", "LT Percentage", "LT Days",
                    "Reduc1 Enable", "Reduc1 Column", "Reduc1 Percentage",
                    "Reduc2 Enable", "Reduc2 Column", "Reduc2 Percentage",
                    "Senior Enable", "Senior Column", "Senior Percentage",
                    "Combinations EB_LT", "Combinations EB_Reduc", "Combinations EB_Senior", "From date", "To date"]
        
        self.entries = {}
        self.configure(highlightbackground="black", highlightthickness=2)
        for i, label in enumerate(labels):
            
            if "enable" in label.lower():
                self.entries[label] = tk.BooleanVar()
                
            elif "From date" in label:
                self.entries[label] = DateEntry(self, date_pattern="dd/mm/yyyy")
                self.entries[label].set_date(contract_sheet.loc[0,"first date"])
            elif "To date" in label:
                self.entries[label] = DateEntry(self, date_pattern="dd/mm/yyyy")
                self.entries[label].set_date(contract_sheet.loc[len(contract_sheet)-1,"second date"])
            elif "date" in label.lower():
                self.entries[label] = DateEntry(self, date_pattern="dd/mm/yyyy")
                self.entries[label].set_date(contract_sheet.loc[0,"first date"])

            elif "percentage" in label.lower() or "amount" in label.lower() or "days" in label.lower():
                self.entries[label] = tk.Entry(self)
                

        
        # widgets placemnet

        # eb1

        
        if rank != 1:
            tk.Button(self, image=Up).grid(row=0, column=3, sticky="w", padx=5, pady=5)
        if rank != max_iter:   
            tk.Button(self, image=Down).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        tk.Button(self, image=Delete).grid(row=0, column=4, sticky="w", padx=5, pady=5)

        tk.Label(self, text=str(rank) + "-" + contract_name, font=("Helvetica", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        tk.Label(self, text="").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        if contract_name != "contract":
            tk.Label(self, text="From", font=("Helvetica", 10, "underline")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
            self.entries["From date"].grid(row=2, column=1, sticky="w", padx=5, pady=5)
            tk.Label(self, text="To", font=("Helvetica", 10, "underline")).grid(row=2, column=2, sticky="w", padx=5, pady=5)
            self.entries["To date"].grid(row=2, column=3, sticky="w", padx=5, pady=5)
        
        tk.Label(self, text="").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        
        tk.Label(self, text="Early Booking 1", font=("Helvetica", 10, "underline")).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        
        tk.Label(self, text="Enable").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["EB1 Enable"]).grid(row=5, column=1, sticky="w", padx=5, pady=5)
        
        tk.Label(self, text="Early booking percentage").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.entries["EB1 Percentage"].grid(row=6, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Early booking date").grid(row=6, column=2, sticky="w", padx=5, pady=5)
        self.entries["EB1 Date"].grid(row=6, column=3, sticky="w", padx=5, pady=5)
        
        tk.Label(self, text="").grid(row=7, column=0, sticky="w", padx=5, pady=5)

        # eb2
        tk.Label(self, text="Early Booking 2", font=("Helvetica", 10, "underline")).grid(row=8, column=0, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Enable").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["EB2 Enable"]).grid(row=9, column=1, sticky="w", padx=5, pady=5)
        
        tk.Label(self, text="Early booking percentage").grid(row=10, column=0, sticky="w", padx=5, pady=5)
        self.entries["EB2 Percentage"].grid(row=10, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Early booking date").grid(row=10, column=2, sticky="w", padx=5, pady=5)
        self.entries["EB2 Date"].grid(row=10, column=3, sticky="w", padx=5, pady=5)

        tk.Label(self, text="").grid(row=11, column=0, sticky="w", padx=5, pady=5)

        # reduction 1
        tk.Label(self, text="Reduction 1", font=("Helvetica", 10, "underline")).grid(row=12, column=0, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Enable").grid(row=13, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["Reduc1 Enable"]).grid(row=13, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Reduction 1 percentage").grid(row=14, column=0, sticky="w", padx=5, pady=5)
        self.entries["Reduc1 Percentage"].grid(row=14, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Reduction 1 column").grid(row=14, column=2, sticky="w", padx=5, pady=5)
        
        
        self.entries["Reduc1 Column"] = ttk.Combobox(self, values=list(statment_columns))
        self.entries["Reduc1 Column"].grid(row=14, column=3)

        # Redcution 2
        tk.Label(self, text="Redcution 2", font=("Helvetica", 10, "underline")).grid(row=15, column=0, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Enable").grid(row=16, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["Reduc2 Enable"]).grid(row=16, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Redcution 2 percentage").grid(row=17, column=0, sticky="w", padx=5, pady=5)
        self.entries["Reduc2 Percentage"].grid(row=17, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Redcution 2 column").grid(row=17, column=2, sticky="w", padx=5, pady=5)
        self.entries["Reduc2 Column"] = ttk.Combobox(self, values=list(statment_columns))
        self.entries["Reduc2 Column"].grid(row=17, column=3)

        #lt
        tk.Label(self, text="Long term", font=("Helvetica", 10, "underline")).grid(row=18, column=0, sticky="w", padx=5, pady=5)
        
        tk.Label(self, text="Enable").grid(row=19, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["LT Enable"]).grid(row=19, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Long term percentage").grid(row=20, column=0, sticky="w", padx=5, pady=5)
        self.entries["LT Percentage"].grid(row=20, column=1, sticky="w", padx=5, pady=5)
        
        tk.Label(self, text="Long term days").grid(row=20, column=2, sticky="w", padx=5, pady=5)
        self.entries["LT Days"].grid(row=20, column=3, sticky="w", padx=5, pady=5)
        
        #senior
        tk.Label(self, text="Senior", font=("Helvetica", 10, "underline")).grid(row=21, column=0, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Enable").grid(row=22, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["Senior Enable"]).grid(row=22, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Senior percentage").grid(row=23, column=0, sticky="w", padx=5, pady=5)
        self.entries["Senior Percentage"].grid(row=23, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Senior column").grid(row=23, column=2, sticky="w", padx=5, pady=5)
        self.entries["Senior Column"] = ttk.Combobox(self, values=list(statment_columns))
        self.entries["Senior Column"].grid(row=23, column=3)

        # combinations

        tk.Label(self, text="Combinations", font=("Helvetica", 10, "underline")).grid(row=24, column=0, sticky="w", padx=5, pady=5)
        
        self.entries["Combinations EB_LT"] = tk.BooleanVar()
        tk.Label(self, text="Early booking with long term").grid(row=25, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["Combinations EB_LT"]).grid(row=25, column=1, sticky="w", padx=5, pady=5)
        
        self.entries["Combinations EB_Reduc"] = tk.BooleanVar()
        tk.Label(self, text="Early booking with reduction").grid(row=26, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["Combinations EB_Reduc"]).grid(row=26, column=1, sticky="w", padx=5, pady=5)
        
        self.entries["Combinations EB_Senior"] = tk.BooleanVar()
        tk.Label(self, text="Early booking with senior").grid(row=27, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["Combinations EB_Senior"]).grid(row=27, column=1, sticky="w", padx=5, pady=5)

    def get_entries(self):
        updated_entries = {}
        for key, entry in self.entries.items():
            if isinstance(entry, tk.BooleanVar):
                updated_entries[key] = entry.get()  # For BooleanVar
            elif isinstance(entry, DateEntry):
                updated_entries[key] = entry.get()  # Assuming DateEntry has a get() method
            else:
                updated_entries[key] = entry.get()  # For other types of entries like Entry or Combobox
        return updated_entries


##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################








class Apply(ttk.Frame):
    def __init__(self,parent, current_file=None):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        self.canvas = tk.Canvas(self, background="red", scrollregion=(0,0,self.winfo_width(),20000))
        self.canvas.pack(expand=True, fill='both')

        self.apply_setup = ApplySetup(self)
        # self.canvas.create_window((-1,0), window = self.ApplySetup, anchor='nw', width=self.winfo_width(), height=20000)
        

        self.scrollbar = ttk.Scrollbar(self, orient= "vertical",command=self.canvas.yview)
        self.scrollbar.place(relx=1,rely=0,relheight=1,anchor='ne')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # events
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60),'units'))
        self.bind('<Configure>', self.update_size)

    def update_size(self, event):
        self.canvas.create_window((-1,0), window = self.apply_setup, anchor='nw', width=self.winfo_width(), height=20000)




class ApplySetup(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)


        self.pack(expand=True,fill='both')
        
        if not container:
            
            tk.Label(self, text="Please choose a file to make the setup", font=("Helvetica", 24)).grid(row=0, column=0, sticky="w", padx=0, pady=0)

        else:
            self.tables = self.get_tables()
            tk.Label(self, text="File name", font=("Helvetica", 14,)).grid(row=0, column=0, sticky="w", padx=0, pady=0)
            
            self.file_setup_dict = {}
            self.setup_box = {}
            for file_index in range(len(container)):
                tk.Label(self, text=container[file_index].filename, font=("Helvetica", 10, "underline")).grid(row=1+file_index, column=0, sticky="w", padx=0, pady=0)
                self.setup_box[container[file_index]] = ttk.Combobox(self, values=list(self.tables.keys()))
                self.setup_box[container[file_index]].grid(row=1+file_index, column=1, sticky="w", padx=0, pady=0)
                

            # Button
            self.submit_button = tk.Button(self, text="Submit", command=self.submit)
            self.submit_button.grid(columnspan=2, pady=10)

    def submit(self):
        for file, setup in self.setup_box.items():

            offers_dict = {}

            statment = file.statment
            contracts_sheets = file.contracts_sheets

            if len(setup.get()) == 0:
                
                for contract_name, contract_data in file.contracts_sheets.items():
                    offers_dict[contract_name] = Contract(contract_name,contract_data,file.contracts_activity[contract_name])
                    
            else:
                self.values = self.get_offer_contract_data(setup.get())
                
                for contract_name, contract_data in file.contracts_sheets.items():
                    offers_dict[contract_name] = Contract(contract_name,contract_data,file.contracts_activity[contract_name],self.values[contract_name]["senior"],self.values[contract_name]["earlyBooking1"],self.values[contract_name]["earlyBooking2"],self.values[contract_name]["longTerm"],self.values[contract_name]["reduction1"],self.values[contract_name]["reduction2"],self.values[contract_name]["combinations"],self.values[contract_name]["start_date"],self.values[contract_name]["end_date"])

            invoice = Invoice(file,offers_dict)
            prices = Invoice(file,offers_dict).prices
            date_prices = Invoice(file,offers_dict).Index_contract_date_range_dict

            output_folder = "output"
            # Create the output folder if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Path to the output file
            output_file_path = os.path.join(output_folder, f"{file.filename}_output.xlsx")


            statment.loc[prices.keys(), "Total price"] = [round(price, 2) for price in list(prices.values())]
            statment.loc[list(date_prices.keys()), "calculations"] = [[str(price) for price in prices_dict.values()] for prices_dict in date_prices.values()]


            if "Amount-hotel" in statment.columns:
                statment["Difference"] = statment["Total price"] - statment["Amount-hotel"]
            statment.to_excel(output_file_path, index=False)

    def get_tables(self):
        db_file = 'setups.db'
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            # Get a list of all tables in the database
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            # Create a dictionary to store tables and their values
            tables_and_values = {}

            # Iterate over each table
            for table in tables:
                table_name = table[0]
                # Fetch all rows from the table
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()
                # Store the rows in the dictionary
                tables_and_values[table_name] = rows

            # Close the database connection
            conn.close()

            return tables_and_values

        except sqlite3.Error as e:
            print("SQLite error:", e)
            return None



    def get_offer_contract_data(self, offer_name):
        conn = sqlite3.connect('setups.db')  # Update 'your_database.db' with your actual database name
        c = conn.cursor()
        
        c.execute(f"SELECT * FROM {offer_name}")
        rows = c.fetchall()
        offer_contract_data = {}
        for row in rows:
            contract_data = {}
            contract_data["contract_name"] = row[0]
            contract_data["offer_name"] = row[1]
            contract_data["offer_data"] = row[2]
            
            eb1 = {"enable": row[3], "percentage": row[4], "date": pd.to_datetime(row[5], format='%d/%m/%Y') if row[5] else None}
            eb2 = {"enable": row[6], "percentage": row[7], "date": pd.to_datetime(row[8], format='%d/%m/%Y') if row[8] else None}
            reduc1 = {"enable": row[9], "percentage": row[10], "column": row[11]}
            reduc2 = {"enable": row[12], "percentage": row[13], "column": row[14]}
            lt = {"enable": row[15], "percentage": row[16], "days": row[17]}
            senior = {"enable": row[18], "percentage": row[19], "column": row[20]}
            combinations = {"eb_lt": row[21], "eb_reduc": row[22], "eb_senior": row[23]}
            start_date = pd.to_datetime(row[24], format='%d/%m/%Y') if row[24] else None
            end_date = pd.to_datetime(row[25], format='%d/%m/%Y') if row[25] else None
            active = row[26]
            
            contract_data["earlyBooking1"] = eb1
            contract_data["earlyBooking2"] = eb2
            contract_data["reduction1"] = reduc1
            contract_data["reduction2"] = reduc2
            contract_data["longTerm"] = lt
            contract_data["senior"] = senior
            contract_data["combinations"] = combinations
            contract_data["start_date"] = start_date
            contract_data["end_date"] = end_date
            contract_data["active"] = active

            offer_contract_data[contract_data['contract_name']] = contract_data

        conn.close()
        return offer_contract_data