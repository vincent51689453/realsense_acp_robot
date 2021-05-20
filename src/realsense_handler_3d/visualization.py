"""
@Author : Chan Tai Wing
@Date   : 12 May 2021
@About  : Image drawing and visualization
"""
#System Packages
import cv2
import handler_config as hc

#ROS packages
import rospy
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker

# Drawing test_pt marker on an image
def draw_test_pt_marker(image,x,y,message,bgr,marker_size):
    cv2.putText(image, message,((x-20),(y-20)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,bgr,1,cv2.LINE_AA)
    cv2.circle(image,(x,y),marker_size,bgr,-1)
    return image

# Drawing test_pt marker z distance on an image
def draw_test_pt_marker_z_distance(image,z,x,y,bgr):
    z = str(round(z,3)) + 'cm'
    cv2.putText(image, z,((x-20),(y-40)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,bgr,1,cv2.LINE_AA)

    return image

#A testing function to publish a arrow in rvizq
def marker_publisher_demo():
    marker_vis = rospy.Publisher(hc.marker_topic,Marker,queue_size=10)
    marker = Marker()
    marker.header.frame_id = 'world'
    marker.header.stamp = rospy.Time.now()
    marker.ns = 'realsense_marker'
    marker.action = Marker.ADD
    marker.id = 0
    marker.type = Marker.ARROW
    start = Point(0.5,0.5,0.5)
    end = Point(1,1,1)
    marker.points.append(start)
    marker.points.append(end)
    #marker.text = 'test'
    marker.scale.x = 0.1;
    marker.scale.z = 0.1;
    marker.scale.y = 0.1;
    marker.color.a = 1.0;
    marker.color.r = 0.0;
    marker.color.g = 1.0;
    marker.color.b = 0.0;
    marker_vis.publish(marker)


# Create marker in rviz
def create_marker(x1,y1,z1,x2,y2,z2,r,g,b,id):
    marker = Marker()
    marker.header.frame_id = 'world'
    marker.header.stamp = rospy.Time.now()
    marker.ns = 'realsense_marker'
    marker.action = Marker.ADD
    marker.id = id
    marker.type = Marker.ARROW
    start = Point(x1,y1,z1)
    end = Point(x2,y2,z2)
    marker.points.append(start)
    marker.points.append(end)
    marker.scale.x = 0.003;
    marker.scale.z = 0.003;
    marker.scale.y = 0.003;
    marker.color.a = 1.0;
    marker.color.r = r;
    marker.color.g = g;
    marker.color.b = b;
    return marker