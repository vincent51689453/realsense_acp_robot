import cv2
import numpy as np

import handler_config as hc

def superpixel_refinement(rgb_img):

    # Find unqiue colors in an image
    colors = np.unique(rgb_img.reshape(-1, rgb_img.shape[-1]), axis=0, return_counts=True)
    # Colors
    color_list = colors[0]
    # Number of unique colors
    num_color = len(color_list)


    return rgb_img