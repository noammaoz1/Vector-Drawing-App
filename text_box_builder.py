import tkinter as tk

DEFAULT_FONT_SIZE = 10


class TextBoxBuilder:
    """
    Class responsible for building a text box on the canvas.
    """

    def __init__(self, canvas, toolbar):
        """
        Initialize the TextBoxBuilder with the given canvas and toolbar.

        Parameters:
            canvas (tk.Canvas): The canvas where the text box will be built.
            toolbar (Toolbar): The toolbar containing font and color options.
        """
        self.canvas = canvas
        self.toolbar = toolbar

        self._text = None
        self._text_frame = None
        self._text_box = None
        self._start_x = None
        self._start_y = None
        self.text_boxes = []

        # Bind font size and font type changes to update text
        self.toolbar.font_size.trace_add('write', self._update_font_settings)
        self.toolbar.font_type.trace_add('write', self._update_font_settings)
        self.toolbar.font_style.trace_add('write', self._update_font_settings)

    def start_building(self, event):
        """Start building the text box."""
        self._start_x = event.x
        self._start_y = event.y

    def adjust_size(self, event):
        """Adjust the size of the text box as the user drags the mouse."""
        if self._text_box:
            self.canvas.delete(self._text_box)

        x, y = event.x, event.y
        self._text_box = self.canvas.create_rectangle(self._start_x, self._start_y, x, y, outline="black", dash=(2, 2))

    def finish_building(self, event):
        """Finish building the text box."""
        x, y = event.x, event.y

        if self._text_box:
            self.canvas.delete(self._text_box)
            self._text_box = None

        # Calculate width and height of the rectangle
        text_width = x - self._start_x
        text_height = y - self._start_y

        # Calculate center position of the rectangle
        center_x = self._start_x + text_width / 2
        center_y = self._start_y + text_height / 2

        # Create window at the center of the rectangle
        text_window = self.canvas.create_window(center_x, center_y, width=text_width, height=text_height)

        self._text_frame = tk.Frame(self.canvas, bd=2)
        self.canvas.itemconfigure(text_window, window=self._text_frame)
        self._text = tk.Text(self._text_frame, wrap=tk.WORD)
        self._text.pack(expand=True, fill='both')
        self._text.bind("<FocusIn>",
                        self.update_text_color)  # Bind to focus event to update color when text is selected
        self._text.focus()

        self._update_font_settings()

        # Store attributes of the text box in a dictionary
        text_attributes = {
            "text_window": text_window,
            "text_obj": self._text,
            "frame": self._text_frame,
            "coord_x": center_x,
            "coord_y": center_y,
            "text_width": text_width,
            "text_height": text_height
        }

        self.get_text_boxes.append(text_attributes)

    def get_text_content(self):
        """Get the content of the text widget."""
        if self._text:
            return self._text.get("1.0", "end-1c").strip()

        return ""

    def _update_font_settings(self, *args):
        """Update font settings for the text widget."""
        if self._text:
            font_size_str = self.toolbar.get_font_size()
            font_type_str = self.toolbar.get_font_type()
            font_style_str = self.toolbar.get_font_style()

            try:
                font_size = int(font_size_str)
            except ValueError:
                font_size = DEFAULT_FONT_SIZE

            font_type = font_type_str
            font_style = font_style_str

            self._text.config(font=(font_type, font_size, font_style))
            self.update_text_color()

    def update_text_color(self, event=None):
        """Update text color for the text widget."""
        if self._text:
            color = self.toolbar.get_text_color()
            self._text.config(foreground=color)

            # Check if the fill button is clicked
            if self.toolbar.get_selected_tool() == "Fill":
                bg_color = self.toolbar.get_fill_color()
                self._text.config(bg=bg_color)

            # Check if the select button is clicked
            if self.toolbar.get_selected_tool() == "Select":
                frame_color = self.toolbar.get_color()
                self._text_frame.config(bg=frame_color)

    def clear_text(self):
        """Clear text from the text widget."""
        if self._text:
            self._text.delete(1.0, tk.END)

    @property
    def get_text_boxes(self):
        """Get the list of text box IDs."""
        return self.text_boxes
