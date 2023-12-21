import tkinter as tk
from menu_bar import MenuBar
from toolbar import Toolbar
from canvas_component import CanvasComponent
from properties_bar import PropertiesBar
from bottom_section import BottomSection

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Application")

        self.bottom_section = BottomSection(self.root)
        self.bottom_section.configure_bottom_section()
        self.canvas_component = CanvasComponent(self.root,self.bottom_section )
        
        self.toolbar = Toolbar(self.root, self,self.canvas_component)
        self.menu_bar = MenuBar(self.root, self.canvas_component)
        
        self.properties_bar = PropertiesBar(self.root, self.canvas_component)

        self.configure_interface()

    def configure_interface(self):
        self.menu_bar.configure_menu()
        self.toolbar.configure_toolbar()
        self.bottom_section.configure_bottom_section()
        self.canvas_component.configure_canvas()
        self.properties_bar.configure_properties_bar()


        # # Packing the toolbar on the left side
        # self.toolbar.toolbar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # # Packing the canvas in the center
        # self.canvas_component.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # # Packing the properties bar to the right side
        # self.properties_bar.properties_bar.pack(side=tk.LEFT, fill=tk.Y)
