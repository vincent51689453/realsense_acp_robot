#!/usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import String
from math import pi

def ur3_config():
  global robot,group,scene,display_trajectory_publisher
  ## First initialize moveit_commander and rospy.
  print "============ Starting tutorial setup ============"
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
  print "[INFO] Reference frame: %s" % group.get_planning_frame()

  ## We can also print the name of the end-effector link for this group
  print "[INFO] Reference frame: %s" % group.get_end_effector_link()

  ## We can get a list of all the groups in the robot
  print "[INFO] Robot Groups:"
  print robot.get_group_names()

  ## Sometimes for debugging it is useful to print the entire state of the
  ## robot.
  print "[INFO]Printing robot state"
  print robot.get_current_state()
  print "========================================"
  print "[UR3] Configuration Done"

def ur3_set_joint_pose(j1,j2,j3,j4,j5,j6):

  global robot,group,scene,display_trajectory_publisher
  #Clear any pose in previous
  group.clear_pose_targets()
  ## Then, we will get the current set of joint values for the group
  group_variable_values = group.get_current_joint_values()
  #print "============ Joint values: ", group_variable_values
  ## Modify each joints postion below

  #Base joint
  group_variable_values[0] = j1
  group_variable_values[1] = j2
  group_variable_values[2] = j3
  group_variable_values[3] = j4
  group_variable_values[4] = j5
  #Last joint for end effector
  group_variable_values[5] = j6


  group.set_joint_value_target(group_variable_values)

  plan2 = group.plan()
  #If you want to control the true robot,or move the simulated robot
  #Instead of only showing trajectory
  group.go(wait=True)
  group.stop()
  group.clear_pose_targets()
  current_pose = group.get_current_pose().pose
  print current_pose
  print "[INFO] Pose is executed"



if __name__=='__main__':
  try:
    ur3_config()
    ur3_set_joint_pose(0,0,0,0,0,pi/2)
  except rospy.ROSInterruptException:
    pass