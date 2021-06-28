from __future__ import division
import cv2
import numpy as np
import colorsys
import handler_config as hc

# Color masking
def color_masking(img,threshold):
    upper_limit = np.array([threshold[0] + 10, threshold[1] + 10, threshold[2] + 40])
    lower_limit = np.array([threshold[0] - 10, threshold[1] - 10, threshold[2] - 40])
    image_mask = cv2.inRange(img,lower_limit,upper_limit)
    return image_mask

# Find unqiue colors in an image
def get_color_info(img):
    colors = np.unique(img.reshape(-1, img.shape[-1]), axis=0, return_counts=True)
    # Colors
    color_list = colors[0]
    # Number of unique colors
    num_color = len(color_list)    
    return color_list,num_color

def get_max_contour(mask):
    _,contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Largest contour
    if(len(contours)!=0):
        max_contour = max(contours, key = cv2.contourArea)
  
    return max_contour

def superpixel_refinement(rgb_img):
    object_list = []

    # Get unique colors of an image
    color_list, num_color = get_color_info(rgb_img)
    print("Color bank [BGR]:")
    for i in range(0,num_color):
        print("color #{}: {}".format(i,[color_list[i]]))
    print("\r\n")

    # Consider color in color bank one by one, find max contour
    for j in range(0,num_color):
        mask = color_masking(rgb_img,color_list[j])
        max_contour = get_max_contour(mask)
        object_list.append(max_contour)

    # Find forearm in different 'max' contours
    for k in range(0,len(object_list)):
        if(object_list[k] is not None):
            x,y,w,h = cv2.boundingRect(object_list[k])
            area = w*h
            # Draw detector boundary boxe
            if((area>=hc.forearm_area_min)and(area<=hc.forearm_area_max)):
                cv2.drawContours(rgb_img, object_list[k], -1, (0,255,0),3)
                cv2.rectangle(rgb_img,(x,y),(x+w,y+h),(0,0,255),3)
                hc.target_x,hc.target_y,hc.target_h,hc.target_w = x,y,h,w
                hc.target_found = True
    
    # Acupuncuture Map Generation
    rgb_img = rgb_img[hc.target_y:hc.target_y+hc.target_h, hc.target_x:hc.target_x+hc.target_w]

    return rgb_img

    