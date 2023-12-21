import tkinter as tk

class BottomSection(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.canvas_info_label = tk.Label(self, text="Canvas Size: 0x0")
        self.canvas_info_label.pack()

    def configure_bottom_section(self):
        self.pack(side=tk.BOTTOM, fill=tk.X)
        pass

    def update_canvas_info(self, width, height):
        self.canvas_info_label.config(text=f"Canvas Size: {width}x{height}")
