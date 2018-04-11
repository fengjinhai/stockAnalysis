#-*- encoding:utf-8 -*-

import time
import datetime
import redis
import MySQLdb
import re
import logging
import logging.handlers
import os
import sys
sys.path.append("lib")
from download import getPage
from myDb import getDB, writeDB, doDB
import chardet
import time
reload(sys) 
sys.setdefaultencoding("utf-8")

def getTimeStamp(t):
    return int(time.mktime(time.strptime(t, '%Y%m%d %H:%M:%S')))

def getNormTime(a):
    x = time.localtime(a)
    return time.strftime('%Y%m%d %H:%M:%S',x)

def aggregateTime(timeDic):
    compareTime = getTimeStamp(timeList[0])
    lastTime = getTimeStamp(timeList[-1])
    retDic = {}
    itemList = []
    b = 1
    for item in timeList:
        timeStamp = getTimeStamp(item)
        if (timeStamp - compareTime) <= 86400*30:
            itemList.append(item)
            retDic[b] = itemList
        else:
            b = b + 1
            itemList = []
            itemList.append(item)
            retDic[b] = itemList
        compareTime = timeStamp
    return retDic

def strategy():
    #选出增持行为大于3次的用户
    directorDic = {}
    executeSql = 'select directorName, num from (select directorName, count(*) as num from director_stock_change where afterAction10Day != "0.00" and changeReason in ("竞价交易", "大宗交易", "二级市场买卖") group by directorName )tt where num >3 limit 100;'
    ret = getDB(executeSql, dbase='stock')
    if ret:
        for item in ret:
            directorName = item[0]
            aggregationDic = {}
            executeSql = 'select id, changeTime from director_stock_change where directorName = "%s" order by changeTime'%directorName
            ret1 = getDB(executeSql, dbase='stock')
            for item1 in ret1:
                aggregationDic[item1[0]] = str(item1[1])
            checkTimeInterval(aggregationDic)
                 

strategy()
