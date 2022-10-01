#!/usr/bin/env python3

import math
from posixpath import split
from turtle import width
from venv import create

from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!

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

def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    kernel = generate_kernel(n)

    # then compute the correlation of the input image with that kernel
    correlation = correlate(image, kernel, 'extend')

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    return round_and_clip_image(correlation)

def sharpened(image, n):
    """
    Return a new image representing the result of applying an unsharpen mask (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    kernel = generate_sharpened_kernel(n)
    
    correlation = correlate(image, kernel, 'extend')
    
    return round_and_clip_image(correlation)
    
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

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_greyscale_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    # image = load_greyscale_image("Lab 1\image_processing\image_processing\\test_images\\pigbird.png")
    # image = {'height': 2, 'width': 2, 'pixels': [-1.2, 2, -340.587, 3435]}
    # save_greyscale_image(inverted(image), "inverted_bluegill.png")
    # round_and_clip_image(image)
    # print(image['pixels'])
    # print(get_pixel(image, -232323, -33434, oob_behavior="extend"))
    # print(get_pixel(image, 0, 0, oob_behavior="wrap"))
#     str_kernel = """0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 0
# 1 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 0"""

    # kernel = create_kernel(str_kernel, 13)
    # save_greyscale_image(round_and_clip_image(correlate(image, kernel, 'zero')), "pigbird_zero.png")
    # save_greyscale_image(round_and_clip_image(correlate(image, kernel, 'extend')), "pigbird_extend.png")
    # save_greyscale_image(round_and_clip_image(correlate(image, kernel, 'wrap')), "pigbird_wrap.png")
    # print(load_greyscale_image("Lab 1\image_processing\image_processing\\test_images\\centered_pixel.png"))
    
    image = load_greyscale_image("Lab 1\image_processing\image_processing\\test_images\\construct.png")
    save_greyscale_image(edges(image), "edges_construct.png")
    
