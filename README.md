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

The pipeline for generating a mask is shown below and  
has been tested on scrolls 1, 0332 and 1667.

![Pipeline for mask generation.](https://github.com/OliverDaubney/vesuvius_basic_compression/blob/main/images/Pipeline.png)  


## How to Use The 'Main' Script  
1. Place the main.py and support.py in the folder  
containing the original images.
2. Open the main file in your editor of choice and  
choose the desired settings (see suggested_settings.txt  
for scrolls). If you wish to delete the original files  
as you go, set REMOVE_ORIGINAL equal to True.  
3. Run the python program from the terminal using:  
python main.py  


## How to Use The 'Pixel_Analysis' Script  
This is a relatively involved script for generating a  
histogram of pixel values for a given region in an image.
1. Open script and update the image source.
2. Update the bounds to set a region with an x_min, y_min,  
x_max, y_max format.
3. Run the python program for the terminal using:  
python pixel_analysis.py
4. Review the output region.png and histogram.png files.


## Dependencies
Python 3.x  
Python libraries (os, sys, cv2, numpy, matplotlib, collections) 


## Example Process
To clip and mask scroll 0332 we first need to characterise  
the pixel values. This can be achieved using the pixel_analysis  
script. This shows that the center bright core is mostly pixel  
values of >55000 and that the air is typically around 15000-20000.  
Thus potential clipping points are 18000 and 55000, to help  
increase the contrast of the papyrus sheets.  
![Scroll 0332 Pixel Analysis](https://github.com/OliverDaubney/vesuvius_basic_compression/blob/main/images/Scroll_0332_Analysis.png)  

Following this, a flood point is required that will be used to  
generate a mask. This is a point on the image that is always within  
the case. Once all the settings are prepared it is useful to run  
a test with each 1000th slice to check how the pipeline is performing.  
![Scroll 0332 Test Results](https://github.com/OliverDaubney/vesuvius_basic_compression/blob/main/images/Scroll_0332_Test.png)  

The results clearly show that throughout the scroll the pipeline  
seems to be masking the case successfully.  

