import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import subprocess

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

        # Bottom frame for file list and action buttons
        list_frame = ttk.Frame(self, padding="10 10 10 10")
        list_frame.grid(row=2, column=0, sticky="NSEW")
        
        self.files_listbox = tk.Listbox(list_frame, width=80, height=20)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.files_listbox.bind("<Double-1>", self.open_file)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.files_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_listbox.config(yscrollcommand=scrollbar.set)

        action_frame = ttk.Frame(self, padding="10 10 10 10")
        action_frame.grid(row=3, column=0, sticky="EW")

        ttk.Button(action_frame, text="Delete", command=self.delete_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Rename", command=self.rename_file).pack(side=tk.LEFT, padx=5)

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

    def open_file(self, event):
        selected_index = self.files_listbox.curselection()
        if selected_index:
            selected_file = self.files_listbox.get(selected_index)
            full_path = os.path.join(self.folder_path.get(), selected_file)
            if os.path.isdir(full_path):
                subprocess.Popen(f'explorer "{full_path}"')
            else:
                os.startfile(full_path)

    def delete_file(self):
        selected_index = self.files_listbox.curselection()
        if selected_index:
            selected_file = self.files_listbox.get(selected_index)
            full_path = os.path.join(self.folder_path.get(), selected_file)
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_file}'?"):
                try:
                    if os.path.isdir(full_path):
                        os.rmdir(full_path)
                    else:
                        os.remove(full_path)
                    self.display_files()
                    messagebox.showinfo("Success", f"'{selected_file}' has been deleted.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def rename_file(self):
        selected_index = self.files_listbox.curselection()
        if selected_index:
            selected_file = self.files_listbox.get(selected_index)
            full_path = os.path.join(self.folder_path.get(), selected_file)
            new_name = filedialog.asksaveasfilename(initialdir=self.folder_path.get(), initialfile=selected_file, title="Rename File or Folder")
            if new_name:
                new_name = os.path.basename(new_name)
                new_full_path = os.path.join(self.folder_path.get(), new_name)
                try:
                    os.rename(full_path, new_full_path)
                    self.display_files()
                    messagebox.showinfo("Success", f"'{selected_file}' has been renamed to '{new_name}'.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = FileFilterApp()
    app.mainloop()
