"""
Support file for the Vesuvius Basic Compression script.
Most of these are wrappers for cv2 functions alongside  
some experimental mask generation functions.

Dependencies
------------
Libraries: os, cv2 and numpy
"""

import os
import cv2
import numpy as np


def load_image(path, grayscale=True):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if image.shape[-1] == 3 and grayscale:
        return np.average(image, axis=2)
    return image

def save_image(image, path):
    cv2.imwrite(path, image)

def check_path(path):
    if not os.path.isfile(path):
        print(f'Error - Source file ({path}) could not be found.')
        return False
    return True

def clip(image, clip_min, clip_max):
    image[image<clip_min] = clip_min
    image[image>clip_max] = clip_max
    return (image-clip_min)/(clip_max-clip_min)

def set_to_int8(image):
    return (image*255).astype('uint8')

def blur_image(image, kernel):
    return cv2.filter2D(src=image, ddepth=-1, kernel=kernel)


# NOT CURRENTLY USEABLE! WORK IN PROGRESS!
def create_mask(image):
    clip_red = clip(image, 60, image.max())
    clipped = set_to_int8(clip_red)
    #save_image(image=clipped, path=f'05500_mask_early.png')
    for i in range(0, 5):
        # Initial blur to smooth pixel local pixel differences...
        blurred_1 = blur_image(clipped, np.ones((10, 10), np.float32)/100)
        # Second blur to get averages of larger local environments.
        blurred_2 = blur_image(clipped, np.ones((80, 80), np.float32)/6400)
        diff = np.abs(blurred_1.astype('int16') - blurred_2.astype('int16'))

        diff = (clipped - 2*diff)
        diff[diff < 0] = 0

        clip_blur = clip(diff, diff.min(), diff.max())
        clipped = set_to_int8(clip_blur)

    blur_final = blur_image(clipped, np.ones((60, 60), np.float32)/3600)
    clip_final = clip(blur_final, blur_final.min(), blur_final.max())
    red_final = set_to_int8(clip_final)
    red_final[red_final<130] = 0
    red_final[red_final>0] = 255
    return red_final

def apply_mask(image, mask):
    # CAN DEFINITELY BE IMPROVED!!
    column = [image.shape[1]//2 for x in range(0, image.shape[0])] # Middle
    for index, step in enumerate(column):
        # Traverse Left
        row = mask[index]
        count = step
        while count > 1:
            if row[count] == 255:
                image[index, 0:count] = np.zeros((count))
                break
            count -= 1

        # Traverse Right
        count = step
        while count < image.shape[1]-1:
            if row[count] == 255:
                image[index, count:] = np.zeros((image.shape[1]-count))
                break
            count += 1

        if index > image.shape[0]//2 and row[step] == 255:
            image[index:] = np.zeros((image.shape[0]-index, image.shape[1]))
            break
    return image
