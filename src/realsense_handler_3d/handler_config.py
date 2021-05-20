"""
@Author : Chan Tai Wing
@Date   : 12 May 2021
@About  : System parameters
"""
# Resolution
width = 1280
height = 720

# Test point_L (Left)
test_pt_L_y = int(height/2)
test_pt_L_x = int(width/2) - 270
test_pt_L_bgr = (255,0,255)
test_pt_L_size = 5
test_pt_L_text = "Test point [L]" 

# Test point_R (Right)
test_pt_R_y = int(height/2)
test_pt_R_x = int(width/2) + 270
test_pt_R_bgr = (51,255,51)
test_pt_R_size = 5
test_pt_R_text = "Test point [R]" 

# Test point_T (Top)
test_pt_T_y = int(height/2) - 270
test_pt_T_x = int(width/2) 
test_pt_T_bgr = (255,255,51)
test_pt_T_size = 5
test_pt_T_text = "Test point [T]" 

# Test point_B (Bottom)
test_pt_B_y = int(height/2) + 270
test_pt_B_x = int(width/2) 
test_pt_B_bgr = (51,51,255)
test_pt_B_size = 5
test_pt_B_text = "Test point [B]" 

# Center of the frame
center_x = int(width/2)
center_y = int(height/2)
center_bgr = (153,255,255)
center_size = 5
center_text = "Center"

# ROS Topic
node_name = 'realsense_handler_3d'
camera_info_depth_aligned_color_topic = '/camera/aligned_depth_to_color/camera_info'
depth_image_topic = '/camera/aligned_depth_to_color/image_raw'
color_image_topic = '/camera/color/image_raw'
marker_topic = '/realsense_marker'
output_rgb_image_topic = '/system_rgb_output'
output_depth_image_topic = '/system_depth_output'

# ROS Marker parameters
marker_frame = 'world'
marker_namespace = 'realsense_marker'
marker_vis = None


# Image and camera
depth_image = None
depth_array = None
color_image = None
camera_config = None
intrinsic = None

#TF
tf_listener = None
marker_transform_ok = False
