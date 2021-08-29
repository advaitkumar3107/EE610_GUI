import numpy as np


def gamma_correct(img, gamma):
    """
    Performs gamma correction on the input image intensities
    :param img: Input image intensities
    :param gamma: Correction factor
    :return: gamma_img: Output gamma corrected image
    """
    gamma_img = np.power(img, 1.0/gamma)                        # gamma corrected image = (original image)^(1/gamma)
    gamma_img = 255.0*gamma_img/np.max(gamma_img)          # Adjusting range of output image
    return gamma_img    # return the gamma corrected image
