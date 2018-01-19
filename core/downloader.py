#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-03-12
# @Author  : Shoufu (gyming@outlook.com)
# @Version : 2.7.6

import threading
import os
import pickle
import requests
import core.utils as utils
import core.logger as logger


class Downloader:
    """
    通用网页下载器

    对给定的链接进行下载操作.
    """

    # downloader数据源名字配置选项
    WEIBO = 'weibo'

    # cookies 的存放地址
    cookie_base = utils.base_dir() + 'core/login/cookie/'

    # 初始化日志记录器
    log = logger.getLogger('Downloader')

    def __init__(self, charset='utf-8', auto_login=None):
        """
        初始化方法
        :param charset:     网页解析编码
        :param auto_login:  自动登录标识
        :return:
        """
        self.timeout = 60  # 超时秒数
        self.retry = 0  # 超时重试次数
        self.charset = charset  # 解析编码
        self.data = {}  # 请求数据
        self.proxies = {}  # 代理
        self.auto_login = auto_login  # 自动登录标识
        self.params = {}  # URL参数
        self.session = requests.Session()
        self.cookiejar = requests.utils.cookiejar_from_dict({})
        self.headers = {}
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,id;q=0.4,es;q=0.2,pt-BR;q=0.2,pt;q=0.2',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': "1"
        }

        self.multiFetching = False
        self.multiFetchData = []

    def set_proxy(self, key, value):
        """
        设置代理
        传参参考 http://docs.python-requests.org/en/master/user/advanced/#proxies
        :param key:
        :param value:
        :return:
        """
        self.proxies[key] = value

    def auto_load_proxy(self):
        """
        自己添加自动加载代理的逻辑
        :return:
        """
        pass

    def set_timeout(self, timeout):
        """
        设置请求超时秒数
        :param timeout: 请求超时秒数
        :return:
        """
        self.timeout = timeout

    def set_header(self, key, value):
        """
        设置请求头
        :param key:     请求头 Key
        :param value:   请求头 Value
        :return:
        """
        self.headers[key] = value

    def set_data(self, key, value):
        """
        设置请求数据
        :param key:     请求数据 key
        :param value:   请求数据 value
        :return:
        """
        self.data[key] = value

    def set_param(self, key, value):
        """
        设置URL GET方法的参数
        :param key:     参数数据 KEY
        :param value:   参数数据 VALUE
        :return:
        """
        self.params[key] = value

    def set_charset(self, charset):
        """
        设置网页解析编码
        :param charset:
        :return:
        """
        self.charset = charset

    def set_retry(self, retry):
        """
        设置重试次数
        :param retry:
        :return:
        """
        self.retry = retry

    def set_cookie(self, name, value):
        """
        设置 Cookie
        :param name:     cookie name
        :param value:   cookie value
        :return:
        """
        self.cookiejar.set(name, value)

    def load_cookie(self, filename):
        """
        加载 cookie 文件
        :param filename:    cookie 文件名
        :return:
        """
        filename = self.cookie_base + filename
        if (os.path.exists(filename)):
            with open(filename, 'rb') as file:
                self.cookiejar = pickle.load(file)
            return True
        else:
            return False

    def save_cookie(self, filename):
        """
        保存 cookie 到文件
        :param filename:    cookie 文件名
        :return:
        """
        if not os.path.exists(self.cookie_base):
            os.makedirs(self.cookie_base)
        filename = self.cookie_base + filename
        with open(filename, 'wb') as file:
            pickle.dump(self.cookiejar, file)

    def login(self, which, force=False):
        """
        登陆方法入口
        :param which:   登陆标识
        :param force:   是否忽略已有的 cookies
        :return:
        """
        if (which == 'weibo'):
            from core.login import weibo

            weibo.login(self, force)
        elif which == 'itjuzi':
            from core.login import itjuzi

            itjuzi.login(self, force)

    def fetch(self, url, method='DEFAULT'):
        """
        抓取页面主方法
        :param url:     页面链接
        :param method:  请求方法
        :return:
        """
        if self.auto_login is not None: self.login(self.auto_login)  # 判断是否需要自动登录

        if (self.data == {} and method == 'DEFAULT'): method = 'GET'
        if (self.data != {} and method == 'DEFAULT'): method = 'POST'

        data = ''
        retry = 0
        success = False

        while (retry <= self.retry and success == False):
            try:
                self.cookiejar.clear_expired_cookies()
                headers = self.default_headers.copy()
                headers.update(self.headers)
                req = requests.Request(method, url, cookies=self.cookiejar, headers=headers, params=self.params,
                                       data=self.data)
                prepped = req.prepare()
                resp = self.session.send(prepped, proxies=self.proxies, timeout=self.timeout)
                self.cookiejar.update(resp.cookies)
                data = resp.content
                success = True
            except Exception, e:
                retry += 1
                utils.sleep(retry)  # 等待一下再重试
                self.log.error(e.__str__() + ' [' + url + ']')

        data = utils.replace(data, self.charset)  # 进行解码和HTMLDecode

        self.data = {}  # todo 重置 header 保留 cookies

        if (self.multiFetching): # 多线程爬取时调整结果存入方式
            self.multiFetchData.append({'link':url, 'result':data})

        return data

    def multiFetch(self, urlList, method='DEFAULT'):
        """
        多线程爬取

        :param urlList:
        :param method:
        :return:
        """
        self.multiFetching = True  # 通知 Fetch 函数结果存入 multiFetchData
        self.multiFetchData = []  # 初始化
        threads = []

        for link in urlList:
            quest = threading.Thread(target=self.fetch, args=(link, method))
            threads.append(quest)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(self.timeout)

        return self.multiFetchData
