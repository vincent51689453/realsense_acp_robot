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

## Mask RCNN Implementation (deprecated)
This realtime image segmentation using Mask RCNN was based on *python2 using Pytorch==1.4.0 and torchvision==0.5.0.*. Therefore,please follow the instructions below to setup the environment. **Make Sure your pip version is pointed to python2.7**


```
pip --version
pip install torch==1.4.0 torchvision==0.5.0
pip install future
sudo apt-get install python3-matplotlib
```

Please download the checkpoint trained with COCO dataset using the following path:

https://download.pytorch.org/models/maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth


Please put the checkpoint to the following path:

/home/vincent/.cache/torch/checkpoints/maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth

![image](https://github.com/vincent51689453/realsense_acp_robot/blob/melodic-ur3-devel/git_image/image_segmentation/mask_rcnn_01.png)

## Unsupervised image segmentation
This segmentaiton does not required to prepare a large amount of dataset. It can learn to cluster pixels in an image with unsupervised deep neural network. Thus, it is much more efficient than mask-rcnn. In order to use this approach, scikit-image is required and you can install using the following command. Noted that this system is using python2
```
pip install scikit-image
```

### Training
If you plan to train the newtork, you must enable line 111 to start the training. After you run realsnense_unsupervised_segmentation/main.py, you need to press \<X\> or \<x\> to capture a picture. That picture will be used to train the network to perform image segmentation.

Different parameters can be set to get the most optimal output.

1. num_neurons_basic = 100 (default) -> number of neurons in the hidden layers
2. num_layers_basic = 2 (default) -> number of hidden layers
3. square_kernel_size = 3 (default) -> kernel size
4. stride_step = 1 (default) -> stride 
5. padding_approach = 1 (default) -> padding approach
6. compactness = 100 (default) -> Balances color proximity and space proximity. Higher means consider space.Vice versa, lower meanus consider color
7. segments = 10000 (default) -> The approximate number of labels in the segmented output image.
8. max_epoch = 10000 (default) -> Maximum epohces
9. min_num_labels = 2 (default) -> Categories you need
10. learning_rate = 0.1 (default) -> Learning rate

![image](https://github.com/vincent51689453/realsense_acp_robot/blob/melodic-ur3-devel/git_image/image_segmentation/unsupervised_segmentation.png)

## Acupuncture Localization


## System StartUp Procedures
1) Connect to UR3    : ./start_robot_bringup.sh
2) Start Planning    : ./start_robot_planning.sh
3) Drive UR3 to the standby position: ./robot_standby_pose.sh
3) Start Realsense   : ./realsense_publish_start.sh
3) Start Unsupervised Segmentation: ./realsense_unsup_segmentation.sh

