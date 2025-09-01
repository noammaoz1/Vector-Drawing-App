class ObjectOperationsTools:
    """
    class for tools that manipulate objects on a canvas.
    """

    def __init__(self, canvas):
        """
        Initialize the object manipulator with the given canvas.
        """
        self.canvas = canvas
        self.selected_object = None  # Currently selected object
        self.prev_x = None  # Previous x-coordinate (for tracking movement)
        self.prev_y = None  # Previous y-coordinate (for tracking movement)

    def select_object(self, event):
        """
        Select an object on the canvas when the user clicks on it.

        Parameters:
            event (tk.Event): The mouse event containing the coordinates of the click.
        """
        x, y = event.x, event.y
        items = self.canvas.find_closest(x, y)  # Find the closest object to the clicked coordinates

        if items:
            self.selected_object = items[0]
            self.prev_x, self.prev_y = x, y  # Record initial coordinates for movement

    def release_object(self):
        """
        Release the selected object on the canvas when the user releases the mouse click.
        """
        self.selected_object = None  # Deselect the object

    def move_object(self, event):
        """
        Move the selected object on the canvas when the user drags the mouse.

        Parameters:
            event (tk.Event): The mouse event containing the new coordinates.
        """
        if self.selected_object:
            new_x, new_y = event.x, event.y

            if self.prev_x is not None and self.prev_y is not None:
                # Calculate the movement distance
                dx = new_x - self.prev_x
                dy = new_y - self.prev_y

                # Move the object by the calculated distance
                self.canvas.move(self.selected_object, dx, dy)

                self.prev_x, self.prev_y = new_x, new_y  # Update previous coordinates

    def delete_object(self):
        """
        Delete the selected object on the canvas.
        """
        if self.selected_object:
            self.canvas.delete(self.selected_object)

    def move_forward(self):
        """
        Move the selected object forward by bringing it to the front of the drawing order.
        """
        if self.selected_object:
            self.canvas.tag_raise(self.selected_object)

    def move_backward(self):
        """
        Move the selected object backward by sending it to the back of the drawing order.
        """
        if self.selected_object:
            self.canvas.tag_lower(self.selected_object)
