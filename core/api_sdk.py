#!/usr/bin/env python
# coding:utf-8

"""
对接的 PHP 接口代码: https://gitlab.com/datahunter/interface
"""
import httplib
import json
from core import logger

# 初始化日志记录
__log = logger.getLogger('API_SDK', 'WARN')

# API SDK 配置信息
__private_data = {
    "port": 80,
    "host": "127.0.0.1",
    "timeout": 30,
    "base_url": "/interface/index.php/",
    "api_map": {
        "test": "api/example/test"
    }
}


def __send(data, method, api, param):
    """
    发送 API SDK 请求

    :param data:    请求 body 数据
    :param method:  请求方法
    :param api:     请求接口的名称
    :param param:   请求的 GET 参数
    :return:
    """
    # 根据配置初始化 httpClient
    httpClient = httplib.HTTPConnection(
        __private_data['host'],
        __private_data['port'],
        timeout=__private_data['timeout']
    )

    # 构造链接执行请求
    query = __build_query(param)
    url = __private_data['base_url'] + __private_data['api_map'][api]
    if (query): url = url + '?' + query;
    httpClient.request(method, url, json.dumps(data))
    response = httpClient.getresponse()

    # 记录日志并返回
    __log.debug("method:[" + method + "] status:[" + str(response.status) + "] url:[" + url + "]")

    return response.read()


def __build_query(data):
    """
    构造URL的 query 信息

    :param data:    键值对 ( { keyA : ValueA, KeyB : ValueB } )
    :return:        用于拼接url的query串 ( KeyA=ValueA&KeyB=ValueB )
    """
    query = ''
    if data == None: return ''
    for (key, value) in data.items():
        param = key + '=' + str(value)
        query = query + '&' + param
    return query.strip('&')


def __build_resp(ret):
    """
    预处理 API SDK 的返回

    :param ret:
    :return:
    """
    # 解析返回结果,取出data
    response = json.JSONDecoder().decode(ret)
    data = response['data']

    # 如果返回状态为失败(false)则记录日志
    if response['success'] == False:
        __log.warn(response['msg'])
        return False

    return data

def save(data, api):
    ret = __send(data, 'POST', api, {})
    return ret