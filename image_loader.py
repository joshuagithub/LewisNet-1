import numpy as np
from math import floor
import glob
from PIL import Image

def load_images(paths, resize=False, remove_alpha=False):
    """Take a glob pattern for images and load into a 4-D numpy array, converted to grayscale"""
    if type(paths) == str:
        file_names = glob.glob(paths)
    elif type(paths) == list:
        file_names = []
        for path in paths:
            for file_name in glob.glob(path):
                file_names.append(file_name)
    else:
        raise ValueError("cannot load: " + str(paths))

    list_of_image_2d_arrays = []
    for name in file_names:
        im = Image.open(name)
        if remove_alpha and (im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)):
            im = alpha_to_white(im)
        else:
            im = im.convert("L")
        if (resize and im.size != (150, 150)):
            im = resize_image(im)
        arr = np.array(im)
        list_of_image_2d_arrays.append(arr)
    to_3d_array_of_images = np.array(list_of_image_2d_arrays)
    to_4d_array_of_images = to_3d_array_of_images[:,:,:,np.newaxis]
    return to_4d_array_of_images

def resize_image(im):
    aspect_ratio = im.size[0] / im.size[1]
    newIm = Image.new("L", size=(150, 150), color=255)
    if (aspect_ratio > 1):
        im = im.resize((150, floor(150 / aspect_ratio)), Image.ANTIALIAS)
        margin = floor((150 - im.size[1]) / 2)
        newIm.paste(im, (0, margin, 150, 150 - margin))
    else:
        im = im.resize((floor(150 * aspect_ratio), 150), Image.ANTIALIAS)
        margin = floor((150 - im.size[0]) / 2)
        newIm.pase(im, (margin, 0, 150 - margin, 150))
    return newIm

def alpha_to_white(im):
    laIm = im.convert("LA") # grayscale with alpha
    imWhite = Image.new("L", im.size, color=255)
    imWhite.paste(laIm, mask=im) # use the original image as its own transparency mask
    return imWhite

