"""
    Vesuvius Basic Compression - Script
    -----------------------------------
    This is a simple script to clip the pixel
    values and set air as approximately zero thus
    increasing the overall contrast for the
    scroll. The data type is also altered to 8
    bit for lower memory allocation.
    The output images are PNG files.

    Dependencies
    ------------
    Libraries: os, sys, cv2 and numpy.
    Local: support.py (included in repo).
"""

import os
import sys
import support as sf


# Settings
REMOVE_ORIGINAL = False
FILE_START_NUM = 0
FILE_END_NUM = 4
METHOD = 'basic'
CWD = os.getcwd()

CLIP_MIN = 18000
CLIP_MAX = 65535

def main():
    for i in range(FILE_START_NUM, FILE_END_NUM+1):
        load_path = os.path.join(CWD, f'{i:05}.tif')
        if sf.check_path(load_path):
            initial_image = sf.load_image(path=load_path)
            processed_image = process_image(image=initial_image, method=METHOD)
            save_path = os.path.join(CWD, f'{i:05}.png')
            sf.save_image(image=processed_image, path=save_path)
            if REMOVE_ORIGINAL:
                os.remove(load_path)

def process_image(image, method='basic'):
    output = sf.set_to_int8(sf.clip(image, CLIP_MIN, CLIP_MAX))
    if method == 'masked': 
        # This is not currently operational - work in progress.
        output_copy =  output.copy()
        mask = sf.create_mask(output_copy)
        output = sf.apply_mask(output, mask)
    return output

if __name__ == '__main__':
    main()
    sys.exit()
