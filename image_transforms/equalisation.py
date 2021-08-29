import numpy as np


def create_histogram(img_channel, bins = 256):
    """
    Creates a histogram for the input image channel

    :param img: Input image channel
    :param bins: Number of different pixel intensities
    :return: hist: Histogram of pixel intensities
    """
    img_channel = img_channel.astype('uint8')    # Change the pixels datatype from float to int so that discrete values
    # can be counted
    hist = np.zeros(bins)  # This will be the histogram with size = number of bins. Initialised to all zeros

    for i in img_channel:  # Iterating over all pixels of input channel
        hist[i] += 1  # If pixel intensity is 'i' then corresponding frequency bin in
        # histogram is incremented by 1

    return hist  # Return the output (histogram)


def cumulative_hist(histogram):
    """
    Creates a cumulative histogram out of the input histogram (equalisation)

    :param histogram: Input histogram
    :return: cum: Cumulative histogram
    """
    cum = [histogram[0]]                   # initializing the list which will hold the cumulative frequencies

    for i in range(1, len(histogram)):
        cum.append(histogram[i] + cum[-1])  # cum[i] = histogram[0] + histogram[1] + .. + histogram[i]
        # Hence cum[i] = cum[i-1] + histogram[i]

    cum = np.array(cum)                   # Cast the list to an array
    rnge = np.max(cum) - np.min(cum)              # Total number of pixels in image
    cum = (cum * (len(histogram) - 1))/rnge  # normalizing the histogram
    return cum                            # Return the normalized cumulative histogram


def histogram_eq(img):
    """
    Performs complete histogram equalisation for input images

    :param img: Input image
    :return: equalized_img: Equalised image
    """
    flattened_img = img.flatten().astype('uint8')   # Image is flattened to one dimension and pixels converted to int
    # to create histogram
    histogram = create_histogram(img)   # Histogram created by using above function
    cumulative_histogram = cumulative_hist(histogram).astype('uint8')   # Cumulative histogram created and cast to int
    transformed_img = cumulative_histogram[flattened_img]   # image transformed using the equalized histogram values
    equalized_img = np.reshape(transformed_img, img.shape)   # Reshape the flattened image to original shape

    return equalized_img   # Return the equalized image
