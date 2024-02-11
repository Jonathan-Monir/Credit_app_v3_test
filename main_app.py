import tkinter as tk
from tkinter import ttk
from browse_frame import MainFrame

class ToggleMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Store parent reference

        self.current_page = None  # Keep track of the currently displayed page

        # Create menu buttons with clear labels and functionality
        self.home_button = ttk.Button(self, text="Home", command=self.show_home_page)
        self.page2_button = ttk.Button(self, text="Page 2", command=self.show_page2)
        self.page3_button = ttk.Button(self, text="Page 3", command=self.show_page3)

        # Arrange buttons horizontally with padding
        self.home_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.page2_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.page3_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Style the menu frame
        self.configure(bg="blue", pady=10)  # Set blue background and padding

        # Initially display the Home page and show the menu at the top
        self.pack(fill=tk.X, expand=False)  # Pack the menu at the top without expansion
        self.show_home_page()

    def show_home_page(self):
        if self.current_page is not None:
            self.current_page.destroy()  # Destroy previous page
        self.current_page = MainFrame(self.parent)  # Create new Home page
        self.current_page.pack(fill=tk.BOTH, expand=True)  # Pack to fill parent frame

    def show_page2(self):
        # Similar logic for showing Page 2, replace with your actual content
        if self.current_page is not None:
            self.current_page.destroy()  # Destroy previous page
        self.current_page = tk.Frame(self.parent)  # Create new Page 2 frame
        self.current_page.pack(fill=tk.BOTH, expand=True)  # Pack to fill parent frame

        # Add 3 buttons to Page 2 with clear labels and functionality
        button1 = ttk.Button(self.current_page, text="Button 1", command=self.page2_button1_action)
        button2 = ttk.Button(self.current_page, text="Button 2", command=self.page2_button2_action)
        button3 = ttk.Button(self.current_page, text="Button 3", command=self.page2_button3_action)

        # Arrange buttons horizontally or vertically as desired
        # Example: Arrange horizontally with padding
        button1.pack(side=tk.LEFT, padx=5, pady=5)
        button2.pack(side=tk.LEFT, padx=5, pady=5)
        button3.pack(side=tk.LEFT, padx=5, pady=5)

        # Replace these with your actual button actions
    def page2_button1_action():
        print("page 2")
        pass

    def page2_button2_action():
        print("page 2")
        pass

    def page2_button3_action():
        print("page 2")
        pass

    def show_page3(self):
        # Similar logic for showing Page 3, replace with your actual content
        # ...
        pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INVO")
        self.geometry("600x600")
        self.minsize(600, 600)

        self.toggle_menu = ToggleMenu(self)  # Create the toggle menu

if __name__ == "__main__":
    app = App()
    app.mainloop()
