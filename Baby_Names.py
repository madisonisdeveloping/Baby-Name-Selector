import tkinter as tk
from tkinter import ttk
import gspread
from google.oauth2.service_account import Credentials
import random
import string

def connect_to_google_sheets(credentials_file, sheet_name):
    """Connect to Google Sheets."""
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_file(credentials_file, scopes=scope)
    client = gspread.authorize(credentials)
    return client.open(sheet_name).sheet1

def filter_names(sheet, gender, start_letter):
    """Filter names based on gender and starting letter."""
    all_entries = sheet.get_all_records()
    filtered = list(set(
        entry["Name"]
        for entry in all_entries
        if entry["Gender"].strip().lower() == gender.lower()
        and entry["Name"].strip().lower().startswith(start_letter.lower())
    ))  # Use set to remove duplicates
    return filtered

def remove_name_from_sheet(sheet, name):
    """Remove a name from the sheet."""
    cell = sheet.find(name)
    if cell:
        sheet.delete_rows(cell.row)

# Styling helper
class AppleStyleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Baby Name Selector")

        # Set default window size
        window_width = 700
        window_height = 800

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate center position
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.light_mode_colors = {
            "bg": "#F0F0F0",
            "fg": "#333",
            "highlight": "#007AFF",
            "list_bg": "#FFFFFF",
            "list_fg": "#333"
        }

        self.dark_mode_colors = {
            "bg": "#2E2E2E",
            "fg": "#FFFFFF",
            "highlight": "#00AFFF",
            "list_bg": "#3E3E3E",
            "list_fg": "#FFFFFF"
        }

        self.colors = self.light_mode_colors
        self.configure(bg=self.colors["bg"])

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", font=("Helvetica", 12), background=self.colors["bg"], foreground=self.colors["fg"])
        style.configure("TButton", font=("Helvetica", 11), padding=6, relief="flat", background=self.colors["highlight"], foreground="white")
        style.map("TButton", background=[("active", self.colors["highlight"])] )
        style.configure("TEntry", font=("Helvetica", 11), padding=5, relief="flat")

        self.create_widgets()

    def toggle_mode(self):
        self.colors = self.dark_mode_colors if self.colors == self.light_mode_colors else self.light_mode_colors
        self.configure(bg=self.colors["bg"])

        style = ttk.Style()
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["fg"])
        style.configure("TButton", background=self.colors["highlight"], foreground="white")
        self.names_listbox.configure(bg=self.colors["list_bg"], fg=self.colors["list_fg"], selectbackground=self.colors["highlight"])

        # Update all widgets
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(background=self.colors["bg"], foreground=self.colors["fg"])
            elif isinstance(widget, ttk.Entry):
                widget.configure(background=self.colors["list_bg"], foreground=self.colors["list_fg"])

    def create_widgets(self):
        title_label = ttk.Label(self, text="Baby Name Selector", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=15)

        contribute_label = ttk.Label(self, text="type in chat !babynames", font=("Helvetica", 10, "italic"), foreground="#555")
        contribute_label.pack(pady=5)

        frame = ttk.Frame(self, padding=20, style="TFrame")
        frame.pack(fill="x")

        gender_label = ttk.Label(frame, text="Select Gender:")
        gender_label.grid(row=0, column=0, sticky="w", pady=5)
        self.gender_var = tk.StringVar(value="Male")  # Default value is 'Male'
        gender_menu = ttk.Combobox(frame, textvariable=self.gender_var, values=["Male", "Female"], state="readonly")
        gender_menu.grid(row=0, column=1, pady=5)

        start_letter_label = ttk.Label(frame, text="Starting Letter (A-Z):")
        start_letter_label.grid(row=1, column=0, sticky="w", pady=5)
        self.start_letter_entry = ttk.Entry(frame)
        self.start_letter_entry.grid(row=1, column=1, pady=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=15)

        filter_button = ttk.Button(button_frame, text="Filter Names", command=self.filter_names)
        filter_button.grid(row=0, column=0, padx=10)

        remove_button = ttk.Button(button_frame, text="Remove Selected Name", command=self.remove_name)
        remove_button.grid(row=0, column=1, padx=10)
        
        random_button = ttk.Button(button_frame, text="Random Name", command=self.get_random_name)

        random_frame = ttk.Frame(self)
        random_frame.pack(pady=(5, 15))  # Adds spacing between button groups

        random_button = tk.Button(
            random_frame,
            text="🎲 Random Name",
            font=("Helvetica", 11, "bold"),
            command=self.get_random_name_prompt,
            bg="#34A853",  # Custom green color
            fg="white",
            activebackground="#2C8C47",
            relief="flat",
            padx=10,
            pady=5
        )
        random_button.pack()
        
        ##################################################

        # Sun & Moon toggle
        self.mode_icon = tk.StringVar(value="🌜")  # Moon symbol
        self.mode_button = tk.Button(
            self, textvariable=self.mode_icon, font=("Helvetica", 14), relief="flat",
            bg=self.colors["bg"], fg=self.colors["fg"], command=self.toggle_mode, borderwidth=0
        )
        self.mode_button.pack(side="top", anchor="ne", padx=10, pady=10)

        self.names_listbox = tk.Listbox(
            self, font=("Helvetica", 11), height=15, relief="flat", borderwidth=0,
            highlightthickness=1, highlightbackground="#DDD", bg=self.colors["list_bg"], fg=self.colors["list_fg"], selectbackground=self.colors["highlight"]
        )
        self.names_listbox.pack(fill="both", expand=True, padx=20, pady=10)

        footer_label = ttk.Label(self, text="© acottonsock, 2025", font=("Helvetica", 10), foreground="#777")
        footer_label.pack(pady=5)

    def filter_names(self):
        gender = self.gender_var.get().strip()
        start_letter = self.start_letter_entry.get().strip().upper()

        if len(start_letter) != 1 or start_letter not in string.ascii_uppercase:
            self.show_error("Invalid starting letter. Please enter a single letter A-Z.")
            return

        # Connect to Google Sheets
        credentials_file = "your_credentials.json"
        sheet_name = "acottonsock's Baby Names (Responses)"

        try:
            sheet = connect_to_google_sheets(credentials_file, sheet_name)
            names = filter_names(sheet, gender, start_letter)
            self.names_listbox.delete(0, tk.END)
            for name in names:
                self.names_listbox.insert(tk.END, name)

            if names:
                random_name = random.choice(names)
                self.highlight_name(random_name)
                self.show_error(f"Random name suggestion: {random_name}")
            else:
                self.show_error("No names found matching the criteria.")
        except Exception as e:
            self.show_error(f"Error: {e}")

    def highlight_name(self, name):
        for i in range(self.names_listbox.size()):
            if self.names_listbox.get(i) == name:
                self.names_listbox.selection_clear(0, tk.END)
                self.names_listbox.selection_set(i)
                self.names_listbox.see(i)
                break

    def remove_name(self):
        selected = self.names_listbox.curselection()
        if not selected:
            self.show_error("Please select a name to remove.")
            return

        name = self.names_listbox.get(selected[0])

        try:
            credentials_file = "your_credentials.json"
            sheet_name = "acottonsock's Baby Names (Responses)"
            sheet = connect_to_google_sheets(credentials_file, sheet_name)
            remove_name_from_sheet(sheet, name)
            self.names_listbox.delete(selected[0])
            self.show_error(f"Name '{name}' has been removed.")
        except Exception as e:
            self.show_error(f"Error: {e}")

    def show_error(self, message):
        error_window = tk.Toplevel(self)
        error_window.title("Info")
        error_window.geometry("300x100")
        error_window.configure(bg="#F5F5F7")
        ttk.Label(error_window, text=message, wraplength=250).pack(pady=20)

    def get_random_name_prompt(self):
        prompt = tk.Toplevel(self)
        prompt.title("Select Gender")
        prompt.geometry("250x150")
        prompt.configure(bg=self.colors["bg"])

        ttk.Label(prompt, text="Get a random name for:", font=("Helvetica", 12)).pack(pady=10)

        ttk.Button(prompt, text="Male", command=lambda: [prompt.destroy(), self.get_random_name("Male")]).pack(pady=5)
        ttk.Button(prompt, text="Female", command=lambda: [prompt.destroy(), self.get_random_name("Female")]).pack(pady=5)

    def get_random_name(self, gender):
        credentials_file = "your_credentials.json"
        sheet_name = "acottonsock's Baby Names (Responses)"

        try:
            sheet = connect_to_google_sheets(credentials_file, sheet_name)
            all_entries = sheet.get_all_records()
            filtered_names = list(set(
                entry["Name"]
                for entry in all_entries
                if entry["Gender"].strip().lower() == gender.lower()
                and entry["Name"].strip()
            ))

            self.names_listbox.delete(0, tk.END)
            for name in filtered_names:
                self.names_listbox.insert(tk.END, name)

            if filtered_names:
                random_name = random.choice(filtered_names)
                self.highlight_name(random_name)
                self.show_error(f"Random {gender} name: {random_name}")
            else:
                self.show_error(f"No {gender} names found in the sheet.")
        except Exception as e:
            self.show_error(f"Error: {e}")

if __name__ == "__main__":
    
    app = AppleStyleApp()
    app.mainloop()
