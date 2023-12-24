import tkinter as tk
import cv2
from painting import newW
from FaceDetectionModule import faceDetection
import time
class Toolbar:
    def __init__(self, root, drawing_app, canvas_component):
        self.root = root
        self.toolbar_frame = tk.Frame(self.root, bg="lightgray", width=100, height=400)
        self.drawing_app = drawing_app
        self.simple_tools_frame = tk.Frame(self.toolbar_frame, bg="lightgray")
        self.advanced_tools_frame = tk.Frame(self.toolbar_frame, bg="lightgray")
        self.current_tool_frame = self.simple_tools_frame 
        self.canvas_component = canvas_component
        self.pTime = 0
        self.cTime = 0
    def configure_toolbar(self):
       
        btn_simple_tools = tk.Button(self.toolbar_frame, text="Simple Tools", command=self.show_simple_tools)
        btn_simple_tools.pack(side=tk.TOP, fill=tk.X)

        btn_advanced_tools = tk.Button(self.toolbar_frame, text="Advanced Tools", command=self.show_advanced_tools)
        btn_advanced_tools.pack(side=tk.TOP, fill=tk.X)

        btn_pen = tk.Button(self.simple_tools_frame, text="Pen", command=lambda: self.select_tool("Pen"))
        btn_pen.pack(side=tk.TOP,pady=5)

        btn_brush = tk.Button(self.simple_tools_frame, text="Brush", command=lambda: self.select_tool("Brush"))
        btn_brush.pack(side=tk.TOP, padx=5)

        btn_brush = tk.Button(self.simple_tools_frame, text="triangle", command=lambda: self.select_tool("Triangle"))
        btn_brush.pack(side=tk.TOP, padx=5)

        btn_camera = tk.Button(self.toolbar_frame, text="Open Camera", command=self.open_camera)
        btn_camera.pack(side=tk.BOTTOM, pady=5)

        btn_camera = tk.Button(self.toolbar_frame, text="Blur camera", command=self.blur_camera)
        btn_camera.pack(side=tk.BOTTOM, pady=5)

        btn_crop = tk.Button(self.advanced_tools_frame, text="Crop", command=lambda: self.select_tool("Crop"))
        btn_crop.pack(side=tk.TOP, padx=5)
        
     

        btn_rotate = tk.Button(self.advanced_tools_frame, text="Rotate", command=lambda: self.select_tool("Rotate"))
        btn_rotate.pack(side=tk.TOP, padx=5)

        btn_negative = tk.Button(self.advanced_tools_frame, text="negative", command=self.negate)
        btn_negative.pack(side=tk.TOP, padx=5)

        btn_negative = tk.Button(self.advanced_tools_frame, text="selection", command=self.selection)
        btn_negative.pack(side=tk.TOP, padx=5)

        self.toolbar_frame.pack(side=tk.LEFT, fill=tk.Y)
    # self.canvas_component.canvas.bind("<Button-1>", self.start_selection)

    def negate(self):
        self.select_tool("Negate")
        # print("negate")
        self.canvas_component.create_negative()

    def selection(self):
        self.select_tool("Selection")
        # print("negate")
        self.canvas_component.start_selection()

    def select_tool(self, tool):
        self.drawing_app.properties_bar.update_properties(tool)
        if tool == "Pen":
            pen_size = self.drawing_app.properties_bar.get_pen_size()
            self.drawing_app.canvas_component.update_pen_size(pen_size)


    def open_camera(self):
       newW()

    def blur_camera(self):
        cap = cv2.VideoCapture(0)
        # pTime = 0
        detector = faceDetection()

        while True:
            success, img = cap.read()

            img, bboxs = detector.findFace(img,draw=False)
            # lmList = detector.getPosition(img)
            # if len(lmList) != 0:
            # print(lmList[4])
            # cv2.circle(img, (lmList[4][1],lmList[4][2]),5,(0,0,255),cv2.FILLED)
            img = detector.blurFace(img, bboxs)

            self.cTime = time.time()
            fps = 1/(self.cTime-self.pTime)
            self.pTime = self.cTime

            cv2.putText(img, str(int(fps)), (70, 50),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
                

    def show_simple_tools(self):
        self.current_tool_frame.pack_forget()  # Hide the current tool frame
        self.simple_tools_frame.pack(side=tk.TOP, fill=tk.X)  # Show the simple tools frame
        self.current_tool_frame = self.simple_tools_frame  # Update the current tool frame

    def show_advanced_tools(self):
        self.current_tool_frame.pack_forget()  # Hide the current tool frame
        self.advanced_tools_frame.pack(side=tk.TOP, fill=tk.X)  # Show the advanced tools frame
        self.current_tool_frame = self.advanced_tools_frame
    # Define methods for different tools and colors
        
    def use_pen(self):
        # Implement pen functionality
        pass

    def use_eraser(self):
        # Implement eraser functionality
        pass

    def select_red(self):
        # Implement selection of red color
        pass

    def select_blue(self):
        # Implement selection of blue color
        pass
