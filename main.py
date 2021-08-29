import tkinter as tk
from tkinter import ttk
from utils.display_image import DisplayImage
from utils.buttons import ToolBar


class Main(tk.Tk):
    """
    The main class that is run in the code. It sets up the toolbar and the canvas for GUI.
    """
    def __init__(self):
        """
        Initialise the class variables, the toolbar and the image canvas for display
        """
        tk.Tk.__init__(self)    # Initialise the Tk class

        self.images = []    # The stack of images that have been displayed. Used for undo button
        self.horizontal = None    # The horizontal slider
        self.vertical = None    # The vertical slider
        self.filename = ""    # The filename that the user enters to load/save the file
        self.title("Image Editor")    # Title of the GUI window
        self.toolbar = ToolBar(master=self)    # Toolbar of the GUI that has the widgets
        self.display_image = DisplayImage(master=self)    # The canvas configuration to display image

        separator = ttk.Separator(master=self, orient=tk.HORIZONTAL)   # The lines that separate the widgets from canvas

        self.toolbar.pack(pady=10)    # Packing the toolbar onto the GUI screen
        separator.pack(fill=tk.X, padx=20, pady=5)    # Configuring the separator between widgets and canvas
        self.display_image.pack(fill=tk.BOTH, padx=20, pady=10, expand=1)    # Packing the canvas onto the GUI screen


if __name__ == '__main__':    # If this file is run on the terminal
    root = Main()    # Create an object of main class
    root.mainloop()    # Run the main class infinitely till the user closes the GUI screen window.
