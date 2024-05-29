"""
    Vesuvius Basic Compression - Script
    -----------------------------------
    This is a simple script to clip the pixel
    values and set air as approximately zero thus
    increasing the overall contrast for the
    scroll. There is also a rapid masking strategy  
    to remove the casing from the scroll slices.  
    The data type is also altered to 8 bit for  
    lower memory allocation.
    The output images are PNG files.

    How To Use
    ----------
    1. Select the method type in settings.
    2. Update the load directory and save directory  
    in the settings to match your folder layout.
    3. Alter the files expression to create a list  
    of your files.
    4. Update the clip_min and clip_max based on  
    the results of your analysis (e.g pixel_analysis).
    5. For other settings see suggested_settings.txt
    6. Run this main file from the terminal using:  
    python main.py

    Dependencies
    ------------
    Libraries: os, sys, cv2 and numpy.
    Local: support.py (included in repo).
"""

import os
import sys
import support as sf


"""
Settings
--------
Method - has three current types basic_clipped,
basic_masked and clipped_mask.
basic_clipped - just clips the provided images.
basic_masked - just masks the provided images.
clipped_mask - performs a clip and then masks the
images.
Any clipped images are 8-bit outputs, all image
outputs are as PNG files.
"""
METHOD = 'basic_clipped'
# File Handling Settings
LOAD_DIR = os.path.join(os.getcwd(), 'scroll_raw') # Where you want to load files from.
SAVE_DIR = os.path.join(os.getcwd(), 'scroll_small') # Where you want to save files to.
FILES = [f'{i:05}.tif' for i in range(0, 11000, 1000)]
REMOVE_ORIGINAL = False # Delete original files while progressing.
# Image Clipping Settings
CLIP_MIN = 18000
CLIP_MAX = 55000 # This should never exceed 65535.
# Masking Settings
MASK_FRAME = [0, 0, 0, 0] # [top, bottom, left, right]
MIN_CHECK = True
FLOOD_POINT = [1670, 1720] # [y, x] - This should be a point that is within the case for all images.


def main():
    for file in FILES:
        load_path = os.path.join(LOAD_DIR, file)
        if sf.check_path(load_path):
            initial_image = sf.load_image(path=load_path)
            processed_image = process_image(image=initial_image, method=METHOD)
            save_path = os.path.join(SAVE_DIR, f'{file[:-4]}.png')
            sf.save_image(image=processed_image, path=save_path)
            if REMOVE_ORIGINAL:
                os.remove(load_path)

def process_image(image, method='basic_clipped'):
    output = sf.set_to_int8(sf.clip(image, CLIP_MIN, CLIP_MAX))
    if method == 'basic_clipped' or method == 'basic':
        return output
    elif method == 'basic_masked' or method == 'clipped_masked':
        output_copy =  output.copy()
        mask = sf.create_mask(output_copy, MASK_FRAME, FLOOD_POINT, MIN_CHECK)
        if method == 'basic_masked':
            return sf.apply_mask(image, mask)
        elif method == 'clipped_masked':
            return sf.apply_mask(output, mask)
    else:
        print('Error - Unknown method type.')
        sys.exit()


if __name__ == '__main__':
    main()
    sys.exit()
