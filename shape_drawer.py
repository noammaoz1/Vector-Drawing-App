import tkinter as tk
import math


class ShapeDrawer:
    """
    Class responsible for drawing shapes on the canvas, including polygons.
    """

    def __init__(self, canvas, toolbar):
        """
        Initialize the ShapeDrawer with the given canvas and toolbar.

        Parameters:
            canvas (tk.Canvas): The canvas where shapes will be drawn.
            toolbar (Toolbar): The toolbar containing drawing options.
        """
        self.canvas = canvas
        self.toolbar = toolbar

        self.current_shape_item = None
        self.selected_points = []  # List to store selected points for polygon drawing
        self.point_selection_mode = False  # Flag to indicate point selection mode

    def draw(self, event, start_x, start_y):
        """
        Draw the selected shape or polygon based on the current tool.

        Parameters:
            event: The event that triggered the drawing.
            start_x (int): X-coordinate of the starting point.
            start_y (int): Y-coordinate of the starting point.
        """
        selected_shape = self.toolbar.get_selected_tool()
        color = self.toolbar.get_color()
        line_width = int(self.toolbar.get_line_width().replace("px", "")) or 1

        # Determine the shape to draw based on the selected tool
        if selected_shape == "Line":
            self._draw_line(event, start_x, start_y, color, line_width)
        elif selected_shape == "Square":
            self._draw_rectangle(event, start_x, start_y, color, line_width)
        elif selected_shape == "Triangle":
            self._draw_triangle(event, start_x, start_y, color, line_width)
        elif selected_shape == "Oval":
            self._draw_oval(event, start_x, start_y, color, line_width)
        elif selected_shape == "Start polygon":
            self.start_polygon(event, start_x, start_y)
        elif selected_shape == "Close Polygon":
            self.close_polygon(event)

    def _draw_line(self, event, start_x, start_y, color, line_width):
        """Draw a straight line."""
        self._delete_previous_shape()
        self.current_shape_item = self.canvas.create_line(start_x, start_y, event.x, event.y, fill=color,
                                                          width=line_width)

    def _draw_rectangle(self, event, start_x, start_y, color, line_width):
        """Draw a square."""
        self._delete_previous_shape()

        x1, y1 = start_x, start_y
        x2, y2 = event.x, event.y
        self.current_shape_item = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=line_width)

    def _draw_triangle(self, event, start_x, start_y, color, line_width):
        """Draw a triangle."""
        self._delete_previous_shape()

        x1, y1 = start_x, start_y
        x2, y2 = event.x, event.y

        angle = math.atan2(y2 - y1, x2 - x1)
        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        x3 = x1 + length * math.cos(angle - math.pi / 3)
        y3 = y1 + length * math.sin(angle - math.pi / 3)

        self.current_shape_item = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline=color, width=line_width,
                                                             fill='')

    def _draw_oval(self, event, start_x, start_y, color, line_width):
        """Draw an oval (circle)."""
        self._delete_previous_shape()

        x1, y1 = start_x, start_y
        x2, y2 = event.x, event.y
        self.current_shape_item = self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=line_width)

    def start_polygon(self, event, start_x, start_y):
        """Start drawing a polygon."""
        if not self.point_selection_mode:
            self.clear_selection()  # Clear previous selection if not in point selection mode
            self.point_selection_mode = True

        x, y = event.x, event.y
        self.selected_points.append((x, y))

        if len(self.selected_points) > 1:
            prev_point = self.selected_points[-2]
            self.canvas.create_line(prev_point[0], prev_point[1], x, y, fill=self.toolbar.get_color())

    def close_polygon(self, event):
        """Close the polygon by connecting a line between the last point and the first point."""

        if len(self.selected_points) >= 2:
            first_point = self.selected_points[0]
            last_point = self.selected_points[-1]
            self.canvas.create_line(last_point[0], last_point[1], first_point[0], first_point[1],
                                    fill=self.toolbar.get_color())

            self.clear_selection()

    def clear_selection(self):
        """Clear the previous selection."""

        for point in self.selected_points:
            x, y = point
            self.canvas.delete("point_" + str(x) + "_" + str(y))

        self.selected_points.clear()

        self.point_selection_mode = False

    def _delete_previous_shape(self):
        """Delete the previous shape."""

        if self.current_shape_item:
            self.canvas.delete(self.current_shape_item)
            self.current_shape_item = None
