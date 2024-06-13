import tkinter as tk

class CustomListbox(tk.Listbox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-1>", self.on_click)
        self.bind("<Control-Button-1>", self.on_ctrl_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Shift-Button-1>", self.on_shift_click)
        self.start_index = None

    def on_click(self, event):
        # Handle normal click
        if not event.state & 0x0004:  # Check if Ctrl is not pressed
            self.selection_clear(0, tk.END)
            self.start_index = None
        self.select(event)

    def on_ctrl_click(self, event):
        # Handle Ctrl click
        self.select(event)

    def on_drag(self, event):
        # Handle drag selection
        if event.state & 0x0004:  # Check if Ctrl is pressed
            self.select(event)

    def on_shift_click(self, event):
        # Handle Shift click for range selection
        if self.start_index is None:
            self.start_index = self.nearest(event.y)
        end_index = self.nearest(event.y)
        self.selection_clear(0, tk.END)
        self.selection_set(self.start_index, end_index)

    def select(self, event):
        index = self.nearest(event.y)
        if self.selection_includes(index):
            self.selection_clear(index)
        else:
            self.selection_set(index)
        if not self.start_index:
            self.start_index = index