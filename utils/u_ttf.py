#!/usr/bin/ruby
# -*- coding : utf-8 -*-
# author：samge
# data：2023-02-28 9:26
# describe：
import hashlib
from fontTools.ttLib import TTFont
from utils import u_file
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET


# 中国供应商字体反爬的映射信息
num_dict = {
    "0": "12663173rmoveto00rlineto-211-11-280-56rrcurveto00rlineto-1-5811-28222rrcurveto00rlineto22-11128-157rrcurveto00rlineto056-1128-21-1rrcurveto08rmoveto00rlineto33-419-305-57rrcurveto00rlineto-3-57-19-30-35-3rrcurveto00rlineto-352-1930-259rrcurveto00rlineto4571930333rrcurvetoendchar",
    "1": "126983rmoveto-680rlineto07rlineto160rlineto503307rrcurveto00rlineto0134rlineto06-22-5-3rrcurveto00rlineto-16-8rlineto-38rlineto3922rlineto7-4rlineto0-157rlineto0-73-350rrcurveto00rlineto160rlineto0-7rlinetoendchar",
    "2": "12610656rmoveto60rlineto0-53rlineto-1040rlineto07rlineto4755rlineto1720821023rrcurveto00rlineto021-810-170rrcurveto00rlineto-151-13-12-12-24rrcurveto00rlineto-72rlineto9361818260rrcurveto00rlineto28-215-161-30rrcurveto00rlineto1-18-11-21-23-25rrcurveto00rlineto-39-44rlineto520rlineto11-1710322rrcurveto00rlinetoendchar",
    "3": "1263984rmoveto00rlineto-28rlineto28101415-119rrcurveto00rlineto016-78-130rrcurveto00rlineto-151-14-10-13-20rrcurveto00rlineto-63rlineto11311716231rrcurveto00rlineto26-113-121-24rrcurveto00rlineto0-15-9-13-17-12rrcurveto00rlineto25-312-150-26rrcurveto00rlineto-2-39-24-20-47-2rrcurveto00rlineto-181-95-19rrcurveto00rlineto173461rrcurveto00rlineto305-37-5rrcurveto00rlineto-11102-1rrcurveto00rlineto7-56-250rrcurveto00rlineto1931014225rrcurveto00rlineto331-1711-37-8rrcurvetoendchar",
    "4": "1269460rmoveto250rlineto0-20rlineto-250rlineto0-41rlineto-200rlineto041rlineto-700rlineto019rlineto78122rlineto120rlineto0-121rlineto-790rmoveto590rlineto092rlineto-59-92rlinetoendchar",
    "5": "12698156rmoveto-590rlineto-8-36rlineto50125-211-42rrcurveto00rlineto-3-37-22-20-42-3rrcurveto00rlineto-200-105-19rrcurveto00rlineto083470rrcurveto00rlineto516-38-7rrcurveto00rlineto8-56-330rrcurveto00rlineto171914126rrcurveto00rlineto232-2015-42-1rrcurveto00rlineto-30-1203rrcurveto00rlineto1577rlineto740rlineto-4-16rlineto0-3-2-2-30rrcurveto00rlinetoendchar",
    "6": "126111181rmoveto00rlineto0-8rlineto-43-12-25-25-7-39rrcurveto00rlineto109115120rrcurveto00rlineto29-216-182-34rrcurveto00rlineto-3-35-18-19-33-3rrcurveto00rlineto-351-1823-145rrcurveto00rlineto56334376312rrcurveto-50-85rmoveto00rlineto-90-9-3-9-6rrcurveto00rlineto-1-120-91-7rrcurveto00rlineto1-3610-18191rrcurveto00rlineto1911015030rrcurveto00rlineto130-1115-22-1rrcurvetoendchar",
    "7": "12611177rmoveto1010rlineto0-6rlineto-53-172rlineto-210rlineto52157rlineto-560rlineto-61-3-3-1-6rrcurveto00rlineto-7-22rlineto-60rlineto051rlinetoendchar",
    "8": "1265483rmoveto00rlineto-16-11-8-131-15rrcurveto00rlineto1-2311-1221-1rrcurveto00rlineto1921011119rrcurveto00rlineto015-1415-2715rrcurveto8-84rmoveto00rlineto-312-1714-325rrcurveto00rlineto-11811172315rrcurveto00rlineto-2114-1016118rrcurveto00rlineto2271514292rrcurveto00rlineto27-215-132-24rrcurveto00rlineto1-16-10-14-21-13rrcurveto00rlineto27-1513-18-1-22rrcurveto00rlineto-1-29-17-15-33-1rrcurveto-27148rmoveto00rlineto-1-1410-1421-14rrcurveto00rlineto1512813014rrcurveto00rlineto-118-1010-191rrcurveto00rlineto-15-1-8-9-1-16rrcurvetoendchar",
    "9": "12615-1rmoveto00rlineto-27rlineto43152525735rrcurveto00rlineto-11-11-12-6-130rrcurveto00rlineto-273-1518-233rrcurveto00rlineto1411721331rrcurveto00rlineto35-118-251-49rrcurveto00rlineto0-59-33-36-66-12rrcurveto7595rmoveto00rlineto253-1026-22-1rrcurveto00rlineto-190-9-160-32rrcurveto00rlineto-1-3310-16211rrcurveto00rlineto11196811rrcurvetoendchar",
    "-": "14012694rmoveto0-17rlineto-1130rlineto017rlineto1130rlinetoendchar",
}


def get_num_value(char_string: str) -> str:
    """
    从字典中找出字体对应数字的映射
    :param char_string:
    :return:
    """
    for k, v in num_dict.items():
        if v == char_string:
            return k
    return ''


def format_unicode_lst(unicode_str: str, prefix: str= '') -> list:
    """
    将一个unicode字符串提取每个字符的 {prefix}????? 字符，用于字体关系映射。
    :param unicode_str:
    :param prefix:
    :return:
    """
    return [prefix+'{:X}'.format(ord(char)).lower() for char in unicode_str]


def decode_str(txt: str, font_base64: str, xml_node) -> (str, ET.Element):
    """
    字体反爬解密
    :param txt: 待处理的字符串
    :param font_base64: 字体文件的base64
    :param xml_node: 字体文件中的charStrings节点
    :return:
    """
    result_value = None
    font_name = None
    xml_name = None
    try:
        if not xml_node:
            # 测试将base64转字体文件
            font_name = f"{hashlib.md5(font_base64.encode('utf-8')).hexdigest()}.ttf"
            status = u_file.save_base64(font_base64, f'{font_name}')
            print(f'base64转ttf字体【{status}】：{font_name}')
            # 读取xml信息
            font = TTFont(font_name)
            xml_name = font_name.replace('.ttf', '.xml')
            font.saveXML(xml_name)
            # 读取XML文件
            tree = ET.parse(xml_name)
            root = tree.getroot()
            # 遍历XML文档
            xml_node = get_xml_node(root, 'CFF')
            xml_node = get_xml_node(xml_node, 'CFFFont')
            xml_node = get_xml_node(xml_node, 'CharStrings')
            xml_node = xml_node[1:]
        result_lst = []
        unicode_lst = format_unicode_lst(txt) or []
        for _char in unicode_lst:
            hit_char = False
            for node in xml_node:
                name = node.get('name') or ''
                if name.endswith(_char):
                    hit_char = True
                    text = node.text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                    num = get_num_value(text)
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
