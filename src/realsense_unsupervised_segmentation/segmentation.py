# System Packages
import torch
import torch.nn as nn
import torch.nn.init
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets,transforms
from torch.autograd import Variable

import cv2
import sys
import numpy as np

from skimage import segmentation

# Customize Packages
import handler_config as hc
import network

# Get a static image and saved
def freeze_image(rgb_image):
    # When capture button is pressed
    file_name = None
    if hc.capture_image:
        file_name = '/home/vincent/vincent-dev/realsense_acp_robot/src/realsense_unsupervised_segmentation/sample/img_' \
            + str(hc.capture_index) + '.jpg'
        cv2.imwrite(file_name,rgb_image)
        hc.capture_index += 1
        hc.capture_image = False
    return True,file_name


# Pick a picture and start training
def single_image_training(rgb_image):
    im_target_rgb = rgb_image
    image_ready = False
    # Make sure image is captured
    while not(image_ready):
        image_ready,file_name = freeze_image(rgb_image)


    # Start training    
    #file_name = '/home/vincent/vincent-dev/realsense_acp_robot/src/realsense_unsupervised_segmentation/sample/img_0.jpg'
    img = cv2.imread(file_name)
    if(img is not None):
        print("Image is found")
        # Data conversion from opencv to pytorch with CUDA supported
        data = torch.from_numpy(np.array([img.transpose( (2, 0, 1) ).astype('float32')/255.]))
        data = data.cuda()
        data = Variable(data)

        # Segmentation
        labels = segmentation.slic(img, compactness=hc.compactness, n_segments=hc.segments)
        labels = labels.reshape(img.shape[0]*img.shape[1])

        # Find unique labels
        u_labels = np.unique(labels)
        l_inds = []
        for i in range(len(u_labels)):
            l_inds.append(np.where(labels==u_labels[i])[0])

        # Ready to traing
        model = network.unsupCNN(data.size(1))
        model.cuda()
        model.train()
        loss_fn = torch.nn.CrossEntropyLoss()
        optimizer = optim.SGD(model.parameters(), lr=hc.learning_rate, momentum=0.9)
        label_colours = np.random.randint(255,size=(100,3))
        for batch_idx in range(hc.max_epoch):
            # forwarding
            optimizer.zero_grad()
            output = model(data)[0]
            output = output.permute( 1, 2, 0 ).contiguous().view(-1,hc.num_neurons_basic)
            ignore, target = torch.max(output,1)
            im_target = target.data.cpu().numpy()
            nLabels = len(np.unique(im_target))
            im_target_rgb = np.array([label_colours[ c % 100 ] for c in im_target])
            im_target_rgb = im_target_rgb.reshape(img.shape).astype(np.uint8)
            cv2.imshow("output", im_target_rgb)
            cv2.waitKey(1)      

            # Superpixel refinement
            for i in range(len(l_inds)):
                labels_per_sp = im_target[ l_inds[ i ] ]
                u_labels_per_sp = np.unique( labels_per_sp )
                hist = np.zeros( len(u_labels_per_sp) )
                for j in range(len(hist)):
                    hist[ j ] = len( np.where( labels_per_sp == u_labels_per_sp[ j ] )[ 0 ] )
                im_target[ l_inds[ i ] ] = u_labels_per_sp[ np.argmax( hist ) ]    
            target = torch.from_numpy(im_target)
            target = target.cuda()
            target = Variable(target)
            loss = loss_fn(output,target)
            loss.backward()
            optimizer.step()     

            print (batch_idx, '/', hc.max_epoch, ':', nLabels, loss.item())

            if (nLabels <= hc.min_num_labels):
                training_msg = "nLabels", nLabels, "reached minLabels", min_num_labels, "."
                print(training_msg)
                break

    return im_target_rgb

def core (rgb_image):
    return rgb_image
