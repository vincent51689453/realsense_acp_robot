"""
@Author : Chan Tai Wing
@Date   : 01 Jun 2021
@About  : System parameters
"""
# Resolution
width = 1280
height = 720

# ROS Topic
node_name = 'realsense_acupuncture'
camera_info_depth_aligned_color_topic = '/camera/aligned_depth_to_color/camera_info'
depth_image_topic = '/camera/aligned_depth_to_color/image_raw'
color_image_topic = '/camera/color/image_raw'
output_rgb_image_topic = '/camera/deep_learning/rgb'
output_depth_image_topic = '/camera/deep_learning/depth'
output_acp_image_topic = '/camera/acp/rgb'

# Image and camera
depth_image = None
depth_array = None
color_image = None
camera_config = None
intrinsic = None

# Detector
anchor_x = 1000
anchor_y = 600
anchor_color = (255,255,255)
anchor_size = 3
index = 0

