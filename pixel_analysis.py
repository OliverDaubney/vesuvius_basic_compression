"""
    A script to generate histograms of pixel values
    for specified regions of an image (uint16).
"""

import os
import sys
import numpy as np
import support as sf
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# Load an image.
image_file = '02000.tif'
image = sf.load_image(path=image_file)

# Collect pixels in a specified region.
bounds = [3100, 400, 3250, 550] # [x_min, y_min, x_max, y_max]
region = image[bounds[1]:bounds[3], bounds[0]:bounds[2]]
pixels = np.ravel(region)

# Create image with rectangle for the specified region.
fig, ax = plt.subplots()
ax.imshow(((image/65535)*255).astype('uint8'))
rect = patches.Rectangle(
    (bounds[0], bounds[1]),
    bounds[2]-bounds[0],
    bounds[3]-bounds[1],
    linewidth = 2,
    edgecolor = 'r',
    facecolor = 'none'
)
ax.add_patch(rect)
plt.savefig("region.png")
plt.close()

# Create and save the histogram.
plt.hist(pixels, bins=100, range=[0, 65535])
plt.savefig("histogram.png")
plt.close()

# Close program.
sys.exit()
