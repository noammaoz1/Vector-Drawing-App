import tkinter as tk
from tkinter import ttk, colorchooser

DEFAULT_COLOR = "black"
THICKNESS_OPTIONS = ["1px", "3px", "5px", "8px", "10px", "12px"]
TOOL_OPTIONS = ["Basic_tools", "Operation", "Thickness", "Shapes", "Text", "Color", "Select", "Clean"]
SHAPES_BY_IMAGES = {"Line": "line_image.png", "Square": "square_image.png", "Triangle": "triangle_image.png",
                    "Oval": "oval_image.png"}
SELECT_IMAGE = "square_select.png"
SIZE_FRONT_OPTIONS = ["10", "12", "14", "16", "18", "20"]
TYPE_FRONT_OPTION = ["Arial", "David", "Times New Roman", "Courier New"]
STYLE_FRONT_OPTION = ["", "bold", "italic", "underline"]


class Toolbar(ttk.Frame):
    """
    Toolbar class represents a set of tools for a drawing application.

    Attributes:
        _drawing_canvas (tk.Canvas): Reference to the canvas widget.
        _selected_tool (tk.StringVar): Keeps track of the currently selected tool.
        _color (str): Current drawing color.
        _fill_color (str): Current fill color.
        _color1 (str): First color for gradual fill.
        _color2 (str): Second color for gradual fill.
        _text_color (str): Current text color.
        _line_width (tk.StringVar): Current line width.
        font_size (tk.StringVar): Current font size for text.
        font_type (tk.StringVar): Current font type for text.
    """

    def __init__(self, master, canvas=None):
        """
        Initialize the Toolbar.
        """
        super().__init__(master)
        self._drawing_canvas = canvas
        self._selected_tool = tk.StringVar()
        self._color = DEFAULT_COLOR
        self._fill_color = DEFAULT_COLOR
        self._color1 = DEFAULT_COLOR
        self._color2 = DEFAULT_COLOR
        self._text_color = DEFAULT_COLOR
        self._line_width = tk.StringVar()
        self.font_size = tk.StringVar(value="10")
        self.font_type = tk.StringVar(value="Arial")
        self.font_style = tk.StringVar(value="")
        self._setup_toolbar()

    def _setup_toolbar(self):
        """
        Set up the toolbar by creating and arranging tool buttons.
        """
        toolbar_frame = ttk.Frame(self.master)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        toolbar_frame = ttk.Frame(self.master)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        for option in TOOL_OPTIONS:
            if option == "Basic_tools":
                self._create_basic_tools(toolbar_frame)
                self._add_separator(toolbar_frame)
            elif option == "Operation":
                self._create_object_operation(toolbar_frame)
                self._add_separator(toolbar_frame)
            elif option == "Thickness":
                self._create_thickness_tool(toolbar_frame)
                self._add_separator(toolbar_frame)
            elif option == "Shapes":
                self._create_shapes_tool(toolbar_frame)
                self._add_separator(toolbar_frame)
            elif option == "Text":
                self._create_text_tool(toolbar_frame)
                self._add_separator(toolbar_frame)
            elif option == "Select":
                self._create_select_tool(toolbar_frame)
                self._add_separator(toolbar_frame)
            elif option == "Color":
                color_frame = ttk.Frame(toolbar_frame)
                color_frame.pack(side=tk.LEFT, padx=5, pady=5)
                self._create_color_button(color_frame)
                self._add_separator(toolbar_frame)
            elif option == "Clean":
                self.clear_button = ttk.Button(toolbar_frame, text="Clear Canvas")
                self.clear_button.pack(side=tk.TOP, padx=5, pady=5)

    def _create_basic_tools(self, toolbar_frame):
        # pen and eraser tools
        pen_frame = ttk.Frame(toolbar_frame)
        pen_frame.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Label(pen_frame, text="Tools").pack(side=tk.TOP)

        # Button for selecting pen tool
        ttk.Button(pen_frame, text="Pen", command=lambda: self._select_tool("Pen")).pack(side=tk.TOP)

        # Button for selecting eraser tool
        ttk.Button(pen_frame, text="Eraser", command=lambda: self._select_tool("Eraser")).pack(side=tk.TOP)

        ttk.Separator(pen_frame, orient='horizontal').pack(fill='x', pady=5)

        # fill tool
        ttk.Button(pen_frame, text="Fill", command=self._choose_fill_color).pack(side=tk.TOP)
        ttk.Button(pen_frame, text="Gradual fill", command=self._choose_colores_for_gradual_fill).pack(side=tk.TOP)

    def _choose_colores_for_gradual_fill(self):
        """
        Activate the gradual fill tool and choose colors for gradual fill.
        """
        self._select_tool("Gradual fill")

        # Open color selection dialogs
        # for color 1
        selected_color1 = tk.colorchooser.askcolor(title="Select first color")[0]
        if selected_color1:
            self._color1 = selected_color1

        # for color 2
        selected_color2 = tk.colorchooser.askcolor(title="Select second color")[0]
        if selected_color2:
            self._color2 = selected_color2

    def _choose_fill_color(self):
        """
        Activate the fill tool and choose a color for filling.
        """
        self._select_tool("Fill")

        # Open color selection dialog for fill color
        fill_color = tk.colorchooser.askcolor(title="Select color")[1]
        if fill_color:
            self._fill_color = fill_color

    def _create_object_operation(self, toolbar_frame):
        """
        Create operation tools for manipulating objects on the canvas.
        Parameters:
            toolbar_frame (ttk.Frame): The frame where the tools are placed.
        """
        # operations on objects
        operation_frame = ttk.Frame(toolbar_frame)
        operation_frame.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Label(operation_frame, text="Operations").pack(side=tk.TOP)

        # Button for moving objects
        ttk.Button(operation_frame, text="Move", command=lambda: self._select_tool("Move")).pack(side=tk.TOP)

        # Button for deleting objects
        ttk.Button(operation_frame, text="Delete", command=lambda: self._select_tool("Delete")).pack(side=tk.TOP)

        # Buttons for bringing objects forward and sending objects backward
        ttk.Button(operation_frame, text="Forward", command=lambda: self._select_tool("Forward")).pack(side=tk.TOP)
        ttk.Button(operation_frame, text="Backward", command=lambda: self._select_tool("Backward")).pack(side=tk.TOP)

    def _create_thickness_tool(self, toolbar_frame):
        """
        Create tool for selecting line thickness.
        """
        thickness_frame = ttk.Frame(toolbar_frame)
        thickness_frame.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Label(thickness_frame, text="Thickness").pack(side=tk.TOP)

        self._line_width.set(THICKNESS_OPTIONS[0])

        # Radio buttons for selecting line thickness
        for size in THICKNESS_OPTIONS:
            ttk.Radiobutton(thickness_frame, text=size, variable=self._line_width, value=size).pack(side=tk.TOP)

    def _create_shapes_tool(self, toolbar_frame):
        """
        Create tools for drawing shapes on the canvas.
        """
        shape_frame = ttk.Frame(toolbar_frame)
        shape_frame.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Label(shape_frame, text="Shapes").pack(side=tk.TOP)

        shape_buttons_frame = ttk.Frame(shape_frame)
        shape_buttons_frame.pack(side=tk.TOP)

        row_index = 0
        column_index = 0

        # Create buttons for different shapes
        for shape, image_file in SHAPES_BY_IMAGES.items():
            shape_image = tk.PhotoImage(file=image_file)
            button = ttk.Button(shape_buttons_frame, image=shape_image,
                                command=lambda s=shape: self._select_tool(s))
            button.image = shape_image
            button.grid(row=row_index, column=column_index, padx=5, pady=5)

            column_index += 1
            if column_index >= 3:
                column_index = 0
                row_index += 1

        # "Polygons" label
        ttk.Label(shape_buttons_frame, text="Polygons").grid(row=row_index + 1, column=column_index, pady=(10, 0))

        # button to start drawing a polygon
        ttk.Button(shape_buttons_frame, text="Start polygon", command=lambda: self._select_tool("Start polygon")).grid(
            row=row_index + 2, column=column_index, pady=5)

        # button to stop drawing a polygon
        ttk.Button(shape_buttons_frame, text="Close Polygon", command=lambda: self._select_tool("Close Polygon")).grid(
            row=row_index + 3, column=column_index, pady=(0, 5))

    def _create_text_tool(self, toolbar_frame):
        """
        Create tools for adding text to the canvas.
        """
        text_frame = ttk.Frame(toolbar_frame)
        text_frame.pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Label(text_frame, text="Text").pack(side=tk.TOP)

        # Button for adding text box
        ttk.Button(text_frame, text="Text box", command=lambda: self._select_tool("Text")).pack(side=tk.TOP)

        # Frame for font size and style selection
        size_style_frame = ttk.Frame(text_frame)
        size_style_frame.pack(side=tk.TOP, fill=tk.X)

        # Dropdown menu for selecting font size
        ttk.Label(size_style_frame, text="Font Size:").pack(side=tk.LEFT)
        font_size_menu = tk.OptionMenu(size_style_frame, self.font_size, *SIZE_FRONT_OPTIONS,
                                       command=self._update_font_size)
        font_size_menu.pack(side=tk.LEFT, fill=tk.X, padx=5)

        # Dropdown menu for selecting font type
        ttk.Label(size_style_frame, text="Font Type:").pack(side=tk.LEFT)
        font_type_menu = tk.OptionMenu(size_style_frame, self.font_type, *TYPE_FRONT_OPTION,
                                       command=self._update_font_type)
        font_type_menu.pack(side=tk.LEFT, fill=tk.X, padx=5)

        # Font style options
        ttk.Label(size_style_frame, text="Font Style:").pack(side=tk.LEFT)
        font_style_menu = tk.OptionMenu(size_style_frame, self.font_style, *STYLE_FRONT_OPTION,
                                        command=self._update_font_style)
        font_style_menu.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=10)

        ttk.Button(text_frame, text="Text Color", command=self._choose_text_color).pack(side=tk.TOP, padx=20, pady=20)

    def _choose_text_color(self):
        """
        Opens a color selection dialog to choose the text color.
        """
        # Open color selection dialog for fill color
        text_color = colorchooser.askcolor()[1]
        if text_color:
            self._text_color = text_color

    def _update_font_size(self, size):
        """
        Update the font size based on the selected value.
        """
        if self._drawing_canvas:
            self._drawing_canvas.text_box_builder.set_font_size(size)

    def _update_font_type(self, font):
        """
        Update the font type based on the selected value.
        """
        if self._drawing_canvas:
            self._drawing_canvas.text_box_builder.set_font_type(font)

    def _update_font_style(self, style):
        """
        Update the font type based on the selected value.
        """
        if self._drawing_canvas:
            self._drawing_canvas.text_box_builder.set_font_style(style)

    def _create_select_tool(self, toolbar_frame):
        """
        Create tools for selecting objects on the canvas.
        Parameters:
            toolbar_frame (ttk.Frame): The frame where the tools are placed.
        """
        select_frame = ttk.Frame(toolbar_frame)
        select_frame.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Label(select_frame, text="Select an object:").pack(side=tk.TOP)

        # Button for selecting a single object
        ttk.Button(select_frame, text="Select object", command=lambda: self._select_tool("Select")).pack(side=tk.TOP,
                                                                                                         padx=10,
                                                                                                         pady=10)
        ttk.Separator(select_frame, orient='horizontal').pack(fill='x', pady=5)

        ttk.Label(select_frame, text="Select objects:").pack(side=tk.TOP, padx=5, pady=5)

        select_buttons_frame = ttk.Frame(select_frame)
        select_buttons_frame.pack(side=tk.TOP)

        # Button for selecting multiple objects
        shape_image = tk.PhotoImage(file=SELECT_IMAGE)
        button = ttk.Button(select_buttons_frame, image=shape_image,
                            command=lambda: self._select_tool("select objects"))
        button.image = shape_image
        button.grid(row=0, column=0, padx=5, pady=5)

        # Button for moving selected objects
        ttk.Button(select_frame, text="Move objects", command=lambda: self._select_tool("Move objects")).pack(
            side=tk.TOP,
            padx=10,
            pady=10)

    def _create_color_button(self, toolbar_frame):
        """
        Create a button for selecting a color.
        """
        ttk.Label(toolbar_frame, text="Colors").pack(side=tk.TOP, padx=5, pady=5)
        ttk.Button(toolbar_frame, text="Select Color", command=self._choose_color).pack(padx=5, pady=5)

    def _choose_color(self):
        """
        Opens a color selection dialog to choose the color.
        """
        color = colorchooser.askcolor()[1]

        if color:
            self._color = color
            if self._drawing_canvas and self._drawing_canvas.text_box_builder:
                self._drawing_canvas.text_box_builder.set_text_color(color)

    def _select_tool(self, tool):
        """
        Sets the selected tool.
        """
        self._selected_tool.set(tool)

    def get_selected_tool(self):
        """
        Get the currently selected tool.
        """
        return self._selected_tool.get()

    def get_color(self):
        """
        Get the currently selected color.
        """
        return self._color

    def get_gradual_colors(self):
        """
        Get the selected gradual fill colors.
        """
        return self._color1, self._color2

    def get_fill_color(self):
        """
        Get the currently selected fill color.
        """
        return self._fill_color

    def get_text_color(self):
        """
        Get the currently selected text color.
        """
        return self._text_color

    def get_line_width(self):
        """
        Get the currently selected line width.
        """
        return self._line_width.get()

    def get_font_size(self):
        """
        Get the currently selected font size.
        """
        return self.font_size.get()

    def get_font_type(self):
        """
        Get the currently selected font type.
        """
        return self.font_type.get()

    def get_font_style(self):
        """
        Get the currently selected font type.
        """
        return self.font_style.get()

    @staticmethod
    def _add_separator(toolbar_frame):
        """
        Add a separator to the toolbar frame.
        """
        ttk.Separator(toolbar_frame, orient='vertical').pack(side=tk.LEFT, padx=5, fill='y')
