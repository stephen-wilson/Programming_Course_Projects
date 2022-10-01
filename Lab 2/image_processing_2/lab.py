#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from xml.dom import minidom
from PIL import Image


# VARIOUS FILTERS

# From lab 1
def get_pixel(image, x, y, oob_behavior=None):
    """
    Returns the pixel in image['pixels'] at row index x and column index y.
    
    
    Input:
    Dict: image
    int: x - row index
    int: y - column index
    str: oob_behavior - "zero", "extend", "wrap" are valid inputs; default is None.
        Describes different out-of-bounds behaviors when retrieving pixel values.
    
    Return:
    int/float: value of the x,y pixel
    """
    ## NOTE: x = row_idx, y = col_idx
    # 1-d array idx = x * image['width'] + y
    
    ## flatten 2-d array to 1-d array: row_idx * width + col_idx
    idxfunc = lambda row_idx, col_idx: row_idx * image['width'] + col_idx
    last_row_idx = image['height'] - 1
    last_col_idx = image['width'] - 1
    if (0 <= x < image['height']) and (0 <= y < image['width']):
            return image['pixels'][idxfunc(x,y)]
    elif oob_behavior == "zero":
        return 0
    elif oob_behavior == "extend":
        # Address corner cases
        if x <= 0:
            if y <= 0:
                return image['pixels'][idxfunc(0,0)]
            elif y >= last_col_idx:
                return image['pixels'][idxfunc(0,last_col_idx)]
            else:
                return image['pixels'][idxfunc(0, y)]
        elif x >= last_row_idx:
            if y <= 0:
                return image['pixels'][idxfunc(last_row_idx, 0)]
            elif y >= last_col_idx:
                return image['pixels'][idxfunc(last_row_idx, last_col_idx)]
            else:
                return image['pixels'][idxfunc(last_row_idx, y)]
        ##
        # Address side cases
        else:
            if y <= 0:
                return image['pixels'][idxfunc(x, 0)]
            elif y >= last_col_idx:
                return image['pixels'][idxfunc(x, last_col_idx)]
            
        
    elif oob_behavior == "wrap":
        new_y = y
        new_x = x
        
        if y < 0:
            new_y = y + image['width']
        elif y >= image['width']:
            new_y = y - image['width']
            
        if x < 0:
            new_x = x + image['height']
        elif x >= image['height']:
            new_x = x - image['height']
        
        return image['pixels'][idxfunc(new_x, new_y)]
    elif oob_behavior == None:
        return 0
    


def set_pixel(image, x, y, c):
    idx = x * image['width'] + y
    image['pixels'][idx] = c


def apply_per_pixel(image, func):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0]*(image['height']*image['width']),
    }
    for x in range(image['height']): # rows
        for y in range(image['width']): # cols
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, x, y, newcolor)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda c: 255-c)


# HELPER FUNCTIONS

