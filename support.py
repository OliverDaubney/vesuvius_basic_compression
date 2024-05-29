"""
Support file for the Vesuvius Basic Compression script.
Most of these are wrappers for cv2 functions alongside  
some experimental mask generation functions.

Dependencies
------------
Libraries: os, cv2, numpy and collections.
"""

import os
import cv2
import numpy as np
from collections import deque


# Functions to support file handling.
def check_path(path):
    if not os.path.isfile(path):
        print(f'Error - Source file ({path}) could not be found.')
        return False
    return True

def load_image(path, grayscale=True):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if image.shape[-1] == 3 and grayscale:
        return np.average(image, axis=2)
    return image

def save_image(image, path):
    cv2.imwrite(path, image)


# Functions to support data structure handling.
def find_value_in_2D(array, value, start=0):
    for i in range(start, array.shape[0]):
        for j in range(0, array.shape[1]):
            if array[i, j] == value:
                return [i, j]


# Basic image processing
def clip(image, clip_min, clip_max, skip=False):
    if not skip:
        image[image<clip_min] = clip_min
        image[image>clip_max] = clip_max
    return (image-clip_min)/(clip_max-clip_min)

def set_to_int8(image):
    return (image*255).astype('uint8')

def blur_image(image, kernel):
    return cv2.filter2D(src=image, ddepth=-1, kernel=kernel)


# Functions to support breadth-first search.
def bfs(position, grid):
    """
        A Breadth First Search implementation.
        Expects a position as [y, x] and a grid to
        traverse. The grid should be a 2D numpy array
        with values of 1 for any traversable position.
        Returns a list of traversed points and an
        updated grid (0 is used for traversed points).
    """
    queue, closed = deque([position]), []
    while queue:
        current = queue.popleft()
        closed.append(current)
        grid[current[0], current[1]] = 0
        queue = fetch_neighbours(current, queue, grid)
    return closed, grid

def fetch_neighbours(point, queue, grid):
    if point[0] > 0 and grid[point[0]-1, point[1]] == 1 and [point[0]-1, point[1]] not in queue:
        queue.append([point[0]-1, point[1]])
    if point[0] < grid.shape[0]-1 and grid[point[0]+1, point[1]] == 1 and [point[0]+1, point[1]] not in queue:
        queue.append([point[0]+1, point[1]])
    if point[1] > 0 and grid[point[0], point[1]-1] == 1 and [point[0], point[1]-1] not in queue:
        queue.append([point[0], point[1]-1])
    if point[1] < grid.shape[1]-1 and grid[point[0], point[1]+1] == 1 and [point[0], point[1]+1] not in queue:
        queue.append([point[0], point[1]+1])
    return queue;


# Functions to support edge detection.
def sobel_edge_detector(image):
    grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0)
    grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1)
    grad = np.sqrt(grad_x**2 + grad_y**2)
    grad_norm = (grad * 255 / grad.max()).astype('uint8')
    return grad_norm

def clean_edges(image, min_check):
    position, grid = [0, 0], image.copy()
    grid[grid > 0] = 1
    while 1 in grid:
        position = find_value_in_2D(array=grid, value=1, start=position[0])
        cluster, grid = bfs(position, grid)
        if check_cluster(cluster, image.shape[0]-1, image.shape[1]-1):
            if min_check and len(cluster) > 1000:
                continue
            else:
                for point in cluster:
                    image[point[0], point[1]] = 0
    return image

def check_cluster(points, max_y, max_x):
    for point in points:
        if point[0] == 0 or point[0] == max_y or point[1] == 0 or point[1] == max_x:
            return False
    return True


# Mask creation and handling functions.
def density_blur(image, cycles, small_blur, large_blur, diff_multiplier):
    for i in range(0, cycles):
        # Initial blur to smooth pixel local pixel differences.
        blur_1 = blur_image(image, np.ones((small_blur, small_blur), np.float32)/(small_blur**2))
        # Second blur to get averages of larger local environments.
        blur_2 = blur_image(image, np.ones((large_blur, large_blur), np.float32)/(large_blur**2))
        diff = np.abs(blur_1.astype('int16') - blur_2.astype('int16'))
        diff = (image - diff_multiplier*diff)
        diff[diff < 0] = 0
        image = set_to_int8(clip(diff, diff.min(), diff.max(), True))
    return image

def cluster_segmentation(image, num_clusters, grayscale=True):
    X = image.reshape(-1, 1).repeat(3, axis=1).astype('float32')
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, (centers) = cv2.kmeans(X, num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = centers.astype('uint8')
    labels = labels.flatten()
    segmented = centers[labels.flatten()]
    segmented = segmented.reshape((image.shape[0], image.shape[1], 3))
    if grayscale:
        return segmented[:, :, 0]
    return segmented

def set_frame(image, frame):
    image[:frame[0]] = 200
    image[image.shape[0]-frame[1]:] = 200
    image[:, :frame[2]] = 200
    image[:, image.shape[1]-frame[3]:] = 200
    return image

def create_mask(image, frame, position, min_check):
    # Clip image to remove the background noise and increase sheet contrast.
    clipped = set_to_int8(clip(image, 30, image.max()))
    # Use density difference with blur to highlight the case.
    dense = density_blur(clipped, 1, 10, 40, 3)
    # Final blur to create more homogenous regions.
    blur = blur_image(dense, np.ones((80, 80), np.float32)/6400)
    blur = set_to_int8(clip(blur, blur.min(), blur.max(), True))
    # Resize for efficient pixel analysis.
    small = cv2.resize(blur, (blur.shape[1]//10, blur.shape[0]//10))
    # Segmentation by cluster analysis.
    mask = cluster_segmentation(small, 3)
    # Edge detection.
    mask[mask < mask.max()] = 0
    mask[mask > 0] = 255
    mask = sobel_edge_detector(mask)
    mask = clean_edges(mask, min_check)
    # Floodfill to create mask.
    mask[mask>0] = 200
    frame = [i//10 for i in frame]
    mask = set_frame(mask, frame)
    cv2.floodFill(mask, None, (position[0]//10, position[1]//10), 255)
    mask[mask < 255] = 0
    # Resize to original image shape.
    mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
    # Make mask binary.
    mask = mask // 255
    return mask

def apply_mask(image, mask):
    """
        A function to  mask out regions of an
        image using a binary mask for the image.
        This function returns an image array.
    """
    image = image * mask
    return image
