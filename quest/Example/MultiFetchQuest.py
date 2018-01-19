#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-31
# @Author  : wure (116988468@qq.com)
# @Version : 2.7.6

from core import *
from core.downloader import Downloader
from core.link_manager import LinkManager
from core.data_model import DataModel

downloader = Downloader()
manager = LinkManager()
log = logger.getLogger("Example", "DEBUG")

seed = []
seed.append('http://www.huodongxing.com/eventlist?orderby=n&tag=%E5%88%9B%E4%B8%9A&city=%E5%85%A8%E9%83%A8')
for i in range(2, 10):
    seed.append('http://www.huodongxing.com/eventlist?orderby=n&tag=%E5%88%9B%E4%B8%9A&city=%E5%85%A8%E9%83%A8&page=' + i.__str__())
manager.append_link(seed)

def save(data, request):

    # 将爬到的数据进行预处理
    date = data['datetime'].encode('utf-8').split(' ～ ')
    beg_datetime = utils.strtotime(date[0])
    date = utils.timetostr(beg_datetime,'%Y-%m-%d')

    # 将要保存的数据存放好
    record = DataModel()
    record.set('link', request)
    record.set('img_link', data['img'])
    record.set('title', data['title'])
    record.set('date', date)
    record.set('datetime', data['datetime'])
    record.set('address', data['address'])
    record.set('publisher', data['publisher'])
    record.set('source', '活动行')

    # 输出数据,检验
    record.dump()

    pass

while manager.is_empty() == False:

    request = manager.get_links(3)
    html = downloader.multiFetch(request)
    utils.sleep(5)
    for page in html:
        try :
            if (utils.has_item(seed, page['link'])):
                fetch = json_parse.parse(page['result'], 'json_parser/example/list.json')
                for data in fetch['record']:
                    url = 'http://www.huodongxing.com' + data['link']
                    manager.append_link(url)
            else:
                data = json_parse.parse(page['result'], 'json_parser/example/detail.json')
                save(data['meta'][0], page['link'])
            manager.finished_request(page['link'])
            log.debug('Finished [' + page['link'] + ']' + manager.report())
        except Exception, e:
            log.error('Crawling [' + page['link'] + '] failed')
            log.error(e)