def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings 'zero', 'extend', or 'wrap',
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of 'zero', 'extend', or 'wrap', return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with 'height', 'width', and 'pixels' keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    Dict: kernel = {'height': height, 'width': width, 'pixels': [...]}
    
    Kernels are square matrices. The center pixel is (height - 1 / 2, width - 1 /2),
    height = width.
    Kernel pixels are an array of values.
    """
    midpoint = (kernel['height'] - 1) // 2 # given that kernels are always square and have odd number components.
    # print(midpoint)
    # looping through each x and y value in the image in order, creating a new value correlated with the filter,
    # then appending to the new array O(n^4)
    filtered_pixels = []
    for x in range(image['height']):
        for y in range(image['width']):
            # sum each pixel obtained from the correlation of the kernel on the image for each row and col index in kernel
            # w.l.o.g. x - midpoint shifts the x position to the end of the kernel space, then + row_idx moves accross the width
            filtered_pixels.append(
                sum(get_pixel(image, x - midpoint + row_idx, y - midpoint + col_idx, boundary_behavior) *
                                       get_pixel(kernel, row_idx, col_idx, 'zero')
                    for row_idx in range(kernel['height']) for col_idx in range(kernel['width'])))
    
    filtered_image = {'height': image['height'], 'width': image['width'], 'pixels': filtered_pixels}
    return filtered_image

def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    image['pixels'] = list(map(lambda pixel: 0 if pixel < 0 else 255 if pixel > 255 else round(pixel), image['pixels']))
    return image

def create_kernel(kernel, dim):
    """
    Takes a kernel in string format and converts to an image representation.
    
    Inputs:
    Str: kernel as string with spaces
    Int: dim - dimensions of the kernel dim x dim
    
    Returns:
    Dict: kernel representation in 6.101 image format
    """
    kernel_pixels = []
    # split the multi-line string by the newline character
    split_kernel = kernel.split('\n')
    for row_idx in range(len(split_kernel)):
        # split the row in the array by the spaces for the elements inside,
        # then cast those elements to ints through map() and then convert to list and assign to 
        # current row
        split_kernel[row_idx] = list(map(lambda num: int(num), split_kernel[row_idx].split(' ')))
        kernel_pixels.extend(split_kernel[row_idx]) # attaches the current iterable row of split_kernel
                                                    # to the existing kernel_pixels array
        
    kernel_repr = {'height': dim, 'width': dim, 'pixels': kernel_pixels}
    return kernel_repr

def generate_kernel(dim):
    """
    Generates kernel of dim x dim size for box blur.
    
    Inputs:
    Int: dim - dimensions of square kernel
    
    Returns:
    Dict: kernel in the 6.101 image representation 
    """
    # generate list of 1/dim^2 elements, dim^2 times for flat array of box blur kernel
    pixels = [1/(dim*dim)]*(dim*dim)
    return {'height': dim, 'width': dim, 'pixels': pixels} 

def generate_sharpened_kernel(dim):
    """
    Generates dim x dim sharpen matrix by the equation 2*I - B, for I = original image, B = Blurred image
    Combined into one kernel 
    """
    midpoint = (dim - 1) // 2
    idx = midpoint * dim + midpoint
    pixels = [0 - (1/dim**2)]*(dim**2)
    pixels[idx] += 2
    return {'height': dim, 'width': dim, 'pixels': pixels} 

# FILTERS
    
def edges(image):
    """
    Return a new image with the edges emphasized using the Sobel Operator.
    This should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    kernelx = {'height': 3, 'width': 3, 'pixels': [-1,0,1,
                                                   -2,0,2,
                                                   -1,0,1]}
    kernely = {'height': 3, 'width': 3, 'pixels': [-1,-2,-1,
                                                   0,0,0,
                                                   1,2,1]}
    
    correlationx = correlate(image, kernelx, 'extend')
    correlationy = correlate(image, kernely, 'extend')
    output_pixels = [round((ox**2 + oy**2)**(1/2)) for ox, oy in zip(correlationx['pixels'], correlationy['pixels'])]
    output_image = {'height': correlationx['height'], 'width': correlationx['width'], 'pixels': output_pixels}
    return round_and_clip_image(output_image)

# Lab 2 Material
def color_to_greyscale_images(image):
    """
    Given a color image in RGB format, converts to three greyscale images by separating each
    red, green and blue channel.
    
    Parameters:
    image (dict) : color image
    Example:
    i = {
        'height': 3,
        'width': 2,
        'pixels': [(255, 0, 0), (39, 143, 230), (255, 191, 0),
                (0, 200, 0), (100, 100, 100), (179, 0, 199)],
    }
    
    Returns:
    greyscale_images (tuple) : a tuple of 3 greyscale images in 6.101 format, each with R, G, or B
        channels, respectively.
    """
    height = image['height']
    width = image['width']
    original_pixels = image['pixels'].copy()
    red_pixels = []
    green_pixels = []
    blue_pixels = []
    for pixel in original_pixels:
        red_pixels.append(pixel[0])
        green_pixels.append(pixel[1])
        blue_pixels.append(pixel[2])
        
    return ({'height': height, 'width': width, 'pixels': red_pixels}, 
            {'height': height, 'width': width, 'pixels': green_pixels},
            {'height': height, 'width': width, 'pixels': blue_pixels})
        
    

