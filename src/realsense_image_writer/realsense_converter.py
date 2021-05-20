#!/usr/bin/env python
"""
@Author : Chan Tai Wing
@Date   : 12 May 2021
@About  : Subscribe images from realsense and save as file for AI (python3)
"""
import rospy, cv2, cv_bridge
#from cv_bridge.boost.cv_bridge_boost import getCvType
from sensor_msgs.msg import Image
import math
import information as info
import alogrithm

"""
This scrip is only for subsribing raw image and publish image after processing.
All the core image processing will be inside algorithm.py
"""


# Subscriber -> Process -> Publish
class Converter:

  def __init__(self):
    # Bridge between OPENCV and ROS
    self.bridge = cv_bridge.CvBridge()
    # Subscriber
    #use $rostopic list to find out the correct topic about images
    self.image_sub = rospy.Subscriber(info.realsense_image_raw_topic,Image, self.image_callback)

  def image_callback(self, msg):
    # Convert ros message to opencv format
    image = self.bridge.imgmsg_to_cv2(msg)
    
    #Convert color space
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Show image in new window
    # cv2.imshow(info.raw_rgb_window, image)
    # cv2.waitKey(1)

    # External processing
    cv_image = alogrithm.core(image)


rospy.init_node('realsense_converter')
Converter = Converter()
rospy.spin()