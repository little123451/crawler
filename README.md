Crawler - 用于抓取页面信息
==========================

起步
--------
`pip install -r requestments.txt`
安装lxml的过程可能会出错，参考[官网指引](http://lxml.de/installation.html#requirements)安装依赖

开发须知
--------
* `_author_` 信息填写可以联系到个人的邮箱、电话、QQ、微信等资料
* 使用三个双引号 `"""` 来表示注释
* 在脚本中开头必须标明 `#!/usr/bin/env python` 以及 `# coding:utf-8`
* 日志名称建议使用大写字母，并用下划线分割单词(如"SOHU_TECH")
* quest 文件夹中按照项目区分文件夹，即使不同项目需要爬同一个站也分开两个文件

分支说明
--------
* 爬虫分支按项目名创建: `quest-项目名`
* `master`负责更新核心代码内容(与爬取业务逻辑不相关的部分)，不进行业务逻辑迭代。
* `publish`为各任务的合并分支，用于部署。
* 爬虫分支按需 merge 主分支(`master`) 的更新内容。

系统优化
--------
0. 引入 `装饰器` 降低开发成本
0. 引入 [Requirements Files](https://pip.pypa.io/en/stable/user_guide/#requirements-files) 管理依赖
0. 学习 [MarkDown](http://wowubuntu.com/markdown) 编写和美化 README [在线编写](https://maxiang.io/)
0. 引入 [PyExecJS](https://pypi.python.org/pypi/PyExecJS) 执行页面 JS 获取 Cookies
0. 引入 python的[XPath](http://www.w3school.com.cn/xpath/index.asp)包[lxml.etree](http://lxml.de/api/index.html)用作Parser中HTML的一种解析方式

定时任务部署
-----------
``` bash
# !/usr/bin/env bash

BASE_DIR=/home/iiip/code/crawler
export PYTHONPATH=$PYTHONPATH:$BASE_DIR
```
