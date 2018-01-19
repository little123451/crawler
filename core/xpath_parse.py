#!/usr/bin/env python
# coding=utf-8
import json
import utils
import logger
from lxml import etree

__json_cache = {}
__log = logger.getLogger("XPATH_PARSER", "WARN")


def __load_json(json_file):
    # 对已加载过的json文件进行缓存，减少文件IO
    if (__json_cache.has_key(json_file)):
        return __json_cache[json_file]
    fp = open(json_file, 'r')
    data = json.JSONDecoder().decode(fp.read())
    fp.close()
    __json_cache[json_file] = data
    return data


def __filter(html, rule):
    html = html[0]
    for pattern in rule:
        nodes = html.xpath(pattern)
        if nodes != [] and isinstance(nodes[0], etree._Element):
            for node in nodes:
                tail_test = node.tail
                node.clear()
                node.tail = tail_test
        else:
            __log.warn('Filter xpath err : "' + pattern + '"')
    __log.debug(etree.tostring(html))
    return [html]


def __inner(html, rule):
    ret = []
    for pattern in rule:
        for tree in html:
            __log.debug(etree.tostring(tree))
            # When xpath() is used on an Element, the XPath expression is evaluated against the element (if relative) or against the root tree (if absolute)
            tree = tree.xpath(pattern)
            ret = ret + tree
            for match in tree:
                __log.debug(etree.tostring(match))
        html = ret
        ret = []
    return html


def __fetch_object(html, rule):
    container = []
    for tree in html:
        temp = {}
        for key, value in rule.items():
            flag = tree.xpath(value)

            # 根据XPATH匹配结果的类型按照需转化并放入temp
            if ( flag != [] and ( isinstance(flag[0], etree._ElementStringResult) or isinstance(flag[0], etree._ElementUnicodeResult) ) ):
                __log.debug(type(flag[0]))
                temp[key] = flag[0]
            elif ( not isinstance(flag, list) and (isinstance(flag, etree._ElementStringResult) or isinstance(flag, etree._ElementUnicodeResult))):
                __log.debug(type(flag))
                temp[key] = flag
            else:
                temp[key] = []
                for fetch in flag:
                    __log.debug(type(fetch))
                    temp[key].append(etree.tostring(fetch))

        if (temp): container.append(temp)
    return container


def parse(html, json_file):
    ret = {}
    base_url = utils.base_dir()
    pattern = __load_json(base_url + json_file)
    temp = []
    temp.append(etree.HTML(html))
    for key, rule in pattern.items():
        temp = __filter(temp, rule['filter'])
        temp = __inner(temp, rule['inner'])
        temp = __fetch_object(temp, rule['fetchObject'])
        ret[key] = temp
        temp = []
        temp.append(etree.HTML(html))
    return ret
