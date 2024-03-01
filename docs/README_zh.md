<div align="center">
  <div align="center">
    <h1><b>文本检测框合并</b></h1>
  </div>
  <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
  <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Mac%2C%20Win-pink.svg"></a>
<a href="https://pypi.org/project/merge_text_boxes/"><img alt="PyPI" src="https://img.shields.io/pypi/v/merge_text_boxes"></a>
<a href="https://pepy.tech/project/merge_text_boxes"><img src="https://static.pepy.tech/personalized-badge/merge_text_boxes?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
  <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
  <a href="https://github.com/SWHL/MergeTextBoxes/blob/8da071f678d4e3d0681fff8b213a5aa9c1a96073/LICENSE"><img alt="GitHub" src="https://img.shields.io/badge/license-Apache 2.0-blue"></a>

  简体中文 | [English](https://github.com/SWHL/MergeTextBoxes)
</div>

### 简介
该仓库主要用来合并同行文本框，代码修改自[merge_text_boxs](https://github.com/zcswdt/merge_text_boxs)项目，并做了进一步整理和扩展。

### TODO
- [ ] 支持y轴方向合并
- [ ] 支持倾斜文本框合并

### 安装
```bash
pip install merge_text_boxes
```

### 使用
```python
import copy

import cv2
import numpy as np

from merge_text_boxes import MergeTextBoxes

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
show_image = np.zeros([100, 500, 3], np.uint8) + 255

connector = MergeTextBoxes(max_dist=15, overlap_threshold=0.2)
new_rects = connector(rects, 500)

tmp_img = copy.deepcopy(show_image)
for rect in rects:
    cv2.rectangle(tmp_img, (rect[0], rect[1]), (rect[2], rect[3]), (0, 0, 255), 1)
cv2.imwrite("origin.png", tmp_img)

for rect in new_rects:
    cv2.rectangle(show_image, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 0), 1)

cv2.imwrite("res.png", show_image)
```

### 可视化
合并前：

![alt text](origin.png)

合并后：

![alt text](res.png)

### 致谢
- [OCR文字检测框的合并](https://blog.csdn.net/jhsignal/article/details/107840145)
- [merge_text_boxs](https://github.com/zcswdt/merge_text_boxs)

### 贡献指南
欢迎提交请求。对于重大更改，请先打开issue讨论您想要改变的内容。

请确保适当更新测试。

### [赞助](https://rapidai.github.io/RapidOCRDocs/docs/sponsor/)
如果您想要赞助该项目，可直接点击当前页最上面的Sponsor按钮，请写好备注(**您的Github账号名称**)，方便添加到赞助列表中。


### 开源许可证
该项目采用[Apache 2.0](../LICENSE)开源许可证。