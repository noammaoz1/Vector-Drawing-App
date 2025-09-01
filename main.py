import sys
import tkinter as tk
from drawing_canvas import DrawingCanvas
from toolbar import Toolbar
from menu_manager import Menu

_WINDOW_TITLE = "Vector Drawing App"


def instructions():
    info = """Instructions on how to use "Vector Drawing App":
    First, open the application by running the main file main.py.
    The app allows you to:
    
    1. By using the toolbar:
    - Draw freely using the pen button, and erase using the eraser button.
    - Change the color of the pen using the "Select color" button, and the thickness of the pen and eraser using the
     thickness buttons of your choice.
    - Create shapes using the shape buttons.
    - Filling of shapes and gradual filling of shapes using the fill buttons.
    - perform actions on an object such as move, delete, forward and backward using the appropriate buttons under
     "operations".
    - Create a text box using the "text box" button and type text into it.
    - You can also change the text font, text size, text color and text style you choose to type.
    - One object can be marked using the "Select object" button and its outline color/thickness can be changed using
     the appropriate buttons.
    - Several objects can be selected by the "Select objects" button (a square selection button) and initiated by
     pressing the "Move objects" button and dragging the objects on the canvas to the desired location.
    - The "Clear canvas" button, cleans the canvas completely from all the objects that were on it.
    
    2. Using the menu (above the toolbar):
    by "file":
    - The "New drawing" button clears the entire board and allows you to start a new drawing on the canvas.
    - The "save" button allows you to save the drawing in a file of your choice on the computer.
    - The "open" button allows you to open a drawing file that you have already saved and want to continue working on.
    - The "Export" button allows you to import your drawing into an image file.
    - The "upload picture" button allows you to upload a picture onto the canvas (you can move it and draw on it).
    - The "exit" button exits the application completely and closes it.
    """
    print(info)


def main():
    """
    Main function to initialize and run the vector drawing application.
    """

    # Create a Tkinter root window instance
    root = tk.Tk()
    root.title(_WINDOW_TITLE)

    # Make the window full screen
    root.attributes('-fullscreen', True)

    # Create an instance of Toolbar and pack it within the root window
    toolbar = Toolbar(root)
    toolbar.pack()

    # Create an instance of DrawingCanvas and pass the toolbar to it
    drawing_canvas = DrawingCanvas(root, toolbar)
    drawing_canvas.pack(fill=tk.BOTH, expand=True)

    # Create an instance of Menu
    Menu(root, canvas=drawing_canvas)

    root.mainloop()


if __name__ == "__main__":

    # check if python main.py --help has been activated
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        instructions()
        sys.exit()

    main()
