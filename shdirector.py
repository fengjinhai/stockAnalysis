#-*- encodingL:utf-8 -*-
import os
import sys
import json
sys.path.append("lib")
from download import getPage,getSpecialPage
from myDb import getDB, writeDB

for i in range(1, 2):
    url = "http://query.sse.com.cn/commonQuery.do?&isPagination=true&sqlId=COMMON_SSE_XXPL_CXJL_SSGSGFBDQK_S&pageHelp.pageSize=25&pageHelp.pageNo=%d&pageHelp.beginPage=%d&pageHelp.cacheSize=1"%(i, i)
    print url
    contentJson = getSpecialPage(url)
    contentDic = json.loads(contentJson)
    dataList = contentDic['pageHelp']['data']
    for item in dataList:
        if item['CURRENT_AVG_PRICE'] == '-':
            item['CURRENT_AVG_PRICE'] = 0
        if item['HOLDSTOCK_NUM'] == '-':
            item['HOLDSTOCK_NUM'] = 0
        if item['CURRENT_NUM'] == '-':
            item['CURRENT_NUM'] = 0
        recordDic = {
            'stockCode':item['COMPANY_CODE'].encode('utf-8'),
            'stockName':item['COMPANY_ABBR'].encode('utf-8'),
            'directorName':'',
            'changeTime':item['CHANGE_DATE'].encode('utf-8'),
            'changeStockNum':int(item['CURRENT_NUM']),
            'changePercent': 0,
            'dealPrice':round(float(item['CURRENT_AVG_PRICE']), 2),
            'changeReason':item['CHANGE_REASON'].encode('utf-8'),
            'stockBalance':int(item['CURRENT_NUM']),
            'changeStockPerson':item['NAME'].encode('utf-8'),
            'companyPosition':item['DUTY'].encode('utf-8'),
            'relation':'',
            'ori':'sh'
        }
        if item['HOLDSTOCK_NUM'] != '0':
            if int(item['CHANGE_NUM'])<0:
                item['CHANGE_NUM'] = 0-int(item['CHANGE_NUM'])
            recordDic['changePercent'] = round((float(item['CHANGE_NUM'])/float(item['HOLDSTOCK_NUM'])), 4)
        writeDB('stock_change_info', recordDic)    
