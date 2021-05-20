# Acupuncture Robot with Intel D415 Camera

## Introduction
Acupuncture therapy is one of the cornerstones in traditional Chinese medicine. It requires rich experiences from Chinese medicine pratitioner. However, repeatability among different practitioners are low. Meanhwile, there is a large variety of skin conditions in terms of color, diseases, size, etc. In recent year, deep neural network for acupunctur epoint detection is proposed. However, it is difficult to localize multiple acupuncture points. In this repository is proposing a hihg repeatability robot with a new approach of acupuncture points positioning is proposed which can be adaptive to variety of skin conditionsa dn achieve multiple acupuncture points' localization.

## Eye-Hand Coordination
Five testing points are used to check the resultant transformation. They were captured and transformed **ONCE** at the very begining. The transformed coordinates pair were mounted and should not be changed anymore because they were some points which exist in the physical world. Those points should be independent from the camera translations and rotations after capturing. 

The visualization of resultant transformation was shown in the following pictures and videos. 

![image](https://github.com/vincent51689453/realsense_acp_robot/blob/melodic-ur3-devel/git_image/hand-eye-coordination/rviz01.png)

![image](https://github.com/vincent51689453/realsense_acp_robot/blob/melodic-ur3-devel/git_image/hand-eye-coordination/rviz02.png)

![image](https://github.com/vincent51689453/realsense_acp_robot/blob/melodic-ur3-devel/git_image/hand-eye-coordination/rviz03.png)

![image](https://github.com/vincent51689453/realsense_acp_robot/blob/melodic-ur3-devel/git_image/hand-eye-coordination/rviz_image_world_tf.gif)


## Acupuncture Localization
(TO-DO)

