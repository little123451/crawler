#!/usr/bin/env python
# coding=utf-8
from datetime import *
import logging
import utils
import os

"""
  使用方法:
    log = logger.getLogger("日志记录器名称", "记录等级")
    log.debug(msg) / log.error(msg) / log.warn(msg) / log.info(msg)
"""

__load = {}


def getLogger(name, level='DEBUG'):
    """
    获取日志记录器

    :param name:    日志记录器名称
    :param level:   日志记录等级
    :return:
    """
    if (not __load.get(name)):
        lvl = __get_level(level)

        logger = logging.getLogger(name)
        logger.setLevel(lvl)

        fileName = name + '_' + date.today().__str__() + '.log'
        if not os.path.exists(utils.base_dir() + 'log/'):
            os.makedirs(utils.base_dir() + 'log/')
        fileHandler = logging.FileHandler(utils.base_dir() + 'log/' + fileName)
        fileHandler.setLevel(logging.DEBUG)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(lvl)

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
        fileHandler.setFormatter(formatter)
        consoleHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
        logger.addHandler(consoleHandler)
        __load[name] = logger
    return __load[name]


def __get_level(level):
    """
    日志记录等级映射表

    :param level:   日志记录等级
    :return:
    """
    level_dict = {
        "OFF": logging.NOTSET,
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    return level_dict[level]


# 兼容,即将弃用
def debug(msg):
    rootLogger = getLogger('')
    rootLogger.debug(msg)


# 兼容,即将弃用
def error(msg):
    rootLogger = getLogger('')
    rootLogger.error(msg)