def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def color_image_filter(image):
        """
        Given a color image, converts that color image to three separate greyscale images,
        applies the greyscale filter to them individually, then combines them into a color image
        format and returns the filtered color image.
        This should not modify the original image.
        
        Returns:
        filt_color_image (dict) : filtered color image
        """
        red_greyscaled, green_greyscaled, blue_greyscaled = color_to_greyscale_images(image)
        
        # apply greyscale filter to each color channel represented as a greyscale image
        red_filtered = filt(red_greyscaled)
        green_filtered = filt(green_greyscaled)
        blue_filtered = filt(blue_greyscaled)
        
        # Combine the color channels back to create an RGB image again
        rgb_pixels = [(r, g, b) for r,g,b in zip(red_filtered['pixels'], green_filtered['pixels'], blue_filtered['pixels'])]
        
        return {'height': image['height'], 'width': image['width'], 'pixels': rgb_pixels}
        
    
    return color_image_filter


def make_blur_filter(n):
    """"
    Given a kernel size n as an argument to the blur filter, creates a blur filter that
    works in conjunction with the greyscale to color image filter that only takes one argument.
    
    Returns:
    color_blur_filter (func) : blur filter that works with color representation
    """
    def blurred(image):
        """
        Return a new image representing the result of applying a box blur (with
        kernel size n) to the given input image.

        This process should not mutate the input image; rather, it should create a
        separate structure to represent the output.
        """
        N = n
        # first, create a representation for the appropriate n-by-n kernel (you may
        # wish to define another helper function for this)
        kernel = generate_kernel(N)

        # then compute the correlation of the input image with that kernel
        correlation = correlate(image, kernel, 'extend')

        # and, finally, make sure that the output is a valid image (using the
        # helper function from above) before returning it.
        return round_and_clip_image(correlation)
    
    return blurred
    


def make_sharpen_filter(n):
    """"
    Given a kernel size n as an argument to the blur filter, creates a blur filter that
    works in conjunction with the greyscale to color image filter that only takes one argument.
    
    Returns:
    color_blur_filter (func) : blur filter that works with color representation
    """
    def sharpened(image):
        """
        Return a new image representing the result of applying an unsharpen mask (with
        kernel size n) to the given input image.

        This process should not mutate the input image; rather, it should create a
        separate structure to represent the output.
        """
        N = n
        kernel = generate_sharpened_kernel(N)
        
        correlation = correlate(image, kernel, 'extend')
        
        return round_and_clip_image(correlation)
    
    return sharpened


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    def apply_filters(image):
        """
        Applies each filter in filters to the input image, and then sets the new filtered_image
        object to the filtered image that is returned from the filter.
        """
        filtered_image = image
        for filter in filters:
            filtered_image = filter(filtered_image)
        return filtered_image
    return apply_filters
        


# SEAM CARVING

# Main Seam Carving Implementation


