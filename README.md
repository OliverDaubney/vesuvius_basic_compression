# Vesuvius Basic Compression - Script
This is a simple pipeline to reduce the memory requirements  
for Vesuvius scroll sections. It builds on the [great work](https://github.com/JamesDarby345/segment-anything-vesuvius/tree/main)   
by james darby to mask out the background material of the  
individual slices.  

For visualising data and testing ideas I have found  
that 8-bit data is very capable. The pipeline takes  
images and clips them between given pixel thresholds.  
I have used 18000 and 65535 to increase the contrast  
of the scroll fibres (see figure). Then saved the  
resultant images as 8-bit PNGs. This results in the  
whole of scroll 1 fitting in approximately 270 Gb of  
storage.

![Contrast improvement from clipping pixel values.](https://github.com/OliverDaubney/vesuvius_basic_compression/blob/main/images/Clipping_Contrast.png)

## How to Use This Script  
1. Place the main.py and support.py in the folder  
containing the original images (or masked - recommended).
2. Open the main file in your editor of choice and  
choose the file start number and end number. If you wish  
to delete the original files as you go, set REMOVE_ORIGINAL  
equal to True. NOTE - The program can be easily edited for  
access to different directories.
3. Run the python program from the terminal using:  
python main.py

## Dependencies
Python 3.x  
Python libraries (os, sys, cv2, numpy)  



