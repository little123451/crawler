Crawler - 用于抓取页面信息
==========================

起步
--------
`pip install -r requestments.txt`
安装lxml的过程可能会出错，参考[官网指引](http://lxml.de/installation.html#requirements)安装依赖

开发约定
----
* `_author_` 信息填写可以联系到个人的邮箱、电话、QQ、微信等资料
* 使用三个双引号 `"""` 来表示注释
* 在脚本中开头必须标明 `#!/usr/bin/env python` 以及 `# coding:utf-8`
* 日志名称使用驼峰法命名(如"SohuTech")
* quest 目录中按照站点区分文件夹，文件夹内同站点的不同结构数据的爬虫

分支说明
--------
* 爬虫分支按项目名创建: `quest-项目名`
* `master`负责更新核心代码内容(与爬取业务逻辑不相关的部分)，不进行业务逻辑迭代。
* `publish`为各任务的合并分支，用于部署。
* 爬虫分支按需 merge 主分支(`master`) 的更新内容。

参考
--------
0. 使用 [Requirements Files](https://pip.pypa.io/en/stable/user_guide/#requirements-files) 管理依赖
0. 使用 [PyExecJS](https://pypi.python.org/pypi/PyExecJS) 执行页面 JS 获取 Cookies
0. 使用 python的[XPath](http://www.w3school.com.cn/xpath/index.asp)包[lxml.etree](http://lxml.de/api/index.html)用作Parser中HTML的一种解析方式

定时任务部署
-----------
``` bash
# !/usr/bin/env bash

BASE_DIR=/home/iiip/code/crawler
export PYTHONPATH=$PYTHONPATH:$BASE_DIR
```
