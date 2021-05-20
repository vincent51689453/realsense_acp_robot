"""
@Author : Chan Tai Wing
@Date   : 18 May 2021
@About  : Global variables
"""
# ROS
node_name = 'realsense_deep_learning'

# ROS Topic (official)
node_name = 'realsense_deep_learning'
camera_info_depth_aligned_color_topic = '/camera/aligned_depth_to_color/camera_info'
depth_image_topic = '/camera/aligned_depth_to_color/image_raw'
color_image_topic = '/camera/color/image_raw'

# ROS Topic (unofficial)
deeplearning_topic = '/camera/color/deep_learning'

# Image Segmentation
rgb_image = None
bridge = None
network_setup = False
network = None
system_release = False




