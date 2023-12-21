import tkinter as tk
from tkinter import filedialog
# from ttkbootstrap import Style

class MenuBar:
    def __init__(self, root,canvas_component):
        self.root = root
        self.menu_bar = tk.Menu(self.root)
        self.canvas_component = canvas_component
        self.undo_icon = tk.PhotoImage(file="undo_icon.png").subsample(2, 2)  # Adjust the subsample parameters for resizing
        self.redo_icon = tk.PhotoImage(file="redo_icon.png").subsample(2, 2)  # Adjust the subsample parameters for resizing
        # self.style = Style(theme='pulse')

    def configure_menu(self):
        # self.root.config(menu=self.menu_bar)
        # self.style.theme_use('pulse')

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open Image", command=self.open_image)
        file_menu.add_command(label="Save As", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        image_menu = tk.Menu(self.menu_bar, tearoff=0)
        image_menu.add_command(label="Resize", command=self.resize_image)
        image_menu.add_command(label="Rotate", command=self.rotate_image)
        image_menu.add_command(label="Crop", command=self.crop_image)
        self.menu_bar.add_cascade(label="Image", menu=image_menu)

        filter_menu = tk.Menu(self.menu_bar, tearoff=0)
        filter_menu.add_command(label="Apply Filters", command=self.apply_filters)
        filter_menu.add_command(label="Adjustments", command=self.adjust_image)
        self.menu_bar.add_cascade(label="Filter", menu=filter_menu)

       # Inserting Undo and Redo after the Filter menu
        self.menu_bar.insert_separator(4)
        self.menu_bar.add_command(label="Undo", command=self.canvas_component.undo, compound=tk.LEFT)
        self.menu_bar.add_command(label="Redo", command=self.canvas_component.redo, compound=tk.LEFT)

        self.root.config(menu=self.menu_bar)

    # Rest of the methods remain the same
    # ...

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png; *.jpg; *.jpeg; *.gif; *.bmp")])
        if file_path:
            self.canvas_component.load_image(file_path)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.canvas_component.save_as_image(file_path)



    def exit_app(self):
        self.root.quit()

    def undo(self):
        # Implement undo functionality
        pass

    def redo(self):
        # Implement redo functionality
        pass

    def clear_canvas(self):
        # Implement clearing the canvas
        pass

    def resize_image(self):
        # Implement image resizing functionality
        pass

    def rotate_image(self):
        # Implement image rotation functionality
        pass

    def crop_image(self):
        # Implement image cropping functionality
        pass

    def apply_filters(self):
        # Implement applying filters functionality
        pass

    def adjust_image(self):
        # Implement image adjustments functionality
        pass
