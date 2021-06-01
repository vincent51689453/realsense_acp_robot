"""
@Author : Chan Tai Wing
@Date   : 01 Jun 2021
@About  : System parameters
"""
# Resolution
width = 1280
height = 720

# ROS Topic
node_name = 'realsense_regCNN'
camera_info_depth_aligned_color_topic = '/camera/aligned_depth_to_color/camera_info'
depth_image_topic = '/camera/aligned_depth_to_color/image_raw'
color_image_topic = '/camera/color/image_raw'
output_rgb_image_topic = '/camera/deep_learning/rgb'
output_depth_image_topic = '/camera/deep_learning/depth'

# Image and camera
depth_image = None
depth_array = None
color_image = None
camera_config = None
intrinsic = None

