#-*- encoding:utf-8 -*-

import lxml, lxml.etree
import MySQLdb
import lxml.html as x
import re
import logging
import logging.handlers
import os
import sys
import urllib
import urllib2
sys.path.append("lib")
from download import getPage
from myDb import getDB, writeDB


def xpath_extract(doc, xpath):
    return '\n'.join([i.strip() for i in doc.xpath(xpath) if i.strip() != ''])

def getData(c):
    doc = x.document_fromstring(c.decode('utf-8','ignore'))
    for item in doc.xpath("//tr[@class='cls-data-tr']"):
        recordList = []
        for i in range(1, 13):
            recordList.append(xpath_extract(item, ".//td[%d]/text()"%i))
        if recordList[8] == '-':
            recordList[8] = 0
        recordDic = {
            'stockCode':recordList[0],
            'stockName':recordList[1].encode('utf-8'),
            'directorName':recordList[2].encode('utf-8'),
            'changeTime':recordList[3],
            'changeStockNum':int(recordList[4]),
            'dealPrice':float(recordList[5]),
            'changeReason':recordList[6].encode('utf-8'),
            'changePercent':float(recordList[7]),
            'stockBalance':int(recordList[8]),
            'changeStockPerson':recordList[9].encode('utf-8'),
            'companyPosition':recordList[10].encode('utf-8'),
            'relation':recordList[11].encode('utf-8')
        };
        writeDB('director_stock_change', recordDic)

for i in range(500, 2500):
    url = "http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.5142714138156192&ACTIONID=7&AJAX=AJAX-TRUE&CATALOGID=1801_cxda&TABKEY=tab1&tab1PAGENUM=%d&tab1PAGECOUNT=2481&tab1RECORDCOUNT=49607&REPORT_ACTION=navigate"%(i)
    print url
    #html = getPage(url)
    html = urllib2.urlopen(url).read().decode('GBK')
    print html
    exit
    if len(html)>100:
        getData(html)
    else:
        print 'Error: url:%s'%url


