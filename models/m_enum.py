#!/usr/bin/ruby
# -*- coding : utf-8 -*-
# author：samge
# data：2023-02-28 17:48
# describe：
import enum


class FontFrom(enum.Enum):
    """ 字体来源，目前只有一个值，其他值需要再加 """
    CHINA_CN = 7  # 中国供应商
    HUANG_YE_88 = 8  # 黄页88
