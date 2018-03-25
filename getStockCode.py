#-*- encoding:utf-8 -*-
import time
import urllib
import urllib2
import os, sys
import re
reload(sys) 
sys.setdefaultencoding("utf-8")
pattern = re.compile('sz\d{6}')
for i in range(50):
    url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page='+str(i)+'&num=40&sort=symbol&asc=1&node=sz_a#'
    content= urllib2.urlopen(url).read().strip()
    stockList =  re.findall(pattern, content)
    f = open('stock.list', 'a')
    for stockCode in stockList:
        f.write(stockCode+'\n')
    f.close()
    
