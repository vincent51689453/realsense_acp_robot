#!/usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import String
from math import pi
import numpy as np
import csv

robot = None
group = None
scene = None
display_trajectory_publisher = None

log_file = "src/ur3_python_controller/current_pose.csv"

def euler_to_quaternion(Yaw, Pitch, Roll):
  yaw   = Yaw   * pi / 180 
  pitch = Roll  * pi / 180 
  roll  = Pitch * pi / 180 

  qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
  qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
  qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

  return [qx, qy, qz, qw]

def ur3_config():
  global robot,group,scene,display_trajectory_publisher
  ## First initialize moveit_commander and rospy.
  #print "============ Starting system"
  moveit_commander.roscpp_initialize(sys.argv)
  rospy.init_node('move_group_python_interface_tutorial',
                  anonymous=True)

  ## Instantiate a RobotCommander object.  This object is an interface to
  ## the robot as a whole.
  robot = moveit_commander.RobotCommander()

  ## Instantiate a PlanningSceneInterface object.  This object is an interface
  ## to the world surrounding the robot.
  scene = moveit_commander.PlanningSceneInterface()

  ## Instantiate a MoveGroupCommander object.  This object is an interface
  ## to one group of joints.  In this case the group is the joints in the ur3
  ## arm.  This interface can be used to plan and execute motions on the ur3
  ## arm.
  group = moveit_commander.MoveGroupCommander("ur3")

  ## We create this DisplayTrajectory publisher which is used below to publish
  ## trajectories for RVIZ to visualize.
  display_trajectory_publisher = rospy.Publisher(
                                      '/move_group/display_planned_path',
                                      moveit_msgs.msg.DisplayTrajectory)


  ## Getting Basic Information
  ## We can get the name of the reference frame for this robot
  #print "[INFO] Reference frame: %s" % group.get_planning_frame()

  ## We can also print the name of the end-effector link for this group
  #print "[INFO] Reference frame: %s" % group.get_end_effector_link()

  ## We can get a list of all the groups in the robot
  #print "[INFO] Robot Groups:"
  #print robot.get_group_names()

  ## Sometimes for debugging it is useful to print the entire state of the
  ## robot.
  #print "[INFO]Printing robot state"
  #print robot.get_current_state()
  #print "========================================"
  #print "[UR3] Configuration Done"

def ur3_set_end_effector_goal_quat(pos_x,pos_y,pos_z,qx,qy,qz,qw):
  global robot,group,scene,display_trajectory_publisher
  current_pose = group.get_current_pose().pose
  print "Original Pose Information"
  print current_pose
  # XYZ are in terms of meters
  x = 0
  y = 0
  z = 0
  #Yaw,pitch and roll should be in degree    
  # They are all relative to base link coorindates     
  roll = 10
  yaw = 183
  pitch = 180

  pose_goal = geometry_msgs.msg.Pose()
  #Q = euler_to_quaternion(yaw , pitch, roll)
  #print Q
  pose_goal.orientation.x = qx
  pose_goal.orientation.y = qy
  pose_goal.orientation.z = qz
  pose_goal.orientation.w = qw

  pose_goal.position.x = pos_x
  pose_goal.position.y = pos_y
  pose_goal.position.z = pos_z
  group.set_pose_target(pose_goal)

  plan = group.go(wait=True)
  group.stop()
  current_pose = group.get_current_pose().pose
  print "------------ Target Pose Information ------------"
  print current_pose
  group.clear_pose_targets()
  print "[INFO] Goal of end effector is arrived"

def save_to_csv_quat():
  global group
  current_pose = group.get_current_pose().pose
  pos_x = current_pose.position.x
  pos_y = current_pose.position.y
  pos_z = current_pose.position.z
  qx = current_pose.orientation.x
  qy = current_pose.orientation.y
  qz = current_pose.orientation.z
  qw = current_pose.orientation.w
  with open(log_file,'w') as pose_log:
    writer = csv.writer(pose_log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow([pos_x,pos_y,pos_z,qx,qy,qz,qw])


if __name__=='__main__':
  try:
    ur3_config()
    # Set initial position
    ur3_set_end_effector_goal_quat(-0.2784,0.078,0.3399,0.074,0.695,0.711,0.0717)
    
    #while True:
    #  Sending current pose
    #  save_to_csv_quat()

  except rospy.ROSInterruptException:
    pass