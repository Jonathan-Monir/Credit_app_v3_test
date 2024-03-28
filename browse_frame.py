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
from invoice import Invoice
import os
import sys
from pandastable import Table
import numpy as np

import warnings
import os

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

warnings.filterwarnings("ignore", message="A value is trying to be set on a copy of a slice from a DataFrame.*")

# Filter out the specific FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)
pd.set_option('mode.chained_assignment', None)


pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.colheader_justify', 'center')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

global_setup_name = "" 

class MainFrame(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        # Load the image
        image = Image.open(resource_path(resource_path(r"images\bg.png")))
        
        desired_width = 600
        desired_height = 600
        image.thumbnail((desired_width, desired_height))

        
        photo = ImageTk.PhotoImage(image)

        # Create a label to display the image
        self.image_label = tk.Label(self, image=photo)
        self.image_label.image = photo  # Keep a reference to prevent garbage collection
        self.image_label.pack()

        # style = ttk.Style()
        # style.configure("Gray.TFrame", background="#f0f0f0")
        
        # # Create a frame with the custom style
        # self.frame = ttk.Frame(self, style="Gray.TFrame", width=200, height=200)
        # # self.pack(expand=True, fill="both")
        
        global container
        container = []
        self.canvas = tk.Canvas(self, background="#f0f0f0", scrollregion=(0,0,self.winfo_width(),800))
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

        self.scrollbar = Scrollbar(self.list_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.list_frame, selectmode=tk.MULTIPLE, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X)

        self.browse_button = tk.Button(self.buttons_frame, text="Select files", command=self.browse_files)
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
        

class DotDict:
    def __init__(self, dictionary):
        self.__dict__ = dictionary

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

class ContractSetting(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill='both')

        self.name_contract_dict = {contract.filename: contract for contract in container}
        self.current_file = None

        tk.Label(self, text="choose file", font=("Helvetica", 10, "underline")).grid(row=0, column=0, sticky="w", padx=5, pady=10)

        self.setup_file = tk.Listbox(self, listvariable=tk.StringVar(value=[file.filename for file in container]))
        self.setup_file.bind('<Double-1>', self.refresh_page)  # Bind to selection event
        self.setup_file.grid(row=1, column=0, sticky="w", padx=5, pady=10, rowspan=8)  # Corrected this line

        tk.Label(self, text="change setup", font=("Helvetica", 10, "underline")).grid(column=0, sticky="w", padx=0, pady=0)
        table_names = list(get_tables().keys())

        table_names.insert(0, 'None')
        self.initialized_setup = ttk.Combobox(self, values=table_names)
        self.initialized_setup.grid(column=0, sticky="w", padx=5, pady=10)
        self.initialized_setup.bind("<<ComboboxSelected>>", self.refresh_page)

        # Button for deleting and deactivating a table
        self.delete_button = tk.Button(self, text="Delete setup", command=self.deactivate_table_column)
        self.delete_button.grid(row=0, column=0, padx=5, pady=15)

        self.contract_frame = ContractFrame(self)
        self.contract_frame.grid(column=0, columnspan=2)


    def refresh_page(self, event):
        
        

        self.contract_frame.destroy()
        self.current_file = self.name_contract_dict[self.setup_file.get(self.setup_file.curselection()[0])]

        if not(len(self.initialized_setup.get()) == 0 ) and not(self.initialized_setup.get() == "None"):
            self.current_setup = get_offer_contract_data(self.initialized_setup.get())
            for contract_name in self.current_setup.keys():
                self.current_setup[contract_name] = { "eb1": self.current_setup[contract_name]["earlyBooking1"],
                    "eb2": self.current_setup[contract_name]["earlyBooking2"],
                    "reduc1": self.current_setup[contract_name]["reduction1"],
                    "reduc2": self.current_setup[contract_name]["reduction2"],
                    "lt": self.current_setup[contract_name]["longTerm"],
                    "senior": self.current_setup[contract_name]["senior"],

                    "combinations": self.current_setup[contract_name]["combinations"],
                    "start_date": self.current_setup[contract_name]["start_date"],

                    "end_date": self.current_setup[contract_name]["end_date"],
                    "sbi": self.current_setup[contract_name]["sbi"],

                }

                self.current_setup[contract_name] = DotDict(self.current_setup[contract_name])
            #print(self.current_setup.contract) 
        
        else:
            self.current_setup = Invoice.make_contracts_dict(self,self.current_file.contracts_sheets,self.current_file.contracts_activity)


        self.contract_frame = ContractFrame(self, self.current_file, self.current_setup)
        self.contract_frame.grid(column = 0, columnspan=2)


    def deactivate_table_column(self):
        # Connect to the database
        conn = sqlite3.connect('setups.db')
        cursor = conn.cursor()
        table_name = self.initialized_setup.get()
        # Check if the column exists in the table
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        active_column_exists = any(column[1] == 'active_table' for column in columns)

        # If the column doesn't exist, add it to the table
        if not active_column_exists:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN active_table INTEGER DEFAULT 0")

        # Update all rows to set the value of 'active_table' column to 0
        cursor.execute(f"UPDATE {table_name} SET active_table = 0")

        # Commit the changes and close the connection
        conn.commit()
        conn.close()        
        self.refresh_page(None)
# import tkinter as tk
from tkinter import messagebox

class ContractFrame(tk.Frame):
    def __init__(self, master=None, current_file=None, initialized_setup=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        if not current_file:
            
            tk.Label(self, text="Please choose a file to make the setup", font=("Helvetica", 24)).grid(row=0, column=0, sticky="w", padx=0, pady=0)

        else:
            self.initialized_setup = initialized_setup
            self.current_file = current_file
            contracts_activity = current_file.contracts_activity
            
            #if not initialized_setup:
                #initialized_setup = Invoice.make_contracts_dict(self, current_file.contracts_sheets, contracts_activity)
                #self.initialized_setup = {contract_name:contract_obj.contract_dictionary for contract_name, contract_obj in initialized_setup.items()}
            
            tk.Label(self, text="Setup name", font=("Helvetica", 10, "underline")).grid(row=1, column=0, sticky="w", padx=0, pady=0)
            self.setup_name = tk.Text(self, height = 1, width = 15)
            self.setup_name.grid(row=2, column=0, sticky="w", padx=5, pady=10)
            
            
            #down
            pathtophoto = Image.open(resource_path(r"images\RD.png")).resize((25,25))
            Down = ImageTk.PhotoImage(pathtophoto)
            panel1 = Label(self, image=Down)
            panel1.image = Down #keep a reference
            
            #up
            pathtophoto = Image.open(resource_path(r"images\RU.png")).resize((25,25))
            Up = ImageTk.PhotoImage(pathtophoto)
            panel1 = Label(self, image=Up)
            panel1.image = Up #keep a reference
            
            #up
            pathtophoto = Image.open(resource_path(r"images\Delete.png")).resize((25,25))
            Delete = ImageTk.PhotoImage(pathtophoto)
            panel1 = Label(self, image=Delete)
            panel1.image = Delete #keep a reference

            max_iter = len(current_file.contracts_sheets)
            rank = 1 

            statment_columns = current_file.statment.columns
            self.entries_dict = {}
            
            
            self.active_app = True
            
            for contract_name, contract_sheet in current_file.contracts_sheets.items():
                if contracts_activity[contract_name]:
                    self.entries_dict[contract_name] = CreateWidgets(self, contract_name=contract_name, contract_sheet=contract_sheet, rank=rank, max_iter=max_iter, Down=Down, Up=Up, Delete=Delete, statment_columns=statment_columns,initialized_setup=self.initialized_setup)
                    self.entries_dict[contract_name].grid(pady=20)
                    rank+=1
                
                else:
                    # show contract_name error in tkinter as a label in red
                    tk.Label(self, text=f"{contract_name} has an error", font=("Helvetica", 10, "underline"), fg="red").grid(column=0, sticky="w", padx=5, pady=5)
                    self.active_app = False
                
            if not(self.active_app):
                
                messagebox.showwarning("Warning", "There are contracts that are not active and may lead to errors")
            
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
            
    def on_combobox_select(self, event):
        self.destroy()
        self.__init__(self.parent)
        

    
    def submit(self):
        
        
        # make a code that will get the name of the tables from setups.db
        import sqlite3
        
        # Connect to the database
        conn = sqlite3.connect('setups.db')
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Get the table names
        table_names = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        
        # Close the connection
        conn.close()
        
        # Convert the table names to a list
        table_list = [name[0] for name in table_names]
        
        
        if len(self.setup_name.get("1.0", "end-1c")) !=0 and self.setup_name.get("1.0", "end-1c") not in table_list:
                
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

                    if name == "sbi":
                        sbi = entry

                offers["eb1"]=eb1
                offers["eb2"]=eb2
                offers["lt"]=lt
                offers["senior"]=senior
                offers["reduc1"]=reduc1
                offers["reduc2"]=reduc2
                offers["combinations"]=combinations
                offers["start_date"]=start_date
                offers["end_date"]=end_date
                offers["sbi"]=sbi
                
                offers_per_contract[contract_name] = offers
                
            all_offer_contract_dict[self.setup_name.get("1.0", "end-1c")] = offers_per_contract
            

            self.save_to_database(all_offer_contract_dict)
        
        elif len(self.setup_name.get("1.0", "end-1c")) ==0:
            tk.Label(self, text="please insert a name text in setup file").grid()
            
        elif len(self.setup_name.get("1.0", "end-1c")) not in table_list:
            tk.Label(self, text="name reapeted text in setup file").grid()


    def save_to_database(self, all_offer_contract_dict):
        # Connect to the SQLite database
        conn = sqlite3.connect(resource_path('setups.db'))
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
                sbi BOOLEAN,
                active_table INTEGER DEFAULT 1)''')

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
                
                sbi = contract_data["sbi"]
                c.execute(f"INSERT INTO {offer_name} (offer_name, contract_name, offer_data, eb1_enable, eb1_percentage, eb1_date, eb2_enable, eb2_percentage, eb2_date, reduc1_enable, reduc1_percentage, reduc1_column, reduc2_enable, reduc2_percentage, reduc2_column, lt_enable, lt_percentage, lt_days, senior_enable, senior_percentage, senior_column, combinations_eb_lt, combinations_eb_reduc, combinations_eb_senior, start_date, end_date, sbi, active_table) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (offer_name, contract_name, str(contract_data), eb1_enable, eb1_percentage, eb1_date, eb2_enable, eb2_percentage, eb2_date, reduc1_enable, reduc1_percentage, str(reduc1_column), reduc2_enable, reduc2_percentage, str(reduc2_column), lt_enable, lt_percentage, lt_days, senior_enable, senior_percentage, str(senior_column), combinations_eb_lt, combinations_eb_recuc, combinations_eb_senior, start_date, end_date, sbi, 1))

        # Commit changes and close the connection
        conn.commit()
        conn.close()
            
class CreateWidgets(tk.Frame):
    def __init__(self, master, contract_name, contract_sheet, rank, max_iter, Down, Up, Delete, statment_columns, initialized_setup):
        super().__init__(master)
        self.entries = {}
        self.labels = ["EB1 Enable", "EB1 Percentage", "EB1 Date",
                    "EB2 Enable", "EB2 Percentage", "EB2 Date",
                    "LT Enable", "LT Percentage", "LT Days",
                    "Reduc1 Enable", "Reduc1 Column", "Reduc1 Percentage",
                    "Reduc2 Enable", "Reduc2 Column", "Reduc2 Percentage",
                    "Senior Enable", "Senior Column", "Senior Percentage",
                    "Combinations EB_LT", "Combinations EB_Reduc", "Combinations EB_Senior",
                    "From date", "To date", "sbi"]
        self.initialized_setup = initialized_setup
        self.create_widgets(contract_name, contract_sheet, rank, max_iter, Down, Up, Delete, statment_columns)
        self.configure(highlightbackground="black", highlightthickness=2)

    def create_widgets(self, contract_name, contract_sheet, rank, max_iter, Down, Up, Delete, statment_columns):
        self.create_entries(contract_sheet, contract_name)
        self.place_navigation_buttons(rank, max_iter, Down, Up, Delete, contract_name)
        self.place_labels(contract_name)
        self.place_additional_widgets(contract_name, contract_sheet, rank, max_iter, Down, Up, Delete, statment_columns)

    def create_entries(self, contract_sheet, contract_name):
        self.contract_setup = self.initialized_setup[contract_name]
        #for label in self.labels:
            #if "enable" in label.lower():
                #self.entries[label] = tk.BooleanVar()
            #elif "From date" in label or "To date" in label or "date" in label.lower():
                #self.entries[label] = DateEntry(self, date_pattern="dd/mm/yyyy")
                #if "From date" in label:
                    #self.entries[label].set_date(contract_sheet.loc[0, "first date"])
                #elif "To date" in label:
                    #self.entries[label].set_date(contract_sheet.loc[len(contract_sheet) - 1, "second date"])
                #else:
                    #self.entries[label].set_date(contract_sheet.loc[0, "first date"])
            #elif "percentage" in label.lower() or "amount" in label.lower() or "days" in label.lower():
                #self.entries[label] = tk.Entry(self)
                
            
        
        self.entries["EB1 Enable"] = tk.BooleanVar(value=self.contract_setup.eb1['enable'])
        self.entries["EB1 Percentage"] = tk.Entry(self)
        self.entries["EB1 Percentage"].delete(0,tk.END)
        self.entries["EB1 Percentage"].insert(0,self.contract_setup.eb1["percentage"])
        self.entries["EB1 Date"] = DateEntry(self)
        self.entries["EB1 Date"].set_date(self.contract_setup.eb1['date'])

        self.entries["EB2 Enable"] = tk.BooleanVar(value=self.contract_setup.eb2['enable'])
        self.entries["EB2 Percentage"] = tk.Entry(self)
        self.entries["EB2 Percentage"].delete(0,tk.END)
        self.entries["EB2 Percentage"].insert(0,self.contract_setup.eb2["percentage"])
        self.entries["EB2 Date"] = DateEntry(self)
        self.entries["EB2 Date"].set_date(self.contract_setup.eb2['date'])

        self.entries["LT Enable"] = tk.BooleanVar(value=self.contract_setup.lt['enable'])
        self.entries["LT Percentage"] = tk.Entry(self)
        self.entries["LT Percentage"].delete(0,tk.END)
        self.entries["LT Percentage"].insert(0,self.contract_setup.lt["percentage"])
        self.entries["LT Days"] = tk.Entry(self)
        self.entries["LT Days"].delete(0,tk.END)
        self.entries["LT Days"].insert(0,self.contract_setup.lt['days'])

        self.entries["Reduc1 Enable"] = tk.BooleanVar(value=self.contract_setup.reduc1['enable'])
        self.entries["Reduc1 Percentage"] = tk.Entry(self)
        self.entries["Reduc1 Percentage"].delete(0,tk.END)
        self.entries["Reduc1 Percentage"].insert(0,self.contract_setup.reduc1["percentage"])

        self.entries["Reduc2 Enable"] = tk.BooleanVar(value=self.contract_setup.reduc2['enable'])
        

        self.entries["Reduc2 Percentage"] = tk.Entry(self)
        self.entries["Reduc2 Percentage"].delete(0,tk.END)
        self.entries["Reduc2 Percentage"].insert(0,self.contract_setup.reduc2["percentage"])

        self.entries["Senior Enable"] = tk.BooleanVar(value=self.contract_setup.senior['enable'])
        self.entries["Senior Percentage"] = tk.Entry(self)
        self.entries["Senior Percentage"].delete(0,tk.END)
        self.entries["Senior Percentage"].insert(0,self.contract_setup.senior["percentage"])

        self.entries["Combinations EB_LT"] = tk.IntVar(value=self.contract_setup.combinations['eb_lt'])
        self.entries["Combinations EB_Reduc"] = tk.IntVar(value=self.contract_setup.combinations['eb_reduc'])
        self.entries["Combinations EB_Senior"] = tk.IntVar(value=self.contract_setup.combinations['eb_senior'])

        self.entries["From date"] = DateEntry(self)
        self.entries["From date"].set_date(self.contract_setup.start_date)

        self.entries["To date"] = DateEntry(self)
        self.entries["To date"].set_date(self.contract_setup.end_date)

        self.entries["sbi"] = tk.BooleanVar(value=self.contract_setup.sbi)


    def place_navigation_buttons(self, rank, max_iter, Down, Up, Delete, contract_name):
        if rank != 1:
            tk.Button(self, image=Up).grid(row=0, column=3, sticky="w", padx=5, pady=5)
        if rank != max_iter:
            tk.Button(self, image=Down).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        tk.Button(self, image=Delete).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        tk.Label(self, text=str(rank) + "-" + contract_name, font=("Helvetica", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        tk.Label(self, text="").grid(row=1, column=0, sticky="w", padx=5, pady=5)

    def place_labels(self, contract_name):
        if contract_name != "contract":
            tk.Label(self, text="From", font=("Helvetica", 10, "underline")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
            self.entries["From date"].grid(row=2, column=1, sticky="w", padx=5, pady=5)
            tk.Label(self, text="To", font=("Helvetica", 10, "underline")).grid(row=2, column=2, sticky="w", padx=5, pady=5)
            self.entries["To date"].grid(row=2, column=3, sticky="w", padx=5, pady=5)
        tk.Label(self, text="").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Early Booking 1", font=("Helvetica", 10, "underline")).grid(row=4, column=0, sticky="w", padx=5, pady=5)

        # eb1

    def place_additional_widgets(self,contract_name, contract_sheet, rank, max_iter, Down, Up, Delete, statment_columns):
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
        
        # eb2
        eb1_start_row = 4
        tk.Label(self, text="Early Booking 1", font=("Helvetica", 10, "underline")).grid(row=eb1_start_row, column=0, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Enable").grid(row=eb1_start_row + 1, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["EB1 Enable"]).grid(row=eb1_start_row + 1, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Early booking percentage").grid(row=eb1_start_row + 2, column=0, sticky="w", padx=5, pady=5)
        self.entries["EB1 Percentage"].grid(row=eb1_start_row + 2, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Early booking date").grid(row=eb1_start_row + 2, column=2, sticky="w", padx=5, pady=5)
        self.entries["EB1 Date"].grid(row=eb1_start_row + 2, column=3, sticky="w", padx=5, pady=5)
        tk.Label(self, text="").grid(row=eb1_start_row + 3, column=0, sticky="w", padx=5, pady=5)

        # eb2
        eb2_start_row = 8
        tk.Label(self, text="Early Booking 2", font=("Helvetica", 10, "underline")).grid(row=eb2_start_row, column=0, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Enable").grid(row=eb2_start_row + 1, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["EB2 Enable"]).grid(row=eb2_start_row + 1, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Early booking percentage").grid(row=eb2_start_row + 2, column=0, sticky="w", padx=5, pady=5)
        self.entries["EB2 Percentage"].grid(row=eb2_start_row + 2, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Early booking date").grid(row=eb2_start_row + 2, column=2, sticky="w", padx=5, pady=5)
        self.entries["EB2 Date"].grid(row=eb2_start_row + 2, column=3, sticky="w", padx=5, pady=5)
        tk.Label(self, text="").grid(row=eb2_start_row + 3, column=0, sticky="w", padx=5, pady=5)

        # Reduction 1
        reduc1_start_row = 12
        tk.Label(self, text="Reduction 1", font=("Helvetica", 10, "underline")).grid(row=reduc1_start_row, column=0, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Enable").grid(row=reduc1_start_row + 1, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["Reduc1 Enable"]).grid(row=reduc1_start_row + 1, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Reduction 1 percentage").grid(row=reduc1_start_row + 2, column=0, sticky="w", padx=5, pady=5)
        self.entries["Reduc1 Percentage"].grid(row=reduc1_start_row + 2, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Reduction 1 column").grid(row=reduc1_start_row + 2, column=2, sticky="w", padx=5, pady=5)
        self.entries["Reduc1 Column"] = ttk.Combobox(self, values=list(statment_columns))
        self.entries["Reduc1 Column"].set(self.contract_setup.reduc1['column'])
        self.entries["Reduc1 Column"].grid(row=reduc1_start_row + 2, column=3)

        # Reduction 2
        reduc2_start_row = 15
        tk.Label(self, text="Reduction 2", font=("Helvetica", 10, "underline")).grid(row=reduc2_start_row, column=0, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Enable").grid(row=reduc2_start_row + 1, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["Reduc2 Enable"]).grid(row=reduc2_start_row + 1, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Reduction 2 percentage").grid(row=reduc2_start_row + 2, column=0, sticky="w", padx=5, pady=5)
        self.entries["Reduc2 Percentage"].grid(row=reduc2_start_row + 2, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Reduction 2 column").grid(row=reduc2_start_row + 2, column=2, sticky="w", padx=5, pady=5)
        self.entries["Reduc2 Column"] = ttk.Combobox(self, values=list(statment_columns))
        self.entries["Reduc2 Column"].set(self.contract_setup.reduc2['column'])
        self.entries["Reduc2 Column"].grid(row=reduc2_start_row + 2, column=3)

        # Long term
        lt_start_row = 18
        tk.Label(self, text="Long term", font=("Helvetica", 10, "underline")).grid(row=lt_start_row, column=0, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Enable").grid(row=lt_start_row + 1, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["LT Enable"]).grid(row=lt_start_row + 1, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Long term percentage").grid(row=lt_start_row + 2, column=0, sticky="w", padx=5, pady=5)
        self.entries["LT Percentage"].grid(row=lt_start_row + 2, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Long term days").grid(row=lt_start_row + 2, column=2, sticky="w", padx=5, pady=5)
        self.entries["LT Days"].grid(row=lt_start_row + 2, column=3, sticky="w", padx=5, pady=5)


        # Senior
        senior_start_row = 21
        tk.Label(self, text="Senior", font=("Helvetica", 10, "underline")).grid(row=senior_start_row, column=0, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Enable").grid(row=senior_start_row + 1, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["Senior Enable"]).grid(row=senior_start_row + 1, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Senior percentage").grid(row=senior_start_row + 2, column=0, sticky="w", padx=5, pady=5)
        self.entries["Senior Percentage"].grid(row=senior_start_row + 2, column=1, sticky="w", padx=5, pady=5)
        tk.Label(self, text="Senior column").grid(row=senior_start_row + 2, column=2, sticky="w", padx=5, pady=5)
        self.entries["Senior Column"] = ttk.Combobox(self, values=list(statment_columns))
        self.entries["Senior Column"].set(self.contract_setup.senior['column'])
        self.entries["Senior Column"].grid(row=senior_start_row + 2, column=3)

        # Combinations
        combinations_start_row = 24
        tk.Label(self, text="Combinations", font=("Helvetica", 10, "underline")).grid(row=combinations_start_row, column=0, sticky="w", padx=5, pady=5)
        
        tk.Label(self, text="Early booking with long term").grid(row=combinations_start_row + 1, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["Combinations EB_LT"]).grid(row=combinations_start_row + 1, column=1, sticky="w", padx=5, pady=5)
        
        tk.Label(self, text="Early booking with reduction").grid(row=combinations_start_row + 2, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["Combinations EB_Reduc"]).grid(row=combinations_start_row + 2, column=1, sticky="w", padx=5, pady=5)
        
        tk.Label(self, text="Early booking with senior").grid(row=combinations_start_row + 3, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["Combinations EB_Senior"]).grid(row=combinations_start_row + 3, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Spo by arrival").grid(row=combinations_start_row + 4, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self, variable=self.entries["sbi"]).grid(row=combinations_start_row + 4, column=1, sticky="w", padx=5, pady=5)
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
            
            self.tables = get_tables()
            
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
                self.values = get_offer_contract_data(setup.get())
                
                for contract_name, contract_data in file.contracts_sheets.items():
                    offers_dict[contract_name] = Contract(contract_name,contract_data,file.contracts_activity[contract_name],self.values[contract_name]["senior"],self.values[contract_name]["earlyBooking1"],self.values[contract_name]["earlyBooking2"],self.values[contract_name]["longTerm"],self.values[contract_name]["reduction1"],self.values[contract_name]["reduction2"],self.values[contract_name]["combinations"],self.values[contract_name]["start_date"],self.values[contract_name]["end_date"])

            invoice = Invoice(file,offers_dict)
            prices = invoice.prices
            date_prices = invoice.Index_contract_date_range_dict

            statment = invoice.output_statment
            output_folder = "output"
            # Create the output folder if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Path to the output file
            output_file_path = os.path.join(output_folder, f"{file.filename}_output.xlsx")


            statment.loc[prices.keys(), "Total price"] = [round(price, 2) for price in list(prices.values())]
            
            
            for date in date_prices.keys():
                
                prices = date_prices[date]
                    
                result = ""
                for table_name, table_data in prices.items():
                    result += f"{table_name}:\n{table_data.to_string(index=False)}\n\n"
                    
                statment.loc[date, "calculations"] = result
                
            if "Amount-hotel" in statment.columns:
                statment["Difference"] = statment["Total price"] - statment["Amount-hotel"]
                
                DifferenceTable(self, statment, file.filename).grid()
            
            # cols_to_drop = statment.columns[~(statment != 0).any()]
            # columns_to_keep = ['Difference']
            # # Drop the selected columns, creating a new DataFrame
            # statment_filtered = statment.drop(columns=list(set(cols_to_drop) - set(columns_to_keep)), inplace=True)

            statment.to_excel(output_file_path, index=False)

def get_tables():
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

            # Check if the table has the 'active_table' column
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            if 'active_table' not in column_names:
                # If 'active_table' column doesn't exist, add it with default value 1
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN active_table INTEGER DEFAULT 1;")
                conn.commit()

            # Fetch all rows from the table
            cursor.execute(f"SELECT * FROM {table_name} WHERE active_table = 1;")
            rows = cursor.fetchall()
            # Store the rows in the dictionary
            if rows:
                tables_and_values[table_name] = rows

        # Close the database connection
        conn.close()

        return tables_and_values

    except sqlite3.Error as e:
        print("SQLite error:", e)
        return None



def get_offer_contract_data(offer_name):
    conn = sqlite3.connect('setups.db')  # Update 'setups.db' with your actual database name
    c = conn.cursor()
    
    c.execute(f"SELECT * FROM {offer_name}")
    rows = c.fetchall()
    offer_contract_data = {}
    for row in rows:
        contract_data = {}
        contract_data["contract_name"] = row[0]
        contract_data["offer_name"] = row[1]
        contract_data["offer_data"] = row[2]
        
        eb1 = {"enable": row[3], "percentage": row[4], "date": parse_date(row[5])}
        eb2 = {"enable": row[6], "percentage": row[7], "date": parse_date(row[8])}
        reduc1 = {"enable": row[9], "percentage": row[10], "column": row[11]}
        reduc2 = {"enable": row[12], "percentage": row[13], "column": row[14]}
        lt = {"enable": row[15], "percentage": row[16], "days": row[17]}
        senior = {"enable": row[18], "percentage": row[19], "column": row[20]}
        combinations = {"eb_lt": row[21], "eb_reduc": row[22], "eb_senior": row[23]}
        start_date = parse_date(row[24])
        end_date = parse_date(row[25])
        sbi = row[26]
        active = row[27]
        
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
        contract_data["sbi"] = sbi

        offer_contract_data[contract_data['contract_name']] = contract_data

    conn.close()
    return offer_contract_data


def parse_date(date_string):
    if date_string:
        # Define a list of possible date formats
        date_formats = [
            '%m/%d/%y', '%m-%d-%y', '%Y-%m-%d', '%d-%m-%Y',  # Various common formats
            '%m/%d/%Y', '%m-%d-%Y', '%d-%m-%y', '%d/%m/%y',  # More variations
            '%b %d, %Y', '%B %d, %Y',  # Month name abbreviations and full names
            '%b %d %Y', '%B %d %Y', '%b. %d, %Y', '%B. %d, %Y',  # With or without dots after month abbreviation
            '%d %b %Y', '%d %B %Y',  # Day and month swapped
            '%Y/%m/%d', '%Y-%m-%d %H:%M:%S'  # ISO format with or without time
        ]

        # Try to match the date string with the regular expressions for the defined formats
        for date_format in date_formats:
            try:
                parsed_date = pd.to_datetime(date_string, format=date_format)
                return parsed_date
            except ValueError:
                continue

        # If none of the formats matched, return None or handle the case as per your requirement
        return None
    return None








############################################################################
############################################################################
############################################################################
############################################################################

class DifferenceTable(ttk.Frame):
    def __init__(self,parent, statment, filename):
        super().__init__(parent)

        columns_to_review = ["Amount-hotel","Total price","Difference"]
        if "Invoice No." in statment:
            columns_to_review.append("Invoice No.")

        elif "Folio" in statment:
            columns_to_review.append("Folio")

        difference_table = statment[statment['Difference'] != 0][columns_to_review]
        
        tk.Label(self, text=filename, font=("Helvetica", 10, "underline"))
        
        # Create a Table object
        table = Table(self, dataframe=difference_table)

        # Optionally, customize table appearance (e.g., column widths, font)
        table.show()

        
if __name__ == "__main__":
    global container
    container = [FileUploader("test files\Biblio- Resort 23-24 . Invo.xlsx")]
    root = tk.Tk()
    root.geometry("800x600")
    app = SetupContract(root)
    root.mainloop()