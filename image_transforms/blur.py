import numpy as np
from convolution import convolution
from scipy import signal


def gaussian_blur(img, std):
    """
    Performs gaussian blurring on the input image with a kernel having std as passed in the function

    :param img: Input image
    :param std: Standard Deviation of kernel
    :return: output: Output smoothened image
    """
    kernel = np.zeros((5, 5))    # Gaussian kernel of 5x5 size
    m = 2    # m = kernel_height//2 for iteration
    n = 2    # n = kernel_width//2 for iteration

    for x in range(-m, m+1):    # Iterating over the rows of the kernel
        for y in range(-n, n+1):    # Iterating over the columns of the kernel
            kernel[m+x, n+y] = np.exp(-(x**2 + y**2)/(2 * std ** 2))/np.sqrt(2 * np.pi * (std ** 2))  # Calculating the
            # kernel value at location [m+x, n+y] using the gaussian distribution centred at the centre of the kernel
            # and having std equivalent to the one passed in the function

    output = np.zeros_like(img, dtype = np.float32)    # output image matrix

    for i in range(3):    # Iterating over all the channels of the output image
        output[:,:,i] = convolution(img[:,:,i], kernel)    # Performing gaussian convolution over each channel
    return output    # Returning the gaussian blurred image.
