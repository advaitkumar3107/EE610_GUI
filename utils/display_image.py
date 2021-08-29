from tkinter import Frame, Canvas, CENTER
import cv2
from PIL import ImageTk, Image


class DisplayImage(Frame):
    """
    Class extending the tool bar. Used for displaying the image on the GUI screen and clearing the screen.
    """
    def __init__(self, master = None):
        """
        Initializes the parameters which configure the dimensions of the displaying screen and the image size.
        :param master: Inherits from the tool bar class in the main function
        """
        Frame.__init__(self, master=master, width = 750, height = 750)    # Initializing the display screen size

        self.displayed_image = None
        self.canvas = Canvas(self, width = 750, height = 750)    # The canvas size is set
        self.canvas.place(relx = 0.5, rely = 0.5, anchor = CENTER)    # Placing the canvas such that its center lies
        # in the center of the frame

    def display_image(self, img = None):
        """
        This function is used to display the image from the stack onto the GUI screen. It adjusts the image if it not
        fitting on the screen
        :param img: Image to be displayed
        """
        self.clear_canvas()    # Remove any previous image that is being displayed on the screen

        if img is None:    # If no image is passed as argument
            img = self.master.images[-1]    # Use the last image from the stack

        img = img.astype('uint8')    # Convert the image type to 8-bit int, for displaying
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    # Convert to RGB from BGR

        h, w, _ = img.shape    # Get the height and width of image
        aspect_ratio = h/w    # Get the aspect ratio = height/width

        if h > self.winfo_height() or w > self.winfo_width():    # If any one dimension is larger than the screen size
            if aspect_ratio < 1:    # If width > height
                w = self.winfo_width()    # Adjust width acc to screen size
                h = int(w*aspect_ratio)   # Adjust height of image according to aspect ratio

            else:    # If height > width
                h = self.winfo_height()    # Adjust height acc to screen size
                w = int(h/aspect_ratio)    # Adjust width acc to aspect ratio

        self.displayed_image = cv2.resize(img, (h, w))    # Resize the image to be displayed
        self.displayed_image = ImageTk.PhotoImage(Image.fromarray(self.displayed_image))    # Convert it into image that
        # can be displayed using TKinter GUI

        self.canvas.config(width=w, height=h)    # Reshape the canvas according to dimensions of the image
        self.canvas.create_image(w/2, h/2, anchor = CENTER, image = self.displayed_image)    # Finally display the image
        # which has the center at the center of the canvas

    def clear_canvas(self):
        """
        This function helps to clear the canvas if any image is being displayed on it,
        for the next image to be displayed
        """
        self.canvas.delete("all")    # Delete all the image pixels that are currently using the canvas
