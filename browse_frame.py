from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilenames
import pandas as pd
from tkinter import Scrollbar

class MainFrame(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        self.canvas = tk.Canvas(self, background="#F68497", scrollregion=(0,0,0,5000))
        self.canvas.pack(expand=True, fill='both')

        self.welcome = Welcome(self)
        ttk.Label(self.welcome).pack()
        self.canvas.create_window((-1,0), window = self.welcome, anchor='nw', width=598, height=270)

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
        global dfs
        dfs = [pd.read_excel(file_path) for file_path in self.files]
        
    def remove_selected_files(self):
        selected_indices = self.listbox.curselection()
        for i in selected_indices[::-1]:  # Reversing the list to avoid shifting indexes
            self.listbox.delete(i)
            del self.files[i]

    
class Welcome(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)


        self.pack(expand=True,fill='both')
        # self.create_widgets()
        ExcelFileBrowserApp(self)

    def browseFiles(self):
        filenames = filedialog.askopenfilenames(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("Text files",
                                                            "*.xlsx*"),
                                                        ("all files",
                                                            "*.*")))

        

    def create_widgets(self):
        lista = []
        button_explore = ttk.Button(self, 
                        text = "Browse Files",
                        command = self.browseFiles) 
        
        
        button_exit = ttk.Button(self, 
                            text = "Exit",
                            command = exit) 

        button_explore.place(x=0,y=30)
        
        button_exit.place(x=0,y=50)
        
        