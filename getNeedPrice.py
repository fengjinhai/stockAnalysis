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

r = redis.Redis(host='127.0.0.1',port=6379,db=0)
def getPrice(date, stockCode):
    timeStamp = time.mktime(time.strptime(date,'%Y-%m-%d %H:%M:%S'))
    ltime=time.localtime(timeStamp)
    timeStr=time.strftime("%m/%d/%Y", ltime)
    #key = 'SZ%s_%s'%(stockCode, timeStr)
    #keyIndex = 'SZ399001_%s'%(timeStr)
    key = 'SH%s_%s'%(stockCode, timeStr)
    keyIndex = 'SH000001_%s'%(timeStr)
    ret1 = r.get(key) 
    ret2 = r.get(keyIndex) 
    if ret1 and ret2:
        return (ret1, ret2)
    return False

def dealGetPrice(id, changeDate, stockCode, price, stockIndex, afterDay):
    needDate = changeDate + datetime.timedelta(days = afterDay)
    retVal = getPrice(str(needDate), stockCode)
    if not retVal:
        needDate = changeDate + datetime.timedelta(days = (afterDay+2))
        retVal = getPrice(str(needDate), stockCode)
        if not retVal:
            needDate = changeDate + datetime.timedelta(days = (afterDay+4))
            retVal = getPrice(str(needDate), stockCode)
            if not retVal:
                needDate = changeDate + datetime.timedelta(days = (afterDay+8))
                retVal = getPrice(str(needDate), stockCode)
    
    if retVal:
        stockChangePercent = round(((float(retVal[0]) - float(price))/float(price)), 2)
        indexChangePercent = round(((float(retVal[1]) - float(stockIndex))/float(stockIndex)), 2)
        param1 = 'afterAction%dDay'%afterDay
        param2 = 'afterAction%dDayIndex'%afterDay
        sql = 'update stock_change_info set %s=%f, %s=%f where id=%d'%(param1, stockChangePercent, param2, indexChangePercent, id)
        doDB(sql)
    
def dealTimeIndex(id, changeDate, stockCode):
    retVal = getPrice(str(changeDate), stockCode)
    if not retVal:
        needDate = changeDate + datetime.timedelta(days = (2))
        retVal = getPrice(str(needDate), stockCode)
        if not retVal:
            needDate = changeDate + datetime.timedelta(days = (4))
            retVal = getPrice(str(needDate), stockCode)
            if not retVal:
                needDate = changeDate + datetime.timedelta(days = (8))
                retVal = getPrice(str(needDate), stockCode)
    if retVal:
        sql = 'update stock_change_info set dealTimeIndex = %f where id = %d'%(float(retVal[1]), int(id))
        doDB(sql)

def getNeedPrice():
    executeSql = "select id, changeTime,stockCode,dealPrice,dealTimeIndex from stock_change_info where ori='sh'";
    ret = getDB(executeSql, dbase='stock')
    if ret:
        for item in ret:
            id = item[0]
            changeDate = item[1]
            stockCode =  item[2]
            price =  item[3]
            stockIndex =  item[4]
            if stockCode and stockIndex and price:
                for i in [10, 30, 50, 70, 90]:
                    dealGetPrice(id, changeDate, stockCode, price, stockIndex, i)
            #retVal = dealTimeIndex(id, changeDate, stockCode)

getNeedPrice()
