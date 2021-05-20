#!/usr/bin/env python
"""
@Author : Chan Tai Wing
@Date   : 18 May 2021
@About  : Realtime Image Segmentation
"""
# System Packages
import cv2
import torch
import torchvision
from torchvision import transforms as T
from pynput import keyboard

# ROS Packages
import rospy
import cv_bridge
from sensor_msgs.msg import Image

# Customized Packages
import information as info
import mask_rcnn

cv_image = None
cv_image_backup = None

# System Relase based on keyboard input
def on_press (key):
    global adjust,power
    try:
        if(key.char=='q'):
            info.system_release = True
        if(key.char=='Q'):
            info.system_release = True
   
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    #print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def color_callback(ros_msg):
    # RGB image callback
    image = info.bridge.imgmsg_to_cv2(ros_msg)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    info.rgb_image = image

def main():

    # Image Publisher
    image_pub = rospy.Publisher(info.deeplearning_topic,Image)

    # Bridge between ROS and OPENCV
    info.bridge = cv_bridge.CvBridge()

    # Image Subsriber
    image_sub = rospy.Subscriber(info.color_image_topic,Image,callback=color_callback)

    # Mask RCNN Model
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    model.eval()

    # Keyboard Listener
    listener = keyboard.Listener(on_press=on_press,on_release=on_release)
    listener.start()
    print("Press <Q> or <q> to end the AI")

    # Realtime Image Segmentation
    while not(info.system_release):
        if(info.rgb_image is not None):
            # Processing Core
            output_img = mask_rcnn.core(model,info.rgb_image, threshold=0.8, rect_th=6, text_th=2, text_size=1)
            # Visulaiztion in RVIZ
            image_pub.publish(info.bridge.cv2_to_imgmsg(output_img, "bgr8"))

    # Release GPU memory
    torch.cuda.empty_cache()
    print("GPU Memroy is released")

if __name__ == '__main__':
    rospy.init_node(info.node_name)
    main()
    

