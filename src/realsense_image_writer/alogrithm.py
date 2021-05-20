import cv2
import information as info

"""
Core of image saving
"""

# Image processing core
def core(image):
    
    print("Image #{} saving ...".format(info.image_index))
    info.image_index += 1
    cv2.imwrite(info.image_save_path,image)
    return image