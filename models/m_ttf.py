#!/usr/bin/ruby
# -*- coding : utf-8 -*-
# author：samge
# data：2023-02-28 15:11
# describe：
from typing import Optional
from pydantic import BaseModel


class TtfRequest(BaseModel):
    """字体破解请求体"""
    font_from: int  # 数据来源 ： 7为中国供应商
    font_base64: str  # 字体的base64字符串
    contents: list  # 需要解密的字符串
    test_value: Optional[bool] = False
