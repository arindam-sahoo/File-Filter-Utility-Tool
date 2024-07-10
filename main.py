import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import platform
from PIL import Image
import datetime

class FileFilterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Filter Utility")
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
        filters = [("Images", "Images"), ("Videos", "Videos"), ("Audios", "Audios"), ("Zips", "Zips"), ("Folders", "Folders"), ("PDFs", "PDFs"), ("Docs", "Docs"), ("Sheets", "Sheets"), ("Installers", "Installers")]
        
        for text, mode in filters:
            ttk.Radiobutton(filter_frame, text=text, variable=self.filter_var, value=mode, command=self.display_files).pack(side=tk.LEFT, padx=5)

        # Bottom frame for file list and action buttons
        list_frame = ttk.Frame(self, padding="10 10 10 10")
        list_frame.grid(row=2, column=0, sticky="NSEW")

        self.files_tree = ttk.Treeview(list_frame, columns=("Name", "Size", "Type", "Modified"), show='headings')
        self.files_tree.heading("Name", text="Name", command=lambda: self.sort_files("Name"))
        self.files_tree.heading("Size", text="Size", command=lambda: self.sort_files("Size"))
        self.files_tree.heading("Type", text="Type", command=lambda: self.sort_files("Type"))
        self.files_tree.heading("Modified", text="Modified", command=lambda: self.sort_files("Modified"))
        self.files_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.files_tree.bind("<Double-1>", self.open_file)
        self.files_tree.bind("<Button-3>", self.show_context_menu)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.files_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_tree.config(yscrollcommand=scrollbar.set)

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

        self.sort_order = {
            "Name": False,
            "Size": False,
            "Type": False,
            "Modified": False
        }

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

        self.files_tree.delete(*self.files_tree.get_children())
        if self.filter_var.get() == 'Images':
            extensions = ('.png', '.jpg', '.jpeg', '.gif', '.avif')
        elif self.filter_var.get() == 'Videos':
            extensions = ('.mp4', '.avi', '.mov', '.mkv')
        elif self.filter_var.get() == 'Audios':
            extensions = ('.mp3', '.wav')
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
            full_path = os.path.join(directory, file)
            size = os.path.getsize(full_path)
            file_type = 'Folder' if os.path.isdir(full_path) else os.path.splitext(file)[1]
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d %H:%M:%S')
            self.files_tree.insert("", tk.END, values=(file, self.format_size(size), file_type, modified_time))

    def format_size(self, size):
        # Format size to a readable format
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024

    def sort_files(self, column):
        data = [(self.files_tree.set(child, column), child) for child in self.files_tree.get_children('')]
        if column == 'Size':
            data.sort(key=lambda t: self.sort_helper(t[0]), reverse=self.sort_order[column])
        elif column == 'Modified':
            data.sort(key=lambda t: datetime.datetime.strptime(t[0], '%Y-%m-%d %H:%M:%S'), reverse=self.sort_order[column])
        else:
            data.sort(reverse=self.sort_order[column])
        for index, (val, child) in enumerate(data):
            self.files_tree.move(child, '', index)
        self.sort_order[column] = not self.sort_order[column]

    def sort_helper(self, value):
        try:
            size, unit = value.split()
            size = float(size)
            unit_index = ['B', 'KB', 'MB', 'GB', 'TB'].index(unit)
            return size * (1024 ** unit_index)
        except ValueError:
            return value

    def open_file(self, event):
        selected_item = self.files_tree.selection()
        if selected_item:
            for item in selected_item:
                selected_file = self.files_tree.item(item, "values")[0]
                full_path = os.path.join(self.folder_path.get(), selected_file)
                if os.path.isdir(full_path):
                    subprocess.Popen(f'explorer "{full_path}"')
                else:
                    os.startfile(full_path)

    def delete_file(self):
        selected_items = self.files_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No files selected.")
            return

        selected_files = [self.files_tree.item(item, "values")[0] for item in selected_items]
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
        selected_item = self.files_tree.selection()
        if selected_item:
            selected_file = self.files_tree.item(selected_item, "values")[0]
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
        selected_items = self.files_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No files selected.")
            return

        selected_files = [self.files_tree.item(item, "values")[0] for item in selected_items]
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
        selected_items = self.files_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No files selected.")
            return

        selected_files = [self.files_tree.item(item, "values")[0] for item in selected_items]
        for selected_file in selected_files:
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
            self.files_tree.selection_set(self.files_tree.identify_row(event.y))
            self.context_menu.post(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def view_file(self):
        selected_items = self.files_tree.selection()
        if selected_items:
            for item in selected_items:
                selected_file = self.files_tree.item(item, "values")[0]
                full_path = os.path.join(self.folder_path.get(), selected_file)
                if os.path.isdir(full_path):
                    subprocess.Popen(f'explorer "{full_path}"')
                else:
                    os.startfile(full_path)

    def reveal_file(self):
        selected_items = self.files_tree.selection()
        if selected_items:
            for item in selected_items:
                selected_file = self.files_tree.item(item, "values")[0]
                full_path = os.path.join(self.folder_path.get(), selected_file)
                system_name = platform.system()
                if system_name == 'Windows':
                    subprocess.Popen(['explorer', '/select,', full_path])
                elif system_name == 'Darwin':
                    subprocess.Popen(['open', '--reveal', full_path])
                else:
                    raise NotImplementedError(f'Unsupported OS: {system_name}')

if __name__ == "__main__":
    app = FileFilterApp()
    app.mainloop()
