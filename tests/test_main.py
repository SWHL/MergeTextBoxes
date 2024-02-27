# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from merge_text_boxes import BoxesConnector

test_file_dir = cur_dir / "test_files"

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

connector = BoxesConnector(max_dist=15, overlap_threshold=0.2)


def test_normal():
    new_rects = connector(rects, 500)
    assert new_rects.shape == (8, 4)