def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image. Returns a new image. Without
    modifying the original image.
    """
    carved_image = {'height': image['height'], 'width': image['width'], 'pixels': image['pixels'].copy()}
    
    cols_removed = 0
    for _ in range(ncols):
        carved_image = image_without_seam(carved_image, minimum_energy_seam(cumulative_energy_map(
            compute_energy(greyscale_image_from_color_image(carved_image)))))
        
        cols_removed += 1
        if cols_removed % 10 == 0:
            print(f'{cols_removed} seams removed...')
        
    print(f'Done!')
    return carved_image

# Optional Helper Functions for Seam Carving


def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    grey_pixels = []
    pixels = image['pixels'].copy()
    grey_pixels = [round(.299*r + .587*g + .114*b) for r,g,b in pixels]
    
    return {'height': image['height'], 'width': image['width'], 'pixels': grey_pixels}
    


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey)


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    cum_energy_pixels = energy['pixels'].copy()
    for idx in range(len(cum_energy_pixels)):
        if idx >= energy['width']:
            # left side
            if idx % energy['width'] == 0:
                cum_energy_pixels[idx] += min(cum_energy_pixels[idx - energy['width']], 
                                              cum_energy_pixels[idx - energy['width'] + 1])
            # right side
            elif idx % energy['width'] == energy['width'] - 1:
                cum_energy_pixels[idx] += min(cum_energy_pixels[idx - energy['width'] - 1], 
                                              cum_energy_pixels[idx - energy['width']])
            # any other location inside
            else:
                cum_energy_pixels[idx] += min(cum_energy_pixels[idx - energy['width'] - 1], 
                                              cum_energy_pixels[idx - energy['width']], 
                                              cum_energy_pixels[idx - energy['width'] + 1])
                
    return {'height': energy['height'], 'width': energy['width'], 'pixels': cum_energy_pixels}
    
def find_min(row, adjecent_idxs=None):
    """
    Given a row in the cem and the adjecent indices of the previous min,
    finds the min value and returns its index.
    """
    
    min = 2**32
    min_idx = 0
    for i in range(len(row)):
        if adjecent_idxs != None:
            if i in adjecent_idxs:
                if min == None:
                    min = row[i]
                    min_idx = i
                elif row[i] < min:
                    min = row[i]
                    min_idx = i
        else:
            if row[i] < min:
                min = row[i]
                min_idx = i
    
    return min_idx

def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    cem_pixels = cem['pixels'].copy()
    # start from bottom, then move to top
    row_start_idx = len(cem_pixels) - cem['width']
    row_end_idx = len(cem_pixels) - 1
    min_energy_seam_idxs = []
    
    adjecent_idxs = []
    min_idx = 0
    while row_start_idx >= 0:
        row = cem_pixels[row_start_idx:row_end_idx+1]
        if adjecent_idxs:
            min_idx = find_min(row, adjecent_idxs)
            # set new adjecent indices
            if row_start_idx != 0:
                if min_idx == 0:
                    adjecent_idxs = [min_idx, min_idx + 1]
                elif min_idx == len(row) - 1:
                    adjecent_idxs = [min_idx - 1, min_idx]
                else:
                    adjecent_idxs = [min_idx - 1, min_idx, min_idx + 1]
        else:
            min_idx = find_min(row)
            # set new adjecent indices
            if min_idx == 0:
                adjecent_idxs = [min_idx, min_idx + 1]
            elif min_idx == len(row) - 1:
                adjecent_idxs = [min_idx - 1, min_idx]
            else:
                adjecent_idxs = [min_idx - 1, min_idx, min_idx + 1]
            
        min_energy_seam_idxs.append(row_start_idx + min_idx)
        # going to next row above
        row_start_idx -= cem['width']
        row_end_idx -= cem['width']
        
    return min_energy_seam_idxs
        
    
         


def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    no_seam_pixels = image['pixels'].copy()
    for idx in seam:
        del no_seam_pixels[idx]
        
    return {'height': image['height'], 'width': image['width'] - 1, 'pixels': no_seam_pixels}


def custom_feature(image):
    """
    This is a (vertical) emboss filter. It will take the input image and create an image
    embossing that highlights the areas where pixel changes occur in the vertical direction, 
    such as a sudden change of color from black to white.
    """
    kernel = {'height': 3, 'width': 3, 'pixels': [0, +1, 0,
                                                  0, 0, 0,
                                                  0, -1, 0]}
    
    out_image = correlate(image, kernel, 'extend')
    
    # add 128 to each pixel value to give the grey background
    return {'height': out_image['height'], 'width': out_image['width'], 'pixels': list(map(lambda pix: pix+128, out_image['pixels']))}

# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES


def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img = img.convert("RGB")  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {"height": h, "width": w, "pixels": pixels}


def save_color_image(image, filename, mode="PNG"):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError("Unsupported image mode: %r" % img.mode)
        w, h = img.size
        return {"height": h, "width": w, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    # image = load_color_image("Lab 2\image_processing_2\\test_images\\python.png")
    # save_color_image(color_filter_from_greyscale_filter(make_blur_filter(9))(image), "blurred_python.png")
    # image2 = load_color_image("Lab 2\image_processing_2\\test_images\\sparrowchick.png")
    # save_color_image(color_filter_from_greyscale_filter(make_sharpen_filter(7))(image2), "sharpened_sparrowchick.png")
    
    # filter1 = color_filter_from_greyscale_filter(edges)
    # filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))
    # filt = filter_cascade([filter1, filter1, filter2, filter1])
    emboss = color_filter_from_greyscale_filter(custom_feature)
    image = load_color_image("Lab 2\\image_processing_2\\test_images\\chess.png")
    save_color_image(emboss(image), "embossed_chess.png")
