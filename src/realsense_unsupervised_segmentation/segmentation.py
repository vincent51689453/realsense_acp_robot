# System Packages
import torch
import torch.nn as nn
import torch.nn.init
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets,transforms
from torch.autograd import Varible

import cv2
import sys
import numpy as numpy

from skimage import segmentation

# Customize Packages
import handler_config as hc

capture_image = False

# Get a static image and saved
def freeze_image(rgb_image):
    # When capture button is pressed
    file_name = None
    if hc.capture_image:
        file_name = 'sample/' + str(hc.capture_index) + '.jpg'
        cv2.imwrite(file_name,rgb_image)
        hc.capture_index += 1
        hc.capture_image = False
    return True,file_name


# Pick a picture and start training
def single_image_training(rgb_image):
    image_ready = False
    # Make sure image is captured
    while not(image_ready):
        image_ready,file_name = freeze_image(rgb_image)

    # Start training
    


    
    return rgb_image


def core (rgb_image):
    return rgb_image
