# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from typing import List, Optional

import numpy as np


class MergeTextBoxes:
    def __init__(
        self, max_dist: Optional[int] = None, overlap_threshold: Optional[float] = None
    ):
        # x轴方向上合并框阈值
        self.max_dist = max_dist

        # y轴方向上最大重合度
        self.overlap_threshold = overlap_threshold

        self.graph = None
        self.r_index = None
        self.rects = None
        self.image_width = None

    def __call__(self, rects: np.ndarray, image_width: int) -> np.ndarray:
        """

        Args:
            rects (np.ndarray): (N, 4), 左上和右下两个坐标点
            image_width (int): 图像宽度

        Returns:
            _type_: _description_
        """
        self.rects = np.array(rects)
        self.image_width = image_width

        # 构建image_width个空列表？ TODO: 这里有必要构建image_width个吗？
        self.r_index = [[] for _ in range(image_width)]
        for index, rect in enumerate(rects):
            if int(rect[0]) < image_width:
                self.r_index[int(rect[0])].append(index)
            else:
                # 边缘的框旋转后可能坐标越界
                self.r_index[image_width - 1].append(index)

        rect_nums = self.rects.shape[0]
        self.graph = np.zeros((rect_nums, rect_nums))
        for idx, _ in enumerate(self.rects):
            proposal = self.get_proposal(idx)
            if proposal >= 0:
                self.graph[idx][proposal] = 1

        sub_graphs = self.sub_graphs_connected()

        # 不参与合并的框单独存放一个子list
        set_element = sum(sub_graphs, [])
        for idx in range(len(self.rects)):
            if idx not in set_element:
                sub_graphs.append([idx])

        result_rects = []
        for sub_graph in sub_graphs:
            rect_set = self.rects[sub_graph]
            rect_set = self.get_rect_points(rect_set)
            result_rects.append(rect_set)
        return np.array(result_rects)

    def get_proposal(self, index):
        rect = self.rects[index]

        # 只计算到 rect[2] + self.max_dist范围内的框
        for left in range(
            rect[0] + 1, min(self.image_width - 1, rect[2] + self.max_dist)
        ):
            for idx in self.r_index[left]:
                if self.calc_overlap_for_Yaxis(index, idx) > self.overlap_threshold:
                    return idx
        return -1

    def calc_overlap_for_Yaxis(self, index1: int, index2: int) -> float:
        """计算两个框在Y轴方向的重合度(Y轴错位程度)"""
        height1 = self.rects[index1][3] - self.rects[index1][1]
        height2 = self.rects[index2][3] - self.rects[index2][1]

        # 两个框的Y轴重叠程度
        y0 = max(self.rects[index1][1], self.rects[index2][1])
        y1 = min(self.rects[index1][3], self.rects[index2][3])

        Yaxis_overlap = max(0, y1 - y0) / max(height1, height2)
        return Yaxis_overlap

    def sub_graphs_connected(self):
        sub_graphs = []
        for index in range(self.graph.shape[0]):
            cur_row, cur_col = self.graph[index, :], self.graph[:, index]
            if not cur_col.any() and cur_row.any():
                v = index
                sub_graphs.append([v])

                while self.graph[v, :].any():
                    v = np.where(self.graph[v, :])[0][0]
                    sub_graphs[-1].append(v)
        return sub_graphs

    @staticmethod
    def get_rect_points(text_boxes: np.ndarray) -> List[float]:
        x1 = np.min(text_boxes[:, 0])
        y1 = np.min(text_boxes[:, 1])
        x2 = np.max(text_boxes[:, 2])
        y2 = np.max(text_boxes[:, 3])
        return [x1, y1, x2, y2]
