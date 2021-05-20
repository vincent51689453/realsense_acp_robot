"""
@Author : Chan Tai Wing
@Date   : 12 May 2021
@About  : Alogrithms and image processing
"""
# System Packages
# Force float division in python3
from __future__ import division
import cv2
import pyrealsense2 as rs

# ROS Package
import rospy

# Customize packages
import handler_config as hc
import visualization as vs
import tf_subscribe as tf_sub


# RVIZ Coordinates
# Red   - X
# Grren - Y
# Blue  - Z

markers_z = [0,0,0,0,0]
markerL_world = [0,0,0]
markerR_world = [0,0,0]
markerT_world = [0,0,0]
markerB_world = [0,0,0]
center_world = [0,0,0]

markerL_world_x,markerL_world_y,markerL_world_z = 0,0,0
markerR_world_x,markerR_world_y,markerR_world_z = 0,0,0
markerT_world_x,markerT_world_y,markerT_world_z = 0,0,0
markerB_world_x,markerB_world_y,markerB_world_z = 0,0,0
center_world_x,center_world_y,center_world_z = 0,0,0

# Find Z distances for markers (default depth unit is mm)
def all_marker_z_distance(depth_image):
    output = []
    a = depth_image[hc.test_pt_L_y,hc.test_pt_L_x]/10
    output.append(a)
    b = depth_image[hc.test_pt_R_y,hc.test_pt_R_x]/10
    output.append(b)
    c = depth_image[hc.test_pt_T_y,hc.test_pt_T_x]/10
    output.append(c)
    d = depth_image[hc.test_pt_B_y,hc.test_pt_B_x]/10
    output.append(d)
    e = depth_image[hc.center_y,hc.center_x]/10
    output.append(e)
    return output

# Draw all markers on rgb image and depth image
def draw_all_markers_image(rgb_image,depth_image,z_distances):
    # RGB Image - Marker
    rgb_image = vs.draw_test_pt_marker(rgb_image,hc.test_pt_L_x,hc.test_pt_L_y,hc.test_pt_L_text,hc.test_pt_L_bgr,hc.test_pt_L_size)
    rgb_image = vs.draw_test_pt_marker(rgb_image,hc.test_pt_R_x,hc.test_pt_R_y,hc.test_pt_R_text,hc.test_pt_R_bgr,hc.test_pt_R_size)
    rgb_image = vs.draw_test_pt_marker(rgb_image,hc.test_pt_T_x,hc.test_pt_T_y,hc.test_pt_T_text,hc.test_pt_T_bgr,hc.test_pt_T_size)
    rgb_image = vs.draw_test_pt_marker(rgb_image,hc.test_pt_B_x,hc.test_pt_B_y,hc.test_pt_B_text,hc.test_pt_B_bgr,hc.test_pt_B_size)
    rgb_iamge = vs.draw_test_pt_marker(rgb_image,hc.center_x,hc.center_y,hc.center_text,hc.center_bgr,hc.center_size)

    # RGB Image - Z distances
    rgb_image = vs.draw_test_pt_marker_z_distance(rgb_image,z_distances[0],hc.test_pt_L_x,hc.test_pt_L_y,hc.test_pt_L_bgr)
    rgb_image = vs.draw_test_pt_marker_z_distance(rgb_image,z_distances[1],hc.test_pt_R_x,hc.test_pt_R_y,hc.test_pt_R_bgr)
    rgb_image = vs.draw_test_pt_marker_z_distance(rgb_image,z_distances[2],hc.test_pt_T_x,hc.test_pt_T_y,hc.test_pt_T_bgr)
    rgb_image = vs.draw_test_pt_marker_z_distance(rgb_image,z_distances[3],hc.test_pt_B_x,hc.test_pt_B_y,hc.test_pt_B_bgr)
    rgb_image = vs.draw_test_pt_marker_z_distance(rgb_image,z_distances[4],hc.center_x,hc.center_y,hc.center_bgr)

    # Depth Image - Markers
    depth_image = vs.draw_test_pt_marker(depth_image,hc.test_pt_L_x,hc.test_pt_L_y,hc.test_pt_L_text,(0,0,0),hc.test_pt_L_size)
    depth_image = vs.draw_test_pt_marker(depth_image,hc.test_pt_R_x,hc.test_pt_R_y,hc.test_pt_R_text,(0,0,0),hc.test_pt_R_size)
    depth_image = vs.draw_test_pt_marker(depth_image,hc.test_pt_T_x,hc.test_pt_T_y,hc.test_pt_T_text,(0,0,0),hc.test_pt_T_size)
    depth_image = vs.draw_test_pt_marker(depth_image,hc.test_pt_B_x,hc.test_pt_B_y,hc.test_pt_B_text,(0,0,0),hc.test_pt_B_size)
    depth_image = vs.draw_test_pt_marker(depth_image,hc.center_x,hc.center_y,hc.center_text,(0,0,0),hc.center_size)

    # Depth Image - Z distances
    depth_imagee = vs.draw_test_pt_marker_z_distance(depth_image,z_distances[0],hc.test_pt_L_x,hc.test_pt_L_y,(0,0,0))
    depth_image = vs.draw_test_pt_marker_z_distance(depth_image,z_distances[1],hc.test_pt_R_x,hc.test_pt_R_y,(0,0,0))
    depth_image = vs.draw_test_pt_marker_z_distance(depth_image,z_distances[2],hc.test_pt_T_x,hc.test_pt_T_y,(0,0,0))
    depth_image = vs.draw_test_pt_marker_z_distance(depth_image,z_distances[3],hc.test_pt_B_x,hc.test_pt_B_y,(0,0,0))
    depth_image = vs.draw_test_pt_marker_z_distance(depth_image,z_distances[4],hc.center_x,hc.center_y,(0,0,0))

    return rgb_image, depth_image


