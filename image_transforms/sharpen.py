from image_transforms.blur import gaussian_blur


def gaussian_unsharp_masking(img, std, c):
    """
    Performs Unsharp Masking using the input image and a gaussian blurring kernel

    :param img: Input image
    :param std: Standard Deviation of the Gaussian Kernel
    :param c: Constant which needs to be multiplied with the blurred image while subtracting
    :return: sharpened_img: Output sharpened image
    """
    blurred_image = gaussian_blur(img, std)    # Performing gaussian blurring
    sharpened_img = img - c*blurred_image    # Performing unsharp masking. Using a constant while subtracting
    # which is fed by the user
    sharpened_img = sharpened_img.clip(0, 255)    # Clipping the values to between 0, 255
    return sharpened_img    # Returning the sharpened image
