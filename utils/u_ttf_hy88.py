#!/usr/bin/ruby
# -*- coding : utf-8 -*-
# author：samge
# data：2023-02-28 9:26
# describe：
import hashlib
import html

from fontTools.ttLib import TTFont
from utils import u_file
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET


# 黄页88字体反爬的映射信息
num_dict = {
    "numbersign": "#",
    "asterisk": "*",
    "plus": "+",
    "hyphenminus": "-",
    "slash": "/",
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}


def get_num_value(char_string: str) -> str:
    """
    从字典中找出字体对应数字的映射
    :param char_string:
    :return:
    """
    return num_dict.get(char_string) or ''
    # for k, v in num_dict.items():
    #     if v == char_string:
    #         return k
    # return ''


def format_unicode_lst(unicode_str: str, prefix: str = '') -> list:
    """
    将一个unicode字符串提取每个字符的 {prefix}????? 字符，用于字体关系映射。
    :param unicode_str:
    :param prefix:
    :return:
    """
    # 兼容html格式字符
    unicode_str = html.unescape(unicode_str)
    return [prefix+'{:X}'.format(ord(char)).lower() for char in unicode_str]


def decode_str(txt: str, font_base64: str, xml_node) -> (str, ET.Element):
    """
    字体反爬解密
        黄页88的字体不涉及变体，这方法废弃
    :param txt: 待处理的字符串
    :param font_base64: 字体文件的base64
    :param xml_node: 字体文件中的charStrings节点
    :return:
    """
    result_value = None
    font_name = None
    xml_name = None
    try:
        # 测试将base64转字体文件
        font_name = f"{hashlib.md5(font_base64.encode('utf-8')).hexdigest()}.ttf"
        status = u_file.save_base64(font_base64, f'{font_name}')
        print(f'base64转ttf字体【{status}】：{font_name}')
        # 读取xml信息
        font = TTFont(font_name)
        xml_name = font_name.replace('.ttf', '.xml')
        font.saveXML(xml_name)

        # 读取xml信息
        font = TTFont(font_name)
        xml_name = font_name.replace('.ttf', '.xml')
        font.saveXML(xml_name)
        # 读取XML文件
        tree = ET.parse(xml_name)
        root = tree.getroot()
        # 遍历XML文档
        map_dict = {}  # 字体code与name的映射字典
        xml_node = get_xml_node(root, 'cmap') or []
        for cmap in xml_node:
            if not cmap.tag.startswith("cmap"):
                continue
            map_node = get_xml_node(cmap, 'map', is_lst=True) or []
            for map_item in map_node:
                code = str(map_item.get('code') or '').replace('0x', '')
                name = str(map_item.get('name') or '')
                map_dict[code] = name

        result_lst = []
        unicode_lst = format_unicode_lst(txt) or []
        for _char in unicode_lst:
            hit_char = False
            for k, v in map_dict.items():
                if _char.upper() == k.upper():
                    hit_char = True
                    num = get_num_value(v)
                    result_lst.append(num)
            if not hit_char:
                result_lst.append(chr(int(_char, 16)))  # 如果没命中，则转回源字符
        result_value = ''.join(result_lst)
        print(f"解析完成：{txt} => {result_value}")
    except Exception as e:
        print(e)
    finally:
        # 删除临时文件
        if font_name or xml_name:
            print(f"清理临时文件：{font_name or ''}   {xml_name or ''}")
            u_file.remove(font_name)
            u_file.remove(xml_name)
        return result_value or txt, xml_node


def get_xml_node(node, goal_tag: str, is_lst: bool = False):
    """
    读取xml中的某个节点
    :param node: 当前要解析的节点
    :param goal_tag: 目标要解析的tag标签
    :param is_lst: 是否读取同名节点列表
    :return:
    """
    tmp_lst = [] if is_lst else None
    for child in node:
        if child.tag == goal_tag:
            if is_lst:
                tmp_lst.append(child)
            else:
                return child
    return tmp_lst
