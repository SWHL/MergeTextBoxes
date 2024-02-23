# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import cv2
import numpy as np

from merge_text_boxes import BoxesConnector

rects = [
    [144, 5, 192, 25],
    [25, 6, 64, 25],
    [66, 6, 141, 25],
    [193, 5, 275, 33],
    [269, 30, 354, 50],
    [26, 30, 182, 52],
    [185, 28, 265, 55],
    [25, 56, 89, 76],
    [93, 56, 229, 78],
    [232, 56, 262, 76],
    [264, 52, 343, 81],
]

# 创建一个白纸
show_image = np.zeros([500, 500, 3], np.uint8) + 255

connector = BoxesConnector(rects, 500, max_dist=15, overlap_threshold=0.2)
new_rects = connector.connect_boxes()
print(new_rects)

for rect in rects:
    cv2.rectangle(show_image, (rect[0], rect[1]), (rect[2], rect[3]), (0, 0, 255), 1)
cv2.imwrite("origin.png", show_image)

for rect in new_rects:
    cv2.rectangle(show_image, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 0), 1)

cv2.imwrite("res.png", show_image)
