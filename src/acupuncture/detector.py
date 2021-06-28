import cv2
import numpy as np
import colorsys

import handler_config as hc

def hsv_masking(rgb_image,target):
    # It will help to apply color masking

    #
    return masked_img

def superpixel_refinement(rgb_img):

    # Find unqiue colors in an image
    colors = np.unique(rgb_img.reshape(-1, rgb_img.shape[-1]), axis=0, return_counts=True)
    # Colors
    color_list = colors[0]
    # Number of unique colors
    num_color = len(color_list)

    """
    Saving some raw input
    if (hc.index <= 10):
        file_name = '/home/vincent/vincent-dev/realsense_acp_robot/src/acupuncture/data/raw_input_'+str(hc.index)+'.jpg'
        print("Saving to ...")
        print(file_name)
        cv2.imwrite(file_name,rgb_img)
        hc.index += 1
    """

    return rgb_img

    