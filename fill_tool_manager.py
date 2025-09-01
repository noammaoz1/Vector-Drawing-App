NUM_GRADIENT_STEPS = 800  # Number of steps for gradient fill


class FillTool:
    """
        A class representing a tool for filling shapes on a canvas.

        Attributes:
            canvas (tk.Canvas): The canvas on which shapes are drawn.
            toolbar (Toolbar): The toolbar associated with the canvas.
            selected_object (int): The ID of the currently selected shape on the canvas.
    """

    def __init__(self, canvas, toolbar):
        """
        Initializes the FillTool.

        Args:
            canvas (tk.Canvas): The canvas on which shapes are drawn.
            toolbar (Toolbar): The toolbar associated with the canvas.
        """
        self.canvas = canvas
        self.toolbar = toolbar
        self.selected_object = None

    def find_closest_shape(self, event):
        """
        Finds the shape closest to the given point on the canvas.
        """
        x, y = event.x, event.y
        items = self.canvas.find_closest(x, y)

        if items:
            self.selected_object = items[0]  # Set the selected_object attribute to the ID of the closest shape

    def fill_shape(self, event):
        """Fill the shape closest to the click point with the current color."""
        self.find_closest_shape(event)
        if hasattr(self.canvas, 'itemconfig'):
            item_config = self.canvas.itemconfig(self.selected_object)

            # Checks if it can be filled
            if 'fill' in item_config:
                color = self.toolbar.get_fill_color()
                self.canvas.itemconfig(self.selected_object, fill=color)  # Change the fill color of the selected shape

    def shapes_gradual_fill(self, event):
        """Fill the shape closest to the click point with a gradient."""
        color1, color2 = self.toolbar.get_gradual_colors()

        self.find_closest_shape(event)

        # Get the type of the selected shape
        item_type = self.canvas.type(self.selected_object)

        # Get the method to create gradient based on shape type
        fill_method = getattr(self, f'create_gradient_{item_type}', None)

        if fill_method:
            # Call the appropriate method to fill the shape with gradient
            fill_method(self.selected_object, color1, color2)

    def create_gradient(self, color1, color2, num_steps):
        """
        Calculates gradient colors between two given colors.

        Args:
            color1 (tuple): RGB tuple for the starting color.
            color2 (tuple): RGB tuple for the ending color.
            num_steps (int): Number of steps for gradient calculation.

        Returns:
            list: List of gradient colors.
        """
        gradient = []

        # Calculate gradient color at each step
        for i in range(num_steps):
            r = int(color1[0] + (color2[0] - color1[0]) * i / num_steps)
            g = int(color1[1] + (color2[1] - color1[1]) * i / num_steps)
            b = int(color1[2] + (color2[2] - color1[2]) * i / num_steps)
            gradient.append("#%02x%02x%02x" % (r, g, b))

        return gradient

    def create_gradient_rectangle(self, rectangle, color1, color2):
        """
        Fills a rectangle shape with a gradient.
        """
        coords = self.canvas.coords(rectangle)
        x1, y1 = coords[0] + 1, coords[1] + 1
        x2, y2 = coords[2] - 1, coords[3] - 1

        gradient = self.create_gradient(color1, color2, NUM_GRADIENT_STEPS)

        # Create gradient fill for each step
        for i, color in enumerate(gradient):
            self.canvas.create_rectangle(x1, y1 + i * (y2 - y1) / NUM_GRADIENT_STEPS,
                                         x2, y1 + (i + 1) * (y2 - y1) / NUM_GRADIENT_STEPS,
                                         fill=color, outline="")

    def create_gradient_polygon(self, polygon, color1, color2):
        """
        Fills a polygon shape with a gradient.
        """
        coords = self.canvas.coords(polygon)
        x1, y1, x2, y2, x3, y3 = coords

        gradient = self.create_gradient(color1, color2, NUM_GRADIENT_STEPS)

        # Create gradient fill for each step
        for i, color in enumerate(gradient):
            x_fill = x1 + (x2 - x1) * i / NUM_GRADIENT_STEPS
            y_fill = y1 + (y2 - y1) * i / NUM_GRADIENT_STEPS
            self.canvas.create_line(x1, y1, x_fill, y_fill, fill=color)
            self.canvas.create_line(x1, y1, x3 + (x2 - x3) * i / NUM_GRADIENT_STEPS,
                                    y3 + (y2 - y3) * i / NUM_GRADIENT_STEPS, fill=color)
            self.canvas.create_line(x_fill, y_fill, x3 + (x2 - x3) * i / NUM_GRADIENT_STEPS,
                                    y3 + (y2 - y3) * i / NUM_GRADIENT_STEPS,
                                    fill=color)

    def create_gradient_oval(self, oval, color1, color2):
        """
        Fills an oval shape with a gradient.
        """
        coords = self.canvas.coords(oval)
        x1, y1, x2, y2 = coords

        gradient = self.create_gradient(color1, color2, NUM_GRADIENT_STEPS)

        # Calculate center and radius of the oval
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        radius_x = abs(x2 - x1) / 2
        radius_y = abs(y2 - y1) / 2

        # Create gradient fill for each step
        for i, color in enumerate(gradient):
            # Calculate the width and height of the filled oval at this step
            width = radius_x * 2 * (1 - i / NUM_GRADIENT_STEPS)
            height = radius_y * 2 * (1 - i / NUM_GRADIENT_STEPS)

            # Calculate the coordinates of the bounding box for the filled oval
            x_fill1 = center_x - width / 2
            y_fill1 = center_y - height / 2
            x_fill2 = center_x + width / 2
            y_fill2 = center_y + height / 2

            # Create the filled oval using the calculated coordinates
            self.canvas.create_oval(x_fill1, y_fill1, x_fill2, y_fill2, fill=color, outline="")

        self.canvas.create_oval(x1, y1, x2, y2, outline=self.toolbar.get_color())
