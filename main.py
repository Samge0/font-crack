#!/usr/bin/ruby
# -*- coding : utf-8 -*-
# author：samge
# data：2023-02-28 14:56
# describe：

from fastapi import Depends, FastAPI, Header, HTTPException

from models.m_enum import FontFrom
from models.m_ttf import TtfRequest
from utils import u_http, u_ttf, u_file

# api的简易token验证
access_token = eval(u_file.read('config.json')).get('auth_token')


async def verify_token(Authorization: str = Header(...)):
    """ token简易验证 """
    if Authorization != f"Bearer {access_token}":
        print(f"认证失败：{Authorization}")
        u_http.fail403(msg='Authorization header invalid')


app = FastAPI(dependencies=[Depends(verify_token)])


@app.get("/")
async def index():
    return u_http.success('字体反反爬的API')


@app.post("/crack/font")
async def crack_font(request: TtfRequest):
    if request.font_from != FontFrom.CHINA_CN.value:
        return u_http.fail400(msg="暂未支持的类型")

    tmp_lst = []
    xml_node = None
    for content in request.contents:
        content, xml_node = u_ttf.decode_str(content, request.font_base64, xml_node)
        tmp_lst.append(content)
    return u_http.success(tmp_lst)