# Algorithm Core
def core(rgb_image,depth_image,intrinsic):

    global markers_z
    global markerL_world,markerB_world,markerR_world,markerT_world,center_world

    global markerL_world_x,markerL_world_y,markerL_world_z
    global markerR_world_x,markerR_world_y,markerR_world_z
    global markerT_world_x,markerT_world_y,markerT_world_z
    global markerB_world_x,markerB_world_y,markerB_world_z
    global center_world_x,center_world_y,center_world_z

    # TF Calculate from world to camera_link (realsense)
    realsense_trans,realsense_rot = tf_sub.get_tf_transform('world','camera_link')

    
    # Image to world transformation for all markers
    if(not(hc.marker_transform_ok)):
        # Find all Z distances for all markers (in cm)
        # Order: L / R / T / B / Center
        markers_z = all_marker_z_distance(depth_image)

        # Test Point L
        markerL_world = rs.rs2_deproject_pixel_to_point(intrinsic,[hc.test_pt_L_x,hc.test_pt_L_y],markers_z[0])
        # Test Point R
        markerR_world = rs.rs2_deproject_pixel_to_point(intrinsic,[hc.test_pt_R_x,hc.test_pt_R_y],markers_z[1])
        # Test Point T
        markerT_world = rs.rs2_deproject_pixel_to_point(intrinsic,[hc.test_pt_T_x,hc.test_pt_T_y],markers_z[2])
        # Test Point B
        markerB_world = rs.rs2_deproject_pixel_to_point(intrinsic,[hc.test_pt_B_x,hc.test_pt_B_y],markers_z[3])
        # Test Point Center
        center_world = rs.rs2_deproject_pixel_to_point(intrinsic,[hc.center_x,hc.center_y],markers_z[4])
        

    # Test Point L
    if(markers_z[0]!=0):
        if(not(hc.marker_transform_ok)):
            markerL_world_x = markerL_world[1]/100 + realsense_trans[0]
            markerL_world_y = markerL_world[0]/100 + realsense_trans[1]
            markerL_world_z = markerL_world[2]/100*-1 + realsense_trans[2]
        # Publish center marker
        # z2 set to 0 because the arrow needs to point to the ground
        markerL_rviz = vs.create_marker(realsense_trans[0],realsense_trans[1],realsense_trans[2],
                                        markerL_world_x,markerL_world_y,markerL_world_z,1.0,0.0,1.0,id=0)
        hc.marker_vis.publish(markerL_rviz)
        
    # Test Point R
    if(markers_z[1]!=0):
        if(not(hc.marker_transform_ok)):
            markerR_world_x = markerR_world[1]/100 + realsense_trans[0]
            markerR_world_y = markerR_world[0]/100 + realsense_trans[1]
            markerR_world_z = markerR_world[2]/100*-1 + realsense_trans[2]
        # Publish center marker
        # z2 set to 0 because the arrow needs to point to the ground
        markerR_rviz = vs.create_marker(realsense_trans[0],realsense_trans[1],realsense_trans[2],
                                        markerR_world_x,markerR_world_y,markerR_world_z,0.2,1.0,0.2,id=1)
        hc.marker_vis.publish(markerR_rviz)

    # Test Point T
    if(markers_z[2]!=0):
        if(not(hc.marker_transform_ok)):
            markerT_world_x = markerT_world[1]/100 + realsense_trans[0]
            markerT_world_y = markerT_world[0]/100 + realsense_trans[1]
            markerT_world_z = markerT_world[2]/100*-1 + realsense_trans[2] 
        # Publish center marker
        # z2 set to 0 because the arrow needs to point to the ground
        markerT_rviz = vs.create_marker(realsense_trans[0],realsense_trans[1],realsense_trans[2],
                                        markerT_world_x,markerT_world_y,markerT_world_z,0.2,1.0,1.0,id=2)
        hc.marker_vis.publish(markerT_rviz)    

    # Test Point B
    if(markers_z[3]!=0):
        if(not(hc.marker_transform_ok)):
            markerB_world_x = markerB_world[1]/100 + realsense_trans[0]
            markerB_world_y = markerB_world[0]/100 + realsense_trans[1]
            markerB_world_z = markerB_world[2]/100*-1 + realsense_trans[2] 
        # Publish center marker
        # z2 set to 0 because the arrow needs to point to the ground
        markerB_rviz = vs.create_marker(realsense_trans[0],realsense_trans[1],realsense_trans[2],
                                        markerB_world_x,markerB_world_y,markerB_world_z,1.0,0.2,0.2,id=3)
        hc.marker_vis.publish(markerB_rviz)    

    # Test Point C
    if(markers_z[4]!=0):
        if(not(hc.marker_transform_ok)):
            center_world_x = center_world[1]/100 + realsense_trans[0]
            center_world_y = center_world[0]/100 + realsense_trans[1]
            center_world_z = center_world[2]/100*-1 + realsense_trans[2] 
        # Publish center marker
        # z2 set to 0 because the arrow needs to point to the ground
        center_rviz = vs.create_marker(realsense_trans[0],realsense_trans[1],realsense_trans[2],
                                        center_world_x,center_world_y,center_world_z,1.0,1.0,0.6,id=4)
        hc.marker_vis.publish(center_rviz) 

    
    # Draw markers on rgb and depth images (only valid before marker_transform_ok)
    draw_all_markers_image(rgb_image,depth_image,markers_z)

    # Marker should only transform once.
    # As it is physically exist in the world, it should not change anymore
    hc.marker_transform_ok = True   



    #Apply color map to depth image
    depth_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.065), cv2.COLORMAP_JET)


    return rgb_image,depth_image



