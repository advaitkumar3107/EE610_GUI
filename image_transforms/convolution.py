import numpy as np
from skimage.util.shape import view_as_windows


def convolution(img, kernel):
    """
    Performs vectorized convolution between image and kernel. It uses 'reflection' padding on the image
    :param img: Input 2D image
    :param kernel: Convolution kernel
    :return: convoluted: Output convolved image
    """
    h, w = kernel.shape  # Get the height and width of kernel
    padded_img = np.pad(img, (((h-1)//2, (h-1)//2), ((h-1)//2, (h-1)//2)), mode='reflect')  # pad the image
    # in such a way that dimension of output image equals dimension of input
    sub_matrices = view_as_windows(padded_img, (h,w), 1)   # break the padded image into windows that are of the same
    # size as the kernel with stride = 1
    convoluted = np.einsum('ij,klij->kl',kernel,sub_matrices)  # This multiplies the windows with the kernel elementwise
    # and adds the resultant elements of the matrix to give the output convolved image
    return convoluted   # Return the convolved image
