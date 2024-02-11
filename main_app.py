import tkinter as tk
from tkinter import ttk
from browse_frame import MainFrame

class ToggleMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent  # Store parent reference

        self.current_page = None  # Keep track of the currently displayed page



        # Create menu buttons with clear labels and functionality
        self.browse_button = ttk.Button(self, text="Browse", command=self.show_browse)
        self.setup_contract_button = ttk.Button(self, text="Setup Contract", command=self.show_setup_contract)
        
        # Arrange buttons horizontally with padding
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.setup_contract_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Style the menu frame
        self.configure(bg="#D1FFE8", pady=10)  # Set blue background and padding

        # Initially display the browse page and show the menu at the top
        self.pack(fill=tk.X, expand=False)  # Pack the menu at the top without expansion
        self.show_browse()

        

    def show_browse(self):
        if self.current_page is not None:
            self.current_page.destroy()  # Destroy previous page
        self.current_page = MainFrame(self.parent)  # Create new browse page
        self.current_page.pack(fill=tk.BOTH, expand=True)  # Pack to fill parent frame
        
    def show_setup_contract(self):
        # Similar logic for showing Setup Contract, replace with your actual content
        if self.current_page is not None:
            self.current_page.destroy()  # Destroy previous page
        self.current_page = tk.Frame(self.parent)  # Create new Setup Contract frame
        self.current_page.pack(fill=tk.BOTH, expand=True)  # Pack to fill parent frame

        # Add 3 buttons to Setup Contract with clear labels and functionality
        button1 = ttk.Button(self.current_page, text="Button 1", command=self.setup_contract_button1_action)
        # Arrange buttons horizontally or vertically as desired
        # Example: Arrange horizontally with padding
        button1.pack(side=tk.LEFT, padx=5, pady=5)
        # Replace these with your actual button actions
    def setup_contract_button1_action():
        print("Setup Contract")
        pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INVO")
        self.geometry("600x600")
        self.minsize(600, 600)

        self.toggle_menu = ToggleMenu(self)  # Create the toggle menu

        # Create quit button
        self.quit_button = ttk.Button(self, text="Quit", command=self.quit_app)
        self.quit_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)

    def quit_app(self):
        self.destroy()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
