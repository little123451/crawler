#!/usr/bin/env python
# coding=utf-8
import re
import json
import utils
__json_cache = {}

def __load_json(json_file):
    # 对已加载过的json文件进行缓存，减少文件IO
    if (__json_cache .has_key(json_file)) :
        return __json_cache[json_file]
    fp = open(json_file, 'r')
    data = json.JSONDecoder().decode(fp.read())
    fp.close()
    __json_cache[json_file] = data
    return data


def __filter(html, rule):
    ret = []
    for block in html:
        for pattern in rule:
            block = re.subn(pattern, '', block)[0]
        ret.append(block)
    return ret


def __inner(html, rule):
    ret = []
    for pattern in rule:
        for block in html:
            temp = __find_all(pattern, block)
            ret.extend(temp)
        html = ret
        ret = []

    return html


def __find_all(p, block):
    temp = []
    pattern = '(' + p + ')'
    match = re.findall(pattern, block)
    if isinstance(match,list) and len(match)>0 and isinstance(match[0],tuple):
        for fetch in match :  temp.append(fetch[0])
    else: temp = match
    return temp


def __fetch_object(html, rule):
    container = []

    for block in html:
        temp = {}
        for key, value in rule.items():
            flag = re.findall(value, block)
            if (flag): temp[key] = flag[0]
            else : temp[key] = ''
        if (temp): container.append(temp)
    return container


def parse(html, json_file):
    ret = {}
    base_url = utils.base_dir()
    pattern = __load_json(base_url + json_file)
    temp = []
    temp.append(html)
    for key, rule in pattern.items():
        temp = __filter(temp, rule['filter'])
        temp = __inner(temp, rule['inner'])
        temp = __fetch_object(temp, rule['fetchObject'])
        ret[key] = temp
        temp = []
        temp.append(html)
    return ret
