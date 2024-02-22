import tkinter as tk
from tkinter import ttk
from browse_frame import MainFrame, SetupContract, Apply
import warnings
import pandas as pd

# Suppress SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
warnings.filterwarnings("ignore", message="Setting an item of incompatible dtype")

# Suppress UserWarnings related to openpyxl
warnings.filterwarnings("ignore", message="Data Validation extension is not supported and will be removed", category=UserWarning)

class ToggleMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.configure(highlightbackground="black", highlightthickness=2)

        self.parent = parent
        self.current_page_name = None  # Store the name of the current page
        self.pages = {}  # Store created pages to avoid recreation
        
        # Create menu buttons with clear labels and functionality
        self.browse_button = ttk.Button(self, text="Browse Data", command=self.show_browse)
        self.setup_contract_button = ttk.Button(self, text="Setup Contract", command=self.show_setup_contract)
        self.apply_page_button = ttk.Button(self, text="Export Data", command=self.show_apply_page)
        
        # Arrange buttons horizontally with padding
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.setup_contract_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.apply_page_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Style the menu frame
        self.configure(bg="#f6f2e9", pady=10)  # Set blue background and padding

        # Initially display the browse page and show the menu at the top
        self.pack(fill=tk.X, expand=False)  # Pack the menu at the top without expansion
        self.show_browse()
        
    def show_page(self, page_name):
        if self.current_page_name:
            self.pages[self.current_page_name].pack_forget()  # Hide current page


        self.current_page_name = page_name
    
        if page_name not in self.pages:
            self.pages[page_name] = globals()[page_name](self.parent)  # Create page if not yet created
            
        if page_name == "SetupContract":
            self.pages[page_name].destroy()
            self.pages[page_name].__init__(self.parent)

        if page_name == "Apply":
            self.pages[page_name].destroy()
            self.pages[page_name].__init__(self.parent)  

        self.pages[page_name].pack(fill=tk.BOTH, expand=True)  # Show the desired page

    def show_browse(self):
        self.show_page("MainFrame")

    def show_setup_contract(self):
        
        self.show_page("SetupContract")  # Use a descriptive name for the page

    def show_apply_page(self):
        self.show_page("Apply")  # Use a descriptive name for the page

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INVO")
        self.geometry("600x600")
        self.minsize(600, 600)
        # self.attributes('-fullscreen', True)
        self.iconbitmap(r"images\logo.ico")
        self.toggle_menu = ToggleMenu(self)  # Create the toggle menu

        # Create quit button
        self.quit_button = ttk.Button(self, text="Quit", command=self.quit_app)
        self.quit_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)

    def quit_app(self):
        self.destroy()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
