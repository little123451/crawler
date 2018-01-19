#!/usr/bin/env python
# coding:utf-8


class LinkManager:
    def __init__(self):
        self.linkSet = set([])
        self.finished = set([])
        self.current = set([])

    def report(self):
        remain = len(self.linkSet)
        crawled = len(self.finished)
        ret = 'remained : ' + remain.__str__() + ', crawled : ' + crawled.__str__()
        return ret

    def is_empty(self):
        """
        判断待爬取的链接队列是否为空
        :return:
        """
        flag = not self.linkSet
        return flag

    def get_link(self):
        """
        从待爬取链接队列中获取一条链接
        :return:
        """
        if not self.linkSet:
            ret = False
        else:
            ret = self.linkSet.pop()
            self.current.add(ret)
        return ret

    def get_links(self, count=1):
        """
        从待爬取链接队列中获取数条链接
        :return:
        """
        ret = []
        if not self.linkSet:
            return False
        while (self.linkSet and ret.__len__() < count):
            pop = self.linkSet.pop()
            ret.append(pop)
            self.current.add(pop)
        return ret

    def append_link(self, url):
        """
        将链接添加到待爬取链接队列中
        :param url:
        :return:
        """
        if (type(url) == list):
            for link in url: self.append_link(link)
            return
        if (type(url) == dict):
            for link in url: self.append_link(url[link])
            return
        flag = self.__check_exists(url)
        if flag: return
        self.linkSet.add(url)
        return

    def finished_request(self, url):
        """
        标记某条链接已经爬取完毕
        :param url:
        :return:
        """
        self.finished.add(url)
        self.current.remove(url)
        pass

    def __check_exists(self, Item):
        for url in self.finished:
            if url == Item: return True
        for url in self.current:
            if url == Item: return True
        return False
