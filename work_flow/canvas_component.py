import tkinter as tk
from tkinter import filedialog,simpledialog
from PIL import ImageGrab,ImageTk, Image
import cv2
import numpy as np

class CanvasComponent:
    def __init__(self, root,bottom_section):
        self.root = root
        self.canvas = tk.Canvas(self.root)
        self.image = None
        self.drawing = False
        self.last_x, self.last_y = 0, 0
        self.pen_color = "black"
        self.pen_size = 2 
        self.selection_rect = None
        self.selection_start = None
        self.selected_tool = "Pen"  # Default selected tool
        self.drawn_elements = []  # List to store drawn elements for undo/redo
        self.undo_stack = []  # Stack to store actions for undo
        self.actions = []  # Store actions for undo/redo
        # self.undo_stack = []  # Stack to store actions for undo
        self.bottom_section = bottom_section
        self.root.update()  # Update the window to ensure correct canvas size retrieval
        self.update_canvas_info()  # Initial canvas info update

        self.current_line = None
        self.new_drawing = True
        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
       
    def configure_canvas(self):
        self.canvas.configure(bg="white", width=400, height=500)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def update_pen_size(self, pen_size):
        self.pen_size = pen_size
    
    def start_selection(self, event=None):
        # if event:
        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)

        self.selection_start = (event.x, event.y)
        self.selection_rect = None

    def update_selection(self, event=None):
        if self.selection_start and event:
            if self.selection_rect:
                self.canvas.delete(self.selection_rect)

            x, y = self.selection_start
            self.selection_rect = self.canvas.create_rectangle(x, y, event.x, event.y, outline="black")

    def end_selection(self, event=None):
        if self.selection_start and event:
            selected_area = self.canvas.coords(self.selection_rect)
            dx = event.x - self.selection_start[0]
            dy = event.y - self.selection_start[1]
            self.canvas.move(self.selection_rect, dx, dy)

            self.canvas.delete(self.selection_rect)
            self.selection_start = None
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
       
    def start_drawing(self, event):
      
        if self.selected_tool == "Pen" or self.selected_tool == "Brush":
            self.drawing = True
            self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if self.drawing and (self.selected_tool == "Pen" or self.selected_tool == "Brush"):
            current_x, current_y = event.x, event.y
            self.current_line = self.canvas.create_line(self.last_x, self.last_y, current_x, current_y, width=self.pen_size, fill=self.pen_color, capstyle=tk.ROUND, smooth=True)
            self.actions.append(self.current_line)
            self.last_x, self.last_y = current_x, current_y


            self.last_x, self.last_y = current_x, current_y

    def stop_drawing(self, event):
        self.drawing = False
        self.undo_stack = []

    def update_selected_tool(self, tool):
        self.selected_tool = tool

    def undo(self):
        try:
            if self.actions:
                self.undo_stack.append(self.actions.pop())  # Move drawn element to undo stack
                self.canvas.delete(self.undo_stack[-1])  # Remove from canvas
            elif self.actions:
                action = self.actions.pop()  # Get the last action
                action_type, data = action[0], action[1]

                if action_type == "image_load":
                    self.canvas.delete(self.image)
                    self.image = None
        except Exception as e:
                print("the error is from", e)
    def redo(self):
        if self.undo_stack:
            element = self.undo_stack.pop()  # Get element from undo stack
            self.actions.append(element)  # Move back to drawn elements
            self.canvas.itemconfigure(element, state=tk.NORMAL) 

  
    def save_as_image(self, file_path):
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)

    def update_canvas_info(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.bottom_section.update_canvas_info(canvas_width, canvas_height)

    def update_color(self, color):
            self.pen_color = color  # Update the pen color
            self.new_drawing = True
            # # Optionally, change the color of an existing item
            # for item in self.drawn_elements:
            #     self.canvas.itemconfig(item, fill=self.pen_color)

    def load_image(self, image_path):
        try:
            if self.image:
                self.canvas.delete(self.image)
            img = cv2.imread(image_path)
            img_height, img_width = img.shape[:2]

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if img_height > canvas_height or img_width > canvas_width:
                resize_option = self.prompt_user_for_resize()
                if resize_option == "Custom Size":
                    new_width = simpledialog.askinteger("Resize Image", "Enter new width:")
                    new_height = simpledialog.askinteger("Resize Image", "Enter new height:")
                    img = cv2.resize(img, (new_width, new_height))
                else:
                    img = cv2.resize(img, (canvas_width, canvas_height))

            self.image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.image = Image.fromarray(self.image)
            self.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
            self.actions.append(("image_load", image_path))
        except Exception as e:
            print("Error loading image:", e)

    def prompt_user_for_resize(self):
        answer = tk.messagebox.askquestion("Resize Image", "Would you like to fit the image to the canvas?")
        if answer == 'yes':
            return "Fit Canvas"
        else:
            return "Custom Size"
        
    def create_negative(self):
        # print("test")
       if self.actions:
            try:
                # Capture the content of the canvas as an image using PIL ImageGrab
                x = self.canvas.winfo_rootx()
                y = self.canvas.winfo_rooty()
                width = self.canvas.winfo_width()
                height = self.canvas.winfo_height()
                image = ImageGrab.grab((x, y, x + width, y + height))

                img_np = np.array(image)
                img = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

                # Convert the image to its negative using OpenCV
                negative_img = cv2.bitwise_not(img)

                # Display the negative image on the canvas
                negative_img_rgb = cv2.cvtColor(negative_img, cv2.COLOR_BGR2RGB)
                negative_img_pil = Image.fromarray(negative_img_rgb)

                # Clear the canvas
                self.canvas.delete("all")
                self.drawn_elements.clear()

                # Display the negative image on the canvas
                photo = ImageTk.PhotoImage(image=negative_img_pil)
                self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                self.canvas.image = photo  # Keep a reference to prevent image from being garbage collected

            except Exception as e:
                print("Error:", e)