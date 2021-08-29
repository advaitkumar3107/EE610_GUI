import numpy as np
from convolution import convolution


def edge_detector(img, threshold = 100):
    """
    Returns the image with Sobel Edge Detection algorithm applied

    :param img: Input image
    :param threshold: The threshold to be applied on the gradient values
    :return: gradient_map: Edges detected of the input image
    """

    gradient_kernel_x = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])    # Kernel giving derivative in X direction
    gradient_kernel_y = np.flip(gradient_kernel_x.T, axis=0)    # Kernel giving derivative in Y direction

    gradient_x = convolution(img, gradient_kernel_x)    # Calculating gradient in X direction
    gradient_y = convolution(img, gradient_kernel_y)    # Calculating gradient in Y direction

    gradient_mag = np.sqrt(np.square(gradient_x) + np.square(gradient_y))    # Calculating the pixelwise magnitude of
    # the gradient in the spatial domain
    gradient_mag *= 255.0/gradient_mag.max()    # normalising the gradient so that its magnitude values lie in [0,255]
    gradient_mag[gradient_mag >= threshold] = 255.0    # Hard thresholding the gradient using the input threshold value
    gradient_mag[gradient_mag < threshold] = 0.0    # Hard thresholding

    return gradient_mag    # Returning the thresholded edge map
