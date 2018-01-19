#!/usr/bin/env python
# coding:utf-8

"""
工具函数集合
"""

import time
import hashlib
import os
import re
import HTMLParser
import random

from vendor.dateutil.parser import *
# from core import logger
# from core.link_manager import LinkManger


def has_item(bucket, item):
    """
    判断集合中是否含有某个元素

    :param bucket:  集合
    :param item:    某个元素
    :return:
    """
    if (type(bucket) == dict):
        for dict_key in bucket:
            if bucket[dict_key] == item: return True
    if (type(bucket) == list):
        for record in bucket:
            if record == item: return True
    if (type(bucket) == set):
        return item in bucket
    return False


def strtotime(timeString, format=None):
    # todo 增加更多的语义化 timeString 判断
    """
    将字符串转化为时间戳

    :param timeString:  字符串
    :param format:      时间字符串的时间格式
    :return:
    """

    if timeString == None: return 0

    # 对语义化时间进行转换
    if (timeString == 'now'):
        return time.time()
    if (timeString == 'today'):
        return strtotime(timetostr('now', '%Y-%m-%d'))

    # 对中文时间进行调整
    timeString = timeString.replace('年','-').replace('月','-').replace('日','')
    timeString = timeString.replace('时',':').replace('分',':').replace('秒','')

    # 对已知格式的时间进行转换
    if format: timeString = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(timeString, format))

    # 对未知格式的时间进行转换
    timeString = parse(timeString)

    # 对时区进行处理
    if (re.match('.*\+.*', str(timeString))):
        offset = int(time.timezone)
    else:
        offset = 0

    utc_tuple = timeString.utctimetuple()
    return int(time.mktime(utc_tuple)) - offset


def timetostr(timeStamp, format='%Y-%m-%d %H:%M:%S'):
    """
    将时间戳转化为字符串

    :param timeStamp:   时间戳
    :param format:      时间字符串格式
    :return:
    """
    if (type(timeStamp) == str):
        stamp = strtotime(timeStamp)
    elif (type(timeStamp) == int or type(timeStamp) == float):
        stamp = timeStamp
    else:
        return False
    return time.strftime(format, time.localtime(stamp))


def md5(string):
    """
    对给定字符串进行 md5 加密

    :param string:  给定字符串
    :return:
    """
    lib = hashlib.md5()
    if isinstance(string, unicode):
        string = string.encode('utf-8')
    elif not isinstance(string, str):
        string = str(string)
    lib.update(string)
    return lib.hexdigest()


def base_dir():
    """
    获取项目的根目录

    :return:
    """
    file_path = os.path.split(os.path.realpath(__file__))[0]
    root = file_path + '/../'
    return root


def replace(text, charset):
    # todo rename to 'iconv'
    """
    对给定字符串进行转码

    :param text:        字符串
    :param charset:     目标编码
    :return:
    """
    parser = HTMLParser.HTMLParser()
    text = text.decode(charset, 'ignore')
    ret = parser.unescape(text)
    return ret


def sub(text):
    # todo 将'多余空格'(2个以上的空格)的定义作为参数传入
    """
    删除给定字符串中的html标签和多余空格

    :param text:
    :return:
    """
    text = re.sub('<.*?>', '', text)
    text = re.sub('\s{2,}', '', text)
    return text.strip()


def real_href(current, href):
    """
    根据页面当前路径和相对路径求出绝对路径

    :param current:     页面当前路径
    :param href:        抓取到的相对路径
    :return:
    """
    if href == '#' or href == '/': return current

    if (current.count('/') > 2):
        base = re.sub('/[^/]*?$', '/', current)
    else:
        base = current + '/'

    if (re.match('^/[^/]', href)):
        base = re.sub('([^/:])/.*', '\g<1>', current)

    if (re.match('^//[^/]', href)):
        return 'http:' + href

    if (re.match('^[^:]+://', href)):
        return href

    url = base + href
    while (re.search('/\./', url)):
        url = re.sub('/\./', '/', url)
    while (re.search('/[^/]*?/\.\./', url)):
        url = re.sub('/[^/]*?/\.\./', '/', url, 1)
    return url.strip('/')


def sleep(seconds=3, rand=False):
    """
    休眠函数

    :param seconds:     休眠秒数
    :param rand:        是否随机休眠
    :return:
    """
    if rand:
        seconds = (random.random() + 1) * seconds
    time.sleep(seconds)


def getdata(data,param,dict='meta'):
    """
    获取json_parser正则中参数为param的字段值
    加入判断字段值是否存在逻辑
    """
    attribute=data[dict][0].get(param)
    if(attribute==None):
        attribute=''
    else:attribute=attribute.strip()
    return attribute
