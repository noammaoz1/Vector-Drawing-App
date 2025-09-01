import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageGrab
import json
from text_box_builder import TextBoxBuilder


class Menu:
    """
    Represents the menu bar of the drawing application.
    """

    def __init__(self, master, canvas):
        """
        Initialize the menu bar for the application.
        """
        self.master = master
        self.canvas = canvas
        self.create_menu()  # Initialize the menu
        self.text_box = TextBoxBuilder
        self.selected_object = None  # Currently selected object (if any)
        self.objects = []  # List to store drawing objects
        self.images = []  # List to store images

    def create_menu(self):
        """Creates the menu bar with various options."""

        menubar = tk.Menu(self.master)  # Create the menu bar

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Drawing", command=self.new_drawing)
        file_menu.add_command(label="open", command=self.open_draw)
        file_menu.add_command(label="Save", command=self.save_drawing)
        file_menu.add_command(label="Export", command=self.export_drawing)
        file_menu.add_command(label="Upload Picture", command=self.canvas.upload_pictures)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)  # Use self.master.quit instead of self.root.quit
        menubar.add_cascade(label="File", menu=file_menu)

        self.master.config(menu=menubar)  # Attach the menu bar to the root window

    def new_drawing(self):
        """creates a new drawing by clears the canvas and resets the list of drawing objects."""
        self.canvas.delete("all")
        self.objects = []

    def open_draw(self):
        """Opens a drawing that saves, from a JSON file."""

        # Placeholder for opening a drawing functionality
        filename = tk.filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])

        if filename:
            try:
                with open(filename, 'r') as file:
                    drawing_data = json.load(file)
                    self.canvas.load_drawing_data(drawing_data)  # Load the drawing data into the canvas

                messagebox.showinfo("Success", "Drawing opened successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to open drawing: {e}")

    def save_drawing(self):
        """Saves the current drawing as a JSON file."""

        # Get the drawing data from the canvas
        drawing_data = self.canvas.get_drawing_data()

        filename = tk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])

        if filename:
            try:
                with open(filename, 'w') as file:
                    json.dump(drawing_data, file)  # Write the drawing data from the JSON file

                messagebox.showinfo("Success", "Drawing saved successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save drawing: {e}")

    def export_drawing(self):
        """Exports the current drawing as a PNG image."""
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            try:
                image = ImageGrab.grab()  # Capture the content of the canvas as an image

                image.save(file_path)  # Save the image to the specified file path

                messagebox.showinfo("Success", "Drawing export successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to export drawing: {e}")
