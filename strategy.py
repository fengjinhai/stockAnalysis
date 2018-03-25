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
    #executeSql = 'select directorName, num from (select directorName, count(*) as num from stock_change_info where afterAction10Day != "0.00" and changeReason in ("竞价交易", "大宗交易", "二级市场买卖") and changeStockNum>0 group by directorName )tt where num >3;'
    executeSql = 'select changeStockPerson, num from (select changeStockPerson, count(*) as num from stock_change_info where afterAction10Day != "0.00" and changeReason in ("二级市场买卖") and stockBalance>0 and dealPrice !=0 and ori="sh" group by changeStockPerson )tt where num >3;'
    ret = getDB(executeSql, dbase='stock')
    if ret:
        for item in ret:
            changeStockPerson = item[0]
            executeSql = 'select afterAction30Day - afterAction30DayIndex + afterAction50Day - afterAction50DayIndex + afterAction70Day - afterAction70DayIndex as num from stock_change_info where changeStockPerson = "%s"'%changeStockPerson
            res = getDB(executeSql, dbase='stock')
            total  = 0
            for term in res:
                total  = total + term[0]
            directorDic[changeStockPerson] = total
    directorDic = sorted(directorDic.iteritems(), key=lambda d:d[1], reverse = True)
    for item2 in directorDic:
        executeSql = 'select stockCode, stockName, changeStockPerson, changeTime, changeStockNum, dealPrice, dealTimeIndex, changeReason, changePercent, stockBalance, changeStockPerson, companyPosition, relation, afterAction10Day, afterAction30Day, afterAction50Day, afterAction70Day, afterAction90Day, afterAction10DayIndex, afterAction30DayIndex, afterAction50DayIndex, afterAction70DayIndex, afterAction90DayIndex from stock_change_info where changeStockPerson = "%s"'%item2[0]
        ret2 = getDB(executeSql, dbase='stock')
        if ret2:
            f = open('./localfile', 'a')
            for item in ret2:
                values  = []
                for value in item:
                    if isinstance(value, basestring) or isinstance(value, str):
                        values.append("'%s'"% value)
                    elif isinstance(value, int):
                        values.append("%d"%value)
                    elif isinstance(value, float):
                        values.append("%f"%value)
                    else:
                        values.append("%s"%value)
                line  = "\t".join(values)
                print line
                f.write(line + '\t' + str(item2[1]) + '\n')
            f.close()

strategy()
