import tkinter as tk
from tkinter import messagebox, filedialog
from shape_drawer import ShapeDrawer
from text_box_builder import TextBoxBuilder
from object_operations_manager import ObjectOperationsTools
from select_tool_manager import ObjectSelectTool
from fill_tool_manager import FillTool
from PIL import Image, ImageTk


class DrawingCanvas(tk.Canvas):
    """
    Class representing the drawing canvas.
    This class provides a canvas widget for drawing like shapes, text, and images.
    """

    def __init__(self, master, toolbar):
        """
        Initialize the DrawingCanvas with the given root window and toolbar.

        Parameters:
            master (tk.Tk): The main Tkinter root window.
            toolbar (Toolbar): The toolbar containing drawing tools and options.
        """
        super().__init__(master, bg="white")
        self.toolbar = toolbar
        self.shape_drawer = ShapeDrawer(self, toolbar)
        self.text_box_builder = TextBoxBuilder(self, self.toolbar)
        self.fill_tool = FillTool(self, self.toolbar)
        self.operation = ObjectOperationsTools(self)
        self.select_tool = ObjectSelectTool(self, self.toolbar)

        # Variables for drawing operations
        self._start_x = None
        self._start_y = None
        self.text_box = None
        self.images = []

        self._bind_events()

    def _bind_events(self):
        """Bind mouse events for drawing operations."""
        self.bind("<Button-1>", self._start_draw)
        self.bind("<B1-Motion>", self._draw)
        self.bind("<ButtonRelease-1>", self._end_draw)
        self.bind("<Double-Button-1>", self.shape_drawer.close_polygon)
        self.toolbar.clear_button.config(command=self._clear_canvas)

    def _start_draw(self, event):
        """Start drawing based on the selected tool."""
        self._start_x = event.x
        self._start_y = event.y
        tool = self.toolbar.get_selected_tool()
        if tool == "Select":
            self.select_tool.select_object(event)
            self.select_tool.activate_features()
        else:
            self.delete("highlight")
        if tool == "Pen_and_Eraser":
            self._draw_pen_or_eraser(event)
        elif tool == "Start polygon":
            self.shape_drawer.start_polygon(event, self._start_x, self._start_y)
        elif tool == "Close Polygon":
            self._end_draw(event)
        elif tool in ["Line", "Oval", "Square", "Triangle"]:
            self.shape_drawer.draw(event, self._start_x, self._start_y)
        elif tool == "Text":
            self.text_box_builder.start_building(event)
        elif tool == "Move":
            self.operation.select_object(event)
        elif tool == "Delete":
            self.operation.select_object(event)
            self.operation.delete_object()
        elif tool == "Fill":
            self.fill_tool.fill_shape(event)
        elif tool == "Gradual fill":
            self.fill_tool.shapes_gradual_fill(event)
        elif tool == "Forward":
            self.operation.select_object(event)
            self.operation.move_forward()
        elif tool == "Backward":
            self.operation.select_object(event)
            self.operation.move_backward()
        elif tool == "select objects":
            self.select_tool.start_selection(event)

    def _draw(self, event):
        """Continue drawing based on the selected tool."""
        tool = self.toolbar.get_selected_tool()
        if tool == "Start polygon":
            self.shape_drawer.start_polygon(event, self._start_x, self._start_y)
        elif tool in ["Pen", "Eraser"]:
            self._draw_pen_or_eraser(event)
        elif tool in ["Line", "Oval", "Square", "Triangle"]:
            self.shape_drawer.draw(event, self._start_x, self._start_y)
        elif tool == "Text":
            self.text_box_builder.adjust_size(event)
        elif tool == "Move":
            self.operation.move_object(event)
        elif tool == "select objects":
            self.select_tool.update_selection(event)
        elif tool == "Move objects":
            self.select_tool.move_square_objects(event)

    def _end_draw(self, event):
        """Finish drawing."""
        tool = self.toolbar.get_selected_tool()
        if tool in ["Line", "Oval", "Square", "Triangle"]:
            self.shape_drawer.current_shape_item = None  # Reset current shape item
        if tool == "Close Polygon":
            self.shape_drawer.close_polygon(event)
        elif tool == "Text":
            self.text_box_builder.finish_building(event)
        elif tool == "Move":
            self.operation.release_object()
        elif tool == "Delete":
            self.operation.release_object()
        elif tool == "select objects":
            self.select_tool.end_selection(event)
        elif tool == "Move objects":
            self.select_tool.end_move(event)

    def _draw_pen_or_eraser(self, event):
        """Draw with pen or eraser tool."""
        tool = self.toolbar.get_selected_tool()
        if tool == "Pen":
            self._draw_pen(event)
        elif tool == "Eraser":
            self._erase(event)

    def _draw_pen(self, event):
        """Draw with a pen tool."""
        color = self.toolbar.get_color()

        line_width_str = self.toolbar.get_line_width().replace("px", "")
        line_width = int(line_width_str) if line_width_str else 1  # Use default thickness if line width is empty

        # Check if it's the first point
        if self._start_x is None and self._start_y is None:
            self._start_x = event.x
            self._start_y = event.y
            return

        # Draw a line from previous point to current point
        self.create_line(self._start_x, self._start_y, event.x, event.y, fill=color, width=line_width,
                         capstyle=tk.ROUND, smooth=True)

        # Update the starting point for the next line segment
        self._start_x = event.x
        self._start_y = event.y

    def _erase(self, event):
        """Erase using an eraser tool."""
        color = "white"
        line_width_str = self.toolbar.get_line_width().replace("px", "")
        line_width = int(line_width_str) if line_width_str else 1  # Use default eraser thickness if line width is empty

        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)

        self.create_rectangle(x1, y1, x2, y2, fill=color, outline=color, width=line_width)

    def _clear_canvas(self):
        """Clear the content of the canvas."""
        self.delete("all")

    def upload_single_picture(self, file_path, x=0, y=0):
        """Upload a single picture onto the canvas."""
        try:
            # Open the selected image file using PIL
            image = Image.open(file_path)

            # Convert the Image object to a PhotoImage object usable in Tkinter
            photo_image = ImageTk.PhotoImage(image)

            image_id = self.create_image(x, y, anchor=tk.NW, image=photo_image)

            # Append the image with its path to the list
            self.images.append({"id": image_id, "image": photo_image, "path": file_path})

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open the image file: {e}")

    def upload_pictures(self):
        """Upload multiple pictures onto the canvas."""
        # Ask the user to select picture files
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])

        if file_paths:
            for file_path in file_paths:
                self.upload_single_picture(file_path)

    def get_drawing_data(self):
        """
        Get the drawing data from the canvas.

        Returns:
            dict: Dictionary containing the drawing data.
        """
        drawing_data = {
            "objects": [],
            "images": []
        }

        # Iterate through all items on the canvas and extract relevant data
        for item in self.find_all():
            item_type = self.type(item)
            if item_type == "window":  # Handle window (text box) items
                for text_box_attrs in self.text_box_builder.get_text_boxes:
                    text_window = text_box_attrs["text_window"]
                    if text_window == item:  # Check if the current text box item matches the item on the canvas
                        text_obj = text_box_attrs["text_obj"]
                        frame = text_box_attrs["frame"]
                        coord_x = text_box_attrs["coord_x"]
                        coord_y = text_box_attrs["coord_y"]
                        text_width = text_box_attrs["text_width"]
                        text_height = text_box_attrs["text_height"]
                        text_content = text_obj.get("1.0", "end-1c").strip()

                        font_info = text_obj.cget("font")
                        font = font_info.split()

                        font_style = font[-1]
                        font_size = font[-2]
                        font_type = font[0].replace('{', '').replace("}", "")

                        text_color = text_obj.cget("foreground")
                        text_bg_color = text_obj.cget("background")  # Text background color
                        frame_color = frame.cget("bg")  # Frame color

                        drawing_data["objects"].append({
                            "type": "text_box",
                            "text_content": text_content,
                            "font_size": font_size,
                            "font_type": font_type,
                            "font_style": font_style,
                            "text_color": text_color,
                            "text_bg_color": text_bg_color,
                            "frame_color": frame_color,
                            "coord_x": coord_x,
                            "coord_y": coord_y,
                            "text_width": text_width,
                            "text_height": text_height,
                        })

            elif item_type == "image":  # Handle image items
                for image_attrs in self.images:
                    image_id = image_attrs["id"]
                    if image_id == item:
                        image_path = image_attrs["path"]
                        image_data = {"path": image_path, "coords": self.coords(item)}
                        drawing_data["images"].append(image_data)

            elif item_type in ["line", "rectangle", "oval", "polygon"]:
                item_data = {
                    "type": item_type,
                    "coords": self.coords(item),
                    "width": self.itemcget(item, "width"),

                }
                if item_type == "line":
                    item_data["color"] = self.itemcget(item, "fill")
                elif item_type in ["rectangle", "oval", "polygon"]:
                    item_data["color"] = self.itemcget(item, "fill")
                    item_data["outline"] = self.itemcget(item, "outline")
                drawing_data["objects"].append(item_data)

        return drawing_data

    def load_drawing_data(self, drawing_data):
        """
        Load drawing data onto the canvas.

        Parameters:
            drawing_data (dict): Dictionary containing the drawing data.
        """
        self.delete("all")  # Clear the canvas before loading new data

        # Iterate through the objects in the drawing data and draw them on the canvas
        for obj in drawing_data.get("objects", []):
            obj_type = obj.get("type")
            coords = obj.get("coords")
            color = obj.get("color")
            outline = obj.get("outline")
            width = obj.get("width")

            if obj_type == "text_box":  # Handling for text boxes
                text_content = obj.get("text_content")
                font_size = obj.get("font_size")
                font_type = obj.get("font_type")
                text_color = obj.get("text_color")
                text_bg_color = obj.get("text_bg_color")
                frame_color = obj.get("frame_color")
                coord_x = obj.get("coord_x")
                coord_y = obj.get("coord_y")
                text_width = obj.get("text_width")
                text_height = obj.get("text_height")
                font_style = obj.get("font_style")

                # Create text box on the canvas
                text_window = self.create_window(coord_x, coord_y, width=text_width, height=text_height)
                text_frame = tk.Frame(self, bd=2)
                self.itemconfigure(text_window, window=text_frame)
                text_widget = tk.Text(text_frame, wrap=tk.WORD)
                text_widget.pack(expand=True, fill='both')
                text_widget.insert("1.0", text_content)  # Set the text content

                text_attributes = {
                    "text_window": text_window,
                    "text_obj": text_widget,
                    "frame": text_frame,
                    "coord_x": coord_x,
                    "coord_y": coord_y,
                    "text_width": text_width,
                    "text_height": text_height
                }

                self.text_box_builder.get_text_boxes.append(text_attributes)
                try:
                    font_size = int(font_size)  # Convert font size to integer
                except ValueError:
                    font_size = 10  # Default font size if conversion fails

                text_widget.config(foreground=text_color)
                text_widget.config(background=text_bg_color)  # Set text background color
                text_widget.config(font=(font_type, font_size, font_style))
                text_frame.config(bg=frame_color)  # Set frame color

            elif obj_type in ["line", "rectangle", "oval", "polygon"]:
                # Handling for shapes
                if coords is None:
                    continue  # Skip this object if coordinates are missing

                if obj_type == "line":
                    self.create_line(*coords, fill=color, width=width)
                elif obj_type == "rectangle":
                    self.create_rectangle(*coords, fill=color, outline=outline, width=width)
                elif obj_type == "oval":
                    self.create_oval(*coords, fill=color, outline=outline, width=width)
                elif obj_type == "polygon":
                    self.create_polygon(*coords, fill=color, outline=outline, width=width)

        # Load image data onto the canvas
        for img_data in drawing_data.get("images", []):
            image_path = img_data.get("path")
            coords = img_data.get("coords")

            if image_path and coords:
                self.upload_single_picture(image_path, coords[0], coords[1])
