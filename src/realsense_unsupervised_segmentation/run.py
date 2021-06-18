#!/usr/bin/env python
"""
@Author : Chan Tai Wing
@Date   : 01 Jun 2021
@About  : Publish/Subscribe of realsense images
"""
#System Packages
import sys
import os
import cv2
import numpy as np
import pyrealsense2 as rs2
import time
import torch
from pynput import keyboard

#ROS Packages
import rospy
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge, CvBridgeError

#Customize packages
import handler_config as hc
import segmentation 


# System Relase based on keyboard input
def on_press (key):
    try:
        if((key.char=='q')or(key.char=='Q')):
            hc.system_release = True
   
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    #print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def depth_callback(ros_msg):
    # Depth image callback
    bridge = CvBridge()
    image = bridge.imgmsg_to_cv2(ros_msg)
    depth_array = np.array(image, dtype=np.float32)
    hc.depth_image = image
    hc.depth_array = depth_array
    #Display
    #cv2.imshow('depth_image',image)
    #cv2.waitKey(1)

def color_callback(ros_msg):
    # RGB image callback
    bridge = CvBridge()
    image = bridge.imgmsg_to_cv2(ros_msg)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    hc.color_image = image
    # Display
    # cv2.imshow('rgb_image',hc.color_image)
    # cv2.waitKey(1)    

def camera_info_callback(cameraInfo):
    hc.intrinsic = rs2.intrinsics()
    # Number of rows and columns in an image
    hc.intrinsic.width = cameraInfo.width
    hc.intrinsic.height = cameraInfo.height

    # Pixels coordinates of the principal point (center of projection)
    hc.intrinsic.ppx = cameraInfo.K[2]
    hc.intrinsic.ppy = cameraInfo.K[5]

    # Focal Length of image (multiple of pixel width and height)
    hc.intrinsic.fx = cameraInfo.K[0]
    hc.intrinsic.fy = cameraInfo.K[4]

    hc.model = rs2.distortion.none
    hc.coeffs = [i for i in cameraInfo.D]


def main():
    global training

    # Image Publisher for color and depth images
    image_pub_color = rospy.Publisher(hc.output_rgb_image_topic,Image,queue_size=10)
    image_pub_depth = rospy.Publisher(hc.output_depth_image_topic ,Image,queue_size=10)
    bridge = CvBridge()

    # Subscribe color and depth image
    rospy.Subscriber(hc.depth_image_topic,Image,callback=depth_callback)
    rospy.Subscriber(hc.color_image_topic,Image,callback=color_callback)

    # Subscribe camera info [depth_rgb aligned]
    rospy.Subscriber(hc.camera_info_depth_aligned_color_topic,CameraInfo,callback=camera_info_callback)

    # Keyboard Listener
    listener = keyboard.Listener(on_press=on_press,on_release=on_release)
    listener.start()
    print("Press <Q> or <q> to end the AI")
    
    # 2D/3D Image processing
    while not(hc.system_release):
        if((hc.depth_image is not None)and(hc.color_image is not None)):
            # Network training
            color_output = segmentation.inferencing(hc.color_image)
            
            # Unsupervised Segmentation (RGB):
            # color_output = segmentation.core(hc.color_image,hc.depth_image)
           
            # Visulaiztion in RVIZ
            image_pub_color.publish(bridge.cv2_to_imgmsg(color_output, "bgr8"))
            #image_pub_depth.publish(bridge.cv2_to_imgmsg(depth_output, "bgr8"))
            # Visualization in new window
            # cv2.imshow("Realsense [RGB]",color_output)
            # cv2.imshow("Realsense [Depth]",depth_output)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
   
    # Release GPU memory
    torch.cuda.empty_cache()
    print("GPU Memroy is released")


if __name__ == '__main__':
    rospy.init_node(hc.node_name)
    main()
