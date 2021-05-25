# System Packages
from __future__ import division
import cv2
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

    

def core (rgb_image,depth_image):
    #Apply color map to depth image
    depth_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.065), cv2.COLORMAP_JET)
    
    return rgb_image,depth_image
