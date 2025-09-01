class ObjectSelectTool:
    """
    A tool for selecting and manipulating objects on a canvas.
    """

    SELECTION_DASH = (3, 3)

    def __init__(self, canvas, toolbar):
        """
        Initialize ObjectSelectTool.

        Args:
            canvas: The canvas on which objects are placed.
            toolbar: The toolbar to control object properties.
        """
        self.canvas = canvas
        self.toolbar = toolbar
        self.selected_object = None
        self.selection_rectangle = None
        self.marquee_objects = []  # Objects within the selection rectangle

        self.start_x = None  # Initial X coordinate of selection rectangle
        self.start_y = None  # Initial Y coordinate of selection rectangle
        self.prev_x = None  # Previous X coordinate of mouse during movement
        self.prev_y = None  # Previous Y coordinate of mouse during movement

    def select_object(self, event):
        """
        Select an object on the canvas.

        Args:
            event: The mouse event containing coordinates of the click.
        """
        x, y = event.x, event.y

        # Find the closest object to the click coordinates
        items = self.canvas.find_closest(x, y)

        if items:
            if self.selected_object is not None:
                self.deselect_object()

            self.selected_object = items[0]

            if self.selected_object is not None:
                self._highlight_selected_object()

    def deselect_object(self):
        """Deselect the currently selected object."""
        if self.selected_object is not None:
            self.canvas.delete("highlight")

    def _highlight_selected_object(self):
        """Highlight the currently selected object."""
        bbox = self.canvas.bbox(self.selected_object)

        if bbox:
            x1, y1, x2, y2 = bbox

            # Draw a rectangle around the object to highlight it
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", dash=self.SELECTION_DASH, tags="highlight")

    def activate_features(self):
        """Activate features for the selected object."""
        if self.selected_object is not None:

            # Extract line width from toolbar settings
            line_width_str = self.toolbar.get_line_width().replace("px", "")
            line_width = int(line_width_str) if line_width_str else 1

            # Adjust object outline color based on the selected color
            if self.canvas.type(self.selected_object) == 'line':  # For a line, it's the filling
                self.canvas.itemconfigure(self.selected_object, fill=self.toolbar.get_color(), width=line_width)

            elif hasattr(self.canvas, 'itemconfig'):
                object_config = self.canvas.itemconfig(self.selected_object)
                if 'outline' in object_config:
                    self.canvas.itemconfigure(self.selected_object, outline=self.toolbar.get_color(), width=line_width)

    def start_selection(self, event):
        """
        Start the selection process.

        Args:
            event: The mouse event containing coordinates of the click.
        """
        self.start_x = event.x
        self.start_y = event.y

        # Create a selection rectangle at the starting position
        self.selection_rectangle = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y,
                                                                outline="blue", dash=self.SELECTION_DASH,
                                                                tags="highlight")

    def update_selection(self, event):
        """
        Update the selection rectangle during selection.

        Args:
            event: The mouse event containing coordinates of the mouse movement."""

        if self.start_x is not None and self.start_y is not None:
            # Update the selection rectangle to the current mouse position
            self.canvas.coords(self.selection_rectangle, self.start_x, self.start_y, event.x, event.y)

    def end_selection(self, event):
        """
        End the selection process.

        Args:
            event: The mouse event containing coordinates of the mouse release.
        """
        if self.start_x is not None and self.start_y is not None:
            self.marquee_objects.clear()

            # Find objects enclosed by the selection rectangle
            objects_in_marquee = self.canvas.find_enclosed(self.start_x, self.start_y, event.x, event.y)
            self.marquee_objects.extend(objects_in_marquee)

    def move_square_objects(self, event):
        """Move the selected objects within a square selection."""
        if self.prev_x is not None and self.prev_y is not None:
            # Calculate movement delta

            delta_x = event.x - self.prev_x
            delta_y = event.y - self.prev_y

            # Hide the selection rectangle during movement
            self.canvas.itemconfigure(self.selection_rectangle, state='hidden')

            # Move each selected object by the delta amount
            for obj in self.marquee_objects:
                self.canvas.move(obj, delta_x, delta_y)

            # Move each selected object by the delta amount
            self.start_x += delta_x
            self.start_y += delta_y

        # Update previous mouse coordinates for the next movement
        self.prev_x = event.x
        self.prev_y = event.y

    def end_move(self, event) -> None:
        """End moving the selected objects."""

        # Reset previous mouse coordinates and clear selected objects list
        self.prev_x = None
        self.prev_y = None
        self.marquee_objects.clear()
