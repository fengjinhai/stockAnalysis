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

def strategy():
    #选出增持行为大于3次的用户
    directorDic = {}
    #executeSql = 'select directorName, num from (select directorName, count(*) as num from stock_change_info where afterAction10Day != "0.00" and changeReason in ("竞价交易", "大宗交易", "二级市场买卖") and stockBalance>0 group by directorName )tt where num >3;'
    executeSql = 'select changeStockPerson, num from (select changeStockPerson, count(*) as num from stock_change_info where afterAction10Day != "0.00" and changeReason in ("二级市场买卖", "其他") and stockBalance>0 and dealPrice !=0 and ori="sh" group by changeStockPerson )tt where num >3;'
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
            #print changeStockPerson + '\t' + str(total)
    directorDic = sorted(directorDic.iteritems(), key=lambda d:d[1], reverse = True)
    print directorDic
    '''
    for item2 in directorDic:
        print item2
        for k,v in item2.items():
            print k,v
            #print directorName
    '''
strategy()
