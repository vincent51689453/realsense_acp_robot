"""
@Author : Chan Tai Wing
@Date   : 12 May 2021
@About  : Subscribe tf transform
"""
# System packages
import math

# ROS package
import rospy
import tf

#Customize packages
import handler_config as hc

def euler_from_quaternion(rot):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """

    x, y, z, w = rot
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)
        
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)
        
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return roll_x, pitch_y, yaw_z 

# Finding camera link in the world
def get_tf_transform(source_link,target_link):
    trans = [0,0,0]
    rot = [0,0,0]
    r,p,y = 0,0,0

    hc.tf_listener.waitForTransform(source_link,target_link,rospy.Time(),rospy.Duration(5.0))
    
    now = rospy.Time.now()
    hc.tf_listener.waitForTransform(source_link,target_link,now,rospy.Duration(5.0))
    (trans,rot) = hc.tf_listener.lookupTransform(source_link,target_link,now)
    #trans[0]->X, trans[1]->Y, trans[2]->Z
    #rot[0]->X,rot[1]->Y,rot[2]->Z,rot[3]->W

    r,p,y = euler_from_quaternion(rot)

    rot_radian = []
    rot_radian.append(r)
    rot_radian.append(p)
    rot_radian.append(y)

    return trans,rot_radian
