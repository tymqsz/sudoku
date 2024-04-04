from PIL import Image
import numpy as np


# extract pixels from given image and save it as np.array
def get_pixels(img):
    width, height = img.size
    pixels = np.zeros((width, height))
    for y in range(height):
        for x in range(width):
            pixels[x, y] = img.getpixel((y, x))

    return pixels


# check if index doesnt go out of images bounds
def good_index(index, size):
    x, y = index[0], index[1]

    if x < 0 or y < 0 or x >= size[0] or y >= size[1]:
        return False 
    return True

# get part of image the same size as kernel_size
def get_matrix(kernel_size, pixels, pivot):
    ext = (kernel_size-1)//2
    matrix = np.zeros((kernel_size, kernel_size))

    i, j = 0, 0
    for x in range(pivot[0]-ext, pivot[0]+ext+1):
        j = 0
        for y in range(pivot[1]-ext, pivot[1]+ext+1):
            if good_index((x, y), pixels.shape):
               matrix[i, j] = pixels[x, y]
            j += 1
        i += 1
    
    return matrix

# apply convolution
def get_val(M1, M2):
    val = 0
    
    for x in range(M1.shape[0]):
        for y in range(M1.shape[0]):
            val += (M1[x, y] * M2[x, y])

    return val

# transform image
def transform(kernel: np.array, img):
    width, height = img.size
    transformed = Image.new(size=(width, height), mode="L")

    for x in range(width):
        for y in range(height):
            original = get_matrix(kernel.shape[0], get_pixels(img), (x, y))
            val = get_val(original, kernel)
            transformed.putpixel((y, x), int(val))
    
    return transformed
