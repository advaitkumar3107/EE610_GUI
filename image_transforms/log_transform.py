import numpy as np


def log_trans(img):
    """
    Function takes the input image and returns its log transform
    taken to the base 2

    :param img: Image
    :return: log_img: Log transformed image
    """
    c = 255.0/np.log2(1 + np.max(img))   # Constant used for normalising the image so that the pixels lie in [0,255]
    log_img = np.log2(1 + img)  # s(r) = log_2(1+r) for log transformation
    log_img = c*log_img    # Normalising the log transformed image using above constant
    return log_img    # Return the log transformed image


