import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

class FileFilterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Filter Utility")
        self.geometry("600x400")
        self.create_widgets()
        
    def create_widgets(self):
        self.folder_path = tk.StringVar()

        # Top frame for folder selection
        top_frame = ttk.Frame(self, padding="10 10 10 10")
        top_frame.grid(row=0, column=0, sticky="EW")
        
        ttk.Label(top_frame, text="Folder:").grid(row=0, column=0, sticky="W", padx=5)
        self.folder_entry = ttk.Entry(top_frame, textvariable=self.folder_path, width=50)
        self.folder_entry.grid(row=0, column=1, sticky="EW", padx=5)
        ttk.Button(top_frame, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=5)
        
        top_frame.columnconfigure(1, weight=1)

        # Middle frame for filter buttons
        filter_frame = ttk.Frame(self, padding="10 10 10 10")
        filter_frame.grid(row=1, column=0, sticky="EW")
        
        self.filter_var = tk.StringVar(value='Images')
        filters = [("Images", "Images"), ("Videos", "Videos"), ("Zips", "Zips"), ("Folders", "Folders")]
        
        for text, mode in filters:
            ttk.Radiobutton(filter_frame, text=text, variable=self.filter_var, value=mode, command=self.display_files).pack(side=tk.LEFT, padx=5)

        # Bottom frame for file list
        self.files_listbox = tk.Listbox(self, width=80, height=20)
        self.files_listbox.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.display_files()

    def display_files(self):
        directory = self.folder_path.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid directory")
            return

        self.files_listbox.delete(0, tk.END)
        if self.filter_var.get() == 'Images':
            extensions = ('.png', '.jpg', '.jpeg', '.gif', '.avif')
        elif self.filter_var.get() == 'Videos':
            extensions = ('.mp4', '.avi', '.mov', '.mkv')
        elif self.filter_var.get() == 'Zips':
            extensions = ('.zip', '.rar', '.7z')
        elif self.filter_var.get() == 'Folders':
            extensions = None

        if extensions:
            files = [f for f in os.listdir(directory) if f.lower().endswith(extensions)]
        else:
            files = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

        for file in files:
            self.files_listbox.insert(tk.END, file)

if __name__ == "__main__":
    app = FileFilterApp()
    app.mainloop()
