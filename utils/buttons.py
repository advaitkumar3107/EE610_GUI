from tkinter import Frame, Button, LEFT, filedialog, Scale, HORIZONTAL, VERTICAL, messagebox
import cv2
from image_transforms import log_transform, blur, gamma, edge_detector, equalisation, sharpen


class ToolBar(Frame):
    """
    The main toolbar class which will create the GUI and its widgets for display
    """
    def __init__(self, master=None):
        """
        The initialisation function which is used to initialise the widgets

        :param master: Inheritance class attributes
        """
        Frame.__init__(self, master=master)    # Initialising tkinter.Frame class

        self.load_button = Button(self, text="Load Image")   # Button to load image
        self.equalize_button = Button(self, text="Hist Equalization")   # Button to equalize histogram
        self.gamma_correct_button = Button(self, text="Gamma Correct")   # button to perform gaama correction
        self.log_transform_button = Button(self, text="Log Transform")   # Button to perform log transform
        self.blur_button = Button(self, text="Blur")    # Button to perform gaussian blurring
        self.sharpening_button = Button(self, text="Sharpening")   # Button to perform unsharp masking
        self.undo_last_button = Button(self, text="Undo Last Change")   # Button to undo last change
        self.undo_all_button = Button(self, text="Undo All Changes")    # Button to undo all changes
        self.save_current_button = Button(self, text="Save Current")   # Button to save the current displayed image
        self.edge_detector_button = Button(self, text="Edge Detector")  # Button to perform sobel edge detection

        # Binding all the buttons to the action that will be performed when the user presses them
        self.load_button.bind("<ButtonRelease>", self.load_button_released)
        self.equalize_button.bind("<ButtonRelease>", self.equalize_button_released)
        self.gamma_correct_button.bind("<ButtonRelease>", self.gamma_correct_released)
        self.log_transform_button.bind("<ButtonRelease>", self.log_transform_released)
        self.blur_button.bind("<ButtonRelease>", self.blur_released)
        self.sharpening_button.bind("<ButtonRelease>", self.sharpening_released)
        self.undo_last_button.bind("<ButtonRelease>", self.undo_last_released)
        self.undo_all_button.bind("<ButtonRelease>", self.undo_all_released)
        self.save_current_button.bind("<ButtonRelease>", self.save_current_released)
        self.edge_detector_button.bind("<ButtonRelease>", self.edge_detector_released)

        # Packing all buttons to the GUI window where they will be seen by the user. They will be arranged horizontally
        self.load_button.pack(side=LEFT)
        self.equalize_button.pack(side=LEFT)
        self.gamma_correct_button.pack(side=LEFT)
        self.log_transform_button.pack(side=LEFT)
        self.blur_button.pack(side=LEFT)
        self.sharpening_button.pack(side=LEFT)
        self.undo_last_button.pack(side=LEFT)
        self.undo_all_button.pack(side=LEFT)
        self.save_current_button.pack(side=LEFT)
        self.edge_detector_button.pack()

    def image_present_check(self):
        """
        This function checks whether there are any images left in the stack. If not then it throws up the error window
        """
        if not self.master.images:     # If no images present in the list
            messagebox.showerror("Error", 'No image selected')   # Throw up the error messagebox

        else:
            return True   # If there are images present in the list, then return True value

    def load_button_released(self, event):
        """
        Describes behaviour of load button when the user clicks on it. It loads the image onto the screen from the
        user's local computer

        :param event: User clicks on the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.load_button:  # If the clicked area contains the
            # load button
            filename = filedialog.askopenfilename()    # A file dialog opens asking the user to select the file
            img = cv2.imread(filename)    # Image is read from that file location
            img = img.astype('float32')    # Convert the pixels to 8 bit float to perform float operations on them

            if img is not None:    # If image is selected
                self.master.filename = filename    # Set the filename parameter
                self.master.images.append(img)     # Append the selected image in the stack
                self.master.display_image.display_image(img=img)    # Display the image on the window

    def save_current_released(self, event):
        """
        Describes behaviour of save button when the user clicks on it. It saves the displayed image to the user's
        local computer. If there is no displayed image, it throws up an error

        :param event: User clicks on the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.save_current_button: # If clicked area contains
            # save button
            if self.image_present_check():    # If image is present in the stack
                file_type = self.master.filename.split('.')[-1]    # Get the file extension from the filename
                filename = filedialog.asksaveasfile()    # Invoke a dialog box asking the user what name they want to
                # save the image as and get the abolute path
                filename = filename.name + '.' + file_type    # Append the file extension to the path
                cv2.imwrite(filename, self.master.images[-1])    # Save the image in the path provided by user
                self.master.filename = filename    # Update the filename variable with new name

    def undo_last_released(self, event):
        """
        Describes behaviour of undo last button when the user clicks on it. It undos the last transformation that was
        applied to the image. If no transformation was applied and the image is original, then makes the window blank.
        If screen is blank throws up the error message box

        :param event: User clicks on the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.undo_last_button:  # If user clicked on area
            # containing the undo last button
            if len(self.master.images) <= 1:    # If there is less than or equal to 1 image in the stack
                if len(self.master.images) == 1:    # If there is one image
                    self.master.images.pop()    # remove that image from the stack
                self.master.display_image.clear_canvas()    # MAke the display screen blank
            else:    # If there are more than one images in the stack
                self.master.images.pop()    # Remove the most recent image
                self.master.display_image.display_image(img=self.master.images[-1])  # Display the next most recent
                # image on the screen

    def undo_all_released(self, event):
        """
        Describes behaviour of undo all button when the user clicks on it. It undos all the transformations that were
        applied to the image. If screen is blank throws up the error message box

        :param event: User clicks on the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.undo_all_button:  # If clicked area contains the
            # undo all button
            if self.image_present_check():    # Continue if images are present in the stack, else throw error messagebox
                first_img = self.master.images[0]    # The original image in the stack
                self.master.display_image.display_image(img=first_img)    # Display the first image on the screen
                self.master.images = [first_img]    # Edit the stack to now contain only the first image, removing
                # all the other transformed images

    def equalize_button_released(self, event):
        """
        Describes behaviour of equalize button when the user clicks on it. It equalizes the histogram of the displayed
        image. If screen is blank throws up the error message box

        :param event: User clicks on the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.equalize_button:  # If clicked area contains the
            # equalize button
            if self.image_present_check():    # If stack contains images. Else throw the error message box
                img = self.master.images[-1]    # Select the displayed image
                hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)    # Convert it into HSV type
                transformed_dim = equalisation.histogram_eq(hsv_image[:, :, 2])    # Use the 'V' channel for
                # transformation. Apply histogram equalization to it
                hsv_image[:, :, 2] = transformed_dim    # Change the 'V' channel of the original image to the
                # equalized V channel
                color_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)    # Convert the image into BGR format
                self.master.display_image.display_image(img=color_image)    # Display this transformed image
                self.master.images.append(color_image)    # Append this image to the stack

    def gamma_correct_released(self, event):
        """
        Describes behaviour of gamma correct button when the user clicks on it. It shows a slider for the user to select
        the gamma value. Once that value is selected it applies the gamma correcting algorithm. If screen is blank throws up the error message box

        :param event: User clicks on the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.gamma_correct_button:  # If clicked area contains
            # the gamma correct button
            if self.image_present_check():    # Check if an image is being displayed
                self.horizontal = Scale(self, from_=0.00, to=3.00, resolution = 0.25, orient=HORIZONTAL)  # Invoke a
                # horizontal slider for user to choose gamma
                self.horizontal.pack()    # Pack it to the GUI
                gamma_button = Button(self, text="Set Gamma", command=self.gamma_slide).pack()    # Button which the
                # user can press to select gamma. On clicking button, gamma_slide function will be called.

    def gamma_slide(self):
        """
        This is called when the gamma_button is clicked. This performs the gamma correct transformation on the image.
        """
        gamma_input = self.horizontal.get()    # Get the user input of gamma
        img = self.master.images[-1]    # Choose the displayed image to perform gamma correcting
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)    # Convert the BGR to HSV type
        transformed_dim = gamma.gamma_correct(hsv_image[:, :, 2], gamma_input)   # Perform gamma correcting on the
        # 'V' channel
        hsv_image[:, :, 2] = transformed_dim    # Set the 'V' channel of the original image as the gamma corrected one
        color_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)    # Reconvert back the image to BGR
        self.master.display_image.display_image(img=color_image)    # Display the reconverted image on the screen
        self.master.images.append(color_image)    # Append the transformed image to the stack

    def log_transform_released(self, event):
        """
        Describes behaviour of log transform button when the user clicks on it. It performs log transformation on the 
        current image. If screen is blank throws up the error message box.
        
        :param event: User clicks on the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.log_transform_button:  # If clicked area contains 
            # the log transform button
            if self.image_present_check():    # Checks if there is a displayed image present, if not throws up error box
                img = self.master.images[-1]    # The displayed image is selected to be log transformed
                hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)    # Convert the BGR image to HSV
                transformed_dim = log_transform.log_trans(hsv_image[:, :, 2])    # Perform log transformation on the 'V'
                # channel
                hsv_image[:, :, 2] = transformed_dim  # Set the 'V' channel of the original image as log transformed
                color_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)    # Re convert the image back to BGR
                self.master.display_image.display_image(img=color_image)    # Display the transformed image on 
                # GUI screen
                self.master.images.append(color_image) # Append the transformed image to the stack

    def blur_released(self, event):
        """
        Describes behaviour of blur button when the user clicks on it. It uses a horizontal slider to get the user input
        to set the standard deviation of the gaussian kernel. It then performs gaussian blurring on the displayed image. 
        If screen is blank throws up the error message box
        
        :param event: User clicks on the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.blur_button:  # If clicked area has the blur button
            if self.image_present_check():    # Check if there is a displayed image else throw an error box
                self.horizontal = Scale(self, from_=0.00, to=100.00, resolution = 0.5, orient=HORIZONTAL)    # Invoke a 
                # slider to take the user input for standard deviation
                self.horizontal.pack()    # Pack it onto GUI screen
                blur_button = Button(self, text="Set STD of Gaussian Window", command=self.blur_slide).pack()  # Button 
                # for the user to input their chosen value. When the user clicks it blur_slide function is called

    def blur_slide(self):
        """
        Function called when the user presses the blur_button. It performs gaussian blurring on the image.
        """
        std_input = self.horizontal.get()  # Get the user STD input
        img = self.master.images[-1]    # Select the displayed image for transformation
        blurred_image = blur.gaussian_blur(img, std_input)    # Perform gaussian blurring on the input image
        self.master.display_image.display_image(img=blurred_image)    # display the blurred image
        self.master.images.append(blurred_image)    # Append the blurred image to the stack

    def sharpening_released(self, event):
        """
        Describes behaviour of sharpening button when the user clicks on it. It invokes two sliders to get the user 
        input for the std of gaussian kernel and the constant for multiplication. It then performs unsharp masking on 
        the displayed image. If screen is blank throws up the error message box
        
        :param event: User clicks on the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.sharpening_button: # If clicked area contains the 
            # sharpening button
            if self.image_present_check():   # Check if image is being displayed, if not throw error box.
                self.horizontal = Scale(self, from_=0.00, to=100.00, resolution = 0.5, orient=HORIZONTAL) # Slider for 
                # taking the STD of gaussian kernel
                self.horizontal.pack()    # pack the slider onto GUI screen
                self.vertical = Scale(self, from_=0.00, to=100.00, resolution = 0.5, orient=VERTICAL) # Slider for
                # taking the value of the constant
                self.vertical.pack()    # pack the slider onto GUI screen
                sharpen_button = Button(self, text="Set sharpening constants", command=self.sharpen_slide).pack()
                # Button which the user clicks to set the input. On clicking, the sharpen_slide function is called

    def sharpen_slide(self):
        """
        Invoked when the sharpen_button is pressed. Performs unsharp masking on the displayed image using gaussian blur
         with STD set by the user. The constant multiplied is also determined by the user.
        """
        std_input = self.horizontal.get()    # Get the std defined by user
        c_input = self.vertical.get()    # get the constant defined by the user
        img = self.master.images[-1]    # Use the most recent displayed image for sharpening
        sharpened_image = sharpen.gaussian_unsharp_masking(img, std_input, c_input)    # Apply unsharp masking on image
        self.master.display_image.display_image(img=sharpened_image)    # display sharpened image
        self.master.images.append(sharpened_image)     # Append the sharpened image on the stack

    def edge_detector_released(self, event):
        """
        Describes behaviour of edge_detector button when the user clicks on it. It performs sobel edge detection
        on the displayed image. If screen is blank throws up the error message box
        
        :param event: User clicks on the button
        """
        if self.winfo_containing(event.x_root, event.y_root) == self.edge_detector_button:  # Clicked area has edge
            # detector button
            if self.image_present_check():    # Check if image is displayed, else throw error message box
                self.horizontal = Scale(self, from_=0.00, to=255.00, resolution = 0.5, orient=HORIZONTAL)  # Slider for
                # adjusting the threshold of Sobel Detector
                self.horizontal.pack()   # Pack the slider in the GUI window
                edge_detect_button = Button(self, text = "Set threshold", command = self.edge_detect_slide).pack()
                # Button for the user to change the threshold. It will call edge_detect_slide whenever
                # the button is pressed

    def edge_detect_slide(self):
        """
        This is called whenever the edge_detect_button is pressed. This performs the sobel edge detection
        on the displayed image
        """
        img = self.master.images[-1]    # Use the displayed image to perform edge detection
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # Convert BGR image to Grayscale
        transformed_dim = edge_detector.edge_detector(gray_image, self.horizontal.get())    # Perform sobel edge
        # detection on grayscale image
        transformed_dim = transformed_dim.astype('float32')  # Convert the transformed image into 8 bit float
        color_image = cv2.cvtColor(transformed_dim, cv2.COLOR_GRAY2BGR)    # Convert the grayscale transformed image
        # back to BGR
        self.master.display_image.display_image(img=color_image)    # Display the edge map
        self.master.images.append(color_image)    # Append the displayed image to the stack
