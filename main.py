import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import platform
from PIL import Image

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
        filters = [("Images", "Images"), ("Videos", "Videos"), ("Zips", "Zips"), ("Folders", "Folders"), ("PDFs", "PDFs"), ("Docs", "Docs"), ("Sheets", "Sheets"), ("Installers", "Installers")]
        
        for text, mode in filters:
            ttk.Radiobutton(filter_frame, text=text, variable=self.filter_var, value=mode, command=self.display_files).pack(side=tk.LEFT, padx=5)

        # Bottom frame for file list and action buttons
        list_frame = ttk.Frame(self, padding="10 10 10 10")
        list_frame.grid(row=2, column=0, sticky="NSEW")
        
        self.files_listbox = tk.Listbox(list_frame, width=80, height=20, selectmode=tk.MULTIPLE)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.files_listbox.bind("<Double-1>", self.open_file)
        self.files_listbox.bind("<Button-3>", self.show_context_menu)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.files_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_listbox.config(yscrollcommand=scrollbar.set)

        action_frame = ttk.Frame(self, padding="10 10 10 10")
        action_frame.grid(row=3, column=0, sticky="EW")

        ttk.Button(action_frame, text="Delete", command=self.delete_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Rename", command=self.rename_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Move", command=self.move_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Convert", command=self.convert_file).pack(side=tk.LEFT, padx=5)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # Context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="View", command=self.view_file)
        self.context_menu.add_command(label="Reveal", command=self.reveal_file)
        self.context_menu.add_command(label="Delete", command=self.delete_file)
        self.context_menu.add_command(label="Move", command=self.move_file)
        self.context_menu.add_command(label="Convert", command=self.convert_file)

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
        elif self.filter_var.get() == 'PDFs':
            extensions = ('.pdf')
        elif self.filter_var.get() == 'Docs':
            extensions = ('.doc', '.docx')
        elif self.filter_var.get() == 'Sheets':
            extensions = ('.xlsx', '.xlsm', '.xls', '.xltx', '.xltm')
        elif self.filter_var.get() == 'Installers':
            extensions = ('.exe', '.msi')
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
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "No files selected.")
            return

        selected_files = [self.files_listbox.get(i) for i in selected_indices]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {len(selected_files)} files?"):
            for selected_file in selected_files:
                full_path = os.path.join(self.folder_path.get(), selected_file)
                try:
                    if os.path.isdir(full_path):
                        os.rmdir(full_path)
                    else:
                        os.remove(full_path)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            self.display_files()
            messagebox.showinfo("Success", f"{len(selected_files)} files have been deleted.")


    def rename_file(self):
        selected_index = self.files_listbox.curselection()
        if selected_index:
            selected_file = self.files_listbox.get(selected_index)
            full_path = os.path.join(self.folder_path.get(), selected_file)
            if os.path.isfile(full_path):
                file_extension = os.path.splitext(selected_file)[1]
            else:
                file_extension = ""
            
            new_name = filedialog.asksaveasfilename(initialdir=self.folder_path.get(), initialfile=os.path.splitext(selected_file)[0], title="Rename File or Folder")
            if new_name:
                new_name = os.path.basename(new_name)
                new_full_path = os.path.join(self.folder_path.get(), new_name + file_extension)
                try:
                    os.rename(full_path, new_full_path)
                    self.display_files()
                    messagebox.showinfo("Success", f"'{selected_file}' has been renamed to '{new_name + file_extension}'.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def move_file(self):
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "No files selected.")
            return

        selected_files = [self.files_listbox.get(i) for i in selected_indices]
        dest_dir = filedialog.askdirectory(title="Select Destination Folder")
        if dest_dir:
            for selected_file in selected_files:
                full_path = os.path.join(self.folder_path.get(), selected_file)
                new_full_path = os.path.join(dest_dir, selected_file)
                try:
                    shutil.move(full_path, new_full_path)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            self.display_files()
            messagebox.showinfo("Success", f"{len(selected_files)} files have been moved to '{dest_dir}'.")

    def convert_file(self):
        selected_index = self.files_listbox.curselection()
        if selected_index:
            selected_file = self.files_listbox.get(selected_index)
            full_path = os.path.join(self.folder_path.get(), selected_file)

            if selected_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.avif')):
                self.convert_image(full_path)

    def convert_image(self, file_path):
        new_format = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("GIF files", "*.gif"), ("AVIF files", "*.avif")])
        if new_format:
            try:
                img = Image.open(file_path)
                img.save(new_format)
                messagebox.showinfo("Success", f"Image has been converted to {new_format}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def show_context_menu(self, event):
        try:
            # Select the file where right-click happened
            self.files_listbox.selection_clear(0, tk.END)
            self.files_listbox.selection_set(self.files_listbox.nearest(event.y))
            self.context_menu.post(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def view_file(self):
        selected_index = self.files_listbox.curselection()
        if selected_index:
            selected_file = self.files_listbox.get(selected_index)
            full_path = os.path.join(self.folder_path.get(), selected_file)
            if os.path.isdir(full_path):
                subprocess.Popen(f'explorer "{full_path}"')
            else:
                os.startfile(full_path)

    def reveal_file(self):
        selected_index = self.files_listbox.curselection()
        if selected_index:
            selected_file = self.files_listbox.get(selected_index)
            full_path = os.path.join(self.folder_path.get(), selected_file)
            system_name = platform.system()
            if system_name == 'Windows':
                subprocess.Popen(['explorer', '/select,', full_path])
            elif system_name == 'Darwin':
                subprocess.Popen(['open', '-R', full_path])
            else:
                messagebox.showerror("Error", f'{system_name} OS is not supported in this application.')

if __name__ == "__main__":
    app = FileFilterApp()
    app.mainloop()
