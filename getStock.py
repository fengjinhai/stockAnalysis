# -*- coding: utf-8 -*-
import os, sys, urllib, urllib2, json

f = open('stock.list')
for line in f.readlines():
    stockCode = line.strip()
    url = 'http://apis.baidu.com/apistore/stockservice/stock?stockid=%s'%line
    req = urllib2.Request(url)
    req.add_header("apikey", "5ec4419a691538523ed775119aa741f4")
    resp = urllib2.urlopen(req)
    content = resp.read()
    if(content):
        codeName = json.loads(content)['retData']['stockinfo']['name'].encode('utf-8')
        print json.loads(content)['retData']['stockinfo']
        print stockCode+'\t'+codeName
f.close()
