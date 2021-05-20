"""
@Author : Chan Tai Wing
@Date   : 18 May 2021
@About  : Segmentation Algorithm
"""
# pip install torch==1.4.0 torchvision==0.5.0
# pip install future

# System Packages
import torchvision
from torchvision import transforms as T
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random

# Customized Packages
import information as info

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

def get_prediction(model,rgb_img, threshold):
    transform = T.Compose([T.ToTensor()])
    rgb_image = transform(rgb_img)
    model.cuda()
    rgb_image = rgb_image.cuda()
    pred = None
    pred = model([rgb_image])
    pred_score = list(pred[0]['scores'].detach().cpu().numpy())
    x = [pred_score.index(x) for x in pred_score if x > threshold]
    # Check whether detection result is empty
    if(len(x)>0):
        pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1]
        masks = (pred[0]['masks'] > 0.5).squeeze().detach().cpu().numpy()
        pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].cpu().numpy())]
        pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().cpu().numpy())]
        masks = masks[:pred_t+1]
        pred_boxes = pred_boxes[:pred_t+1]
        pred_class = pred_class[:pred_t+1]
    else:
        masks = None
        pred_boxes = None
        pred_class = None
    return masks, pred_boxes, pred_class

def random_colour_masks(rgb_image):
    colours = [[0, 255, 0],[0, 0, 255],[255, 0, 0],[0, 255, 255],
				[255, 255, 0],[255, 0, 255],[80, 70, 180],
				[250, 80, 190],[245, 145, 50],[70, 150, 250],
				[50, 190, 190]]
    r = np.zeros_like(rgb_image).astype(np.uint8)
    g = np.zeros_like(rgb_image).astype(np.uint8)
    b = np.zeros_like(rgb_image).astype(np.uint8)
    r[rgb_image == 1], g[rgb_image == 1], b[rgb_image == 1] = colours[random.randrange(0, 10)]
    coloured_mask = np.stack([r, g, b], axis=2)
    return coloured_mask

def core(model,rgb_image, threshold=0.5, rect_th=3, text_size=3, text_th=3):
    masks, boxes, pred_cls = get_prediction(model,rgb_image, threshold)
    rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
    if(masks is not None):
        for i in range(len(masks)):
            rgb_mask = random_colour_masks(masks[i])
            rgb_image = cv2.addWeighted(rgb_image, 1, rgb_mask, 0.5, 0)
            cv2.rectangle(rgb_image, boxes[i][0], boxes[i][0], color=(0, 255, 0), thickness=rect_th)
            cv2.putText(rgb_image, pred_cls[i], boxes[i][0], cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 255, 0), thickness=text_th)
    return rgb_image