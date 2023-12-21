import tkinter as tk
from tkinter import colorchooser

class PropertiesBar:
    def __init__(self, root, canvas_component):
        self.root = root
        self.properties_bar = tk.Frame(self.root, bg="lightgray", width=100, height=400)
        self.pen_size_scale = tk.Scale(self.properties_bar, from_=1, to=10, orient=tk.HORIZONTAL)
        self.canvas_component = canvas_component
        self.pen_size_scale.bind("<ButtonRelease-1>", self.update_pen_size)

        self.color_btn = tk.Button(self.properties_bar, text="Color", command=self.choose_color)
        self.selected_color = "black"  # Default color

    def configure_properties_bar(self):
        # Create a label for pen size
        pen_label = tk.Label(self.properties_bar, text="Pen Size:")
        pen_label.pack(pady=5)

        # Pack the pen size scale initially (hidden by default)
        self.pen_size_scale.pack_forget()
        self.pen_size_scale.pack(pady=5)

        # Add the color button
        self.color_btn.pack(pady=5)

        # Pack the properties bar to the right side
        self.properties_bar.pack(side=tk.LEFT, fill=tk.Y)

    def update_properties(self, tool):
        # Update properties based on the selected tool
        if tool == "Pen":
            self.show_pen_size_scale()
        else:
            self.hide_pen_size_scale()

    def show_pen_size_scale(self):
        self.pen_size_scale.pack()

    def hide_pen_size_scale(self):
        self.pen_size_scale.pack_forget()

    def get_pen_size(self):
        return self.pen_size_scale.get()

    def update_pen_size(self, event=None):
        pen_size = int(self.pen_size_scale.get())
        self.canvas_component.update_pen_size(pen_size)

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Color", color=self.selected_color)[1]
        if color:
            self.selected_color = color
            # Update canvas component with the selected color
            self.canvas_component.update_color(self.selected_color)
