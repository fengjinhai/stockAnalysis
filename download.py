#!/usr/bin/env python
#coding=GBK
import socket
import urllib
import urllib2
import httplib
import urlparse
import time
import StringIO
import gzip
import sys
import random
import traceback


def getSpecialPage(url):
    try:
        request = urllib2.Request(url)
        request.add_header('Accept-Encoding', 'gzip')
        request.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
        request.add_header('Connection', 'keep-alive')
        request.add_header('Cookie', 'PHPStat_First_Time_10000011=1468939610154; PHPStat_Cookie_Global_User_Id=_ck16071922465012283517557177358;PHPStat_Main_Website_10000011=_ck16071922465012283517557177358%7C10000011%7C%7C%7C;PHPStat_Return_Count_10000011=3;PHPStat_Return_Time_10000011=1473340213689;_trs_uv=1le5_532_iqtkptgt')
        request.add_header('Host', 'query.sse.com.cn')
        request.add_header('Referer', 'http://www.sse.com.cn/disclosure/credibility/change/')
        request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36')
        opener = urllib2.build_opener()
        fd = opener.open(request)
        if fd != None:
            contentEncoding = fd.headers.get("Content-Encoding")
            data = None
            if contentEncoding != None and 'gzip' in contentEncoding:
                compresseddata = fd.read()
                compressedstream = StringIO.StringIO(compresseddata)  
                gzipper = gzip.GzipFile(fileobj=compressedstream)
                data = gzipper.read()
            else:
                data = fd.read()

            return data
    except Exception, e:
        traceback.print_exc()
    return None

def getPage(url):
    try:
        request = urllib2.Request(url)
        request.add_header('Accept-Encoding', 'gzip')
        request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36')
        opener = urllib2.build_opener()
        fd = opener.open(request)
        if fd != None:
            contentEncoding = fd.headers.get("Content-Encoding")
            data = None
            if contentEncoding != None and 'gzip' in contentEncoding:
                compresseddata = fd.read()
                compressedstream = StringIO.StringIO(compresseddata)  
                gzipper = gzip.GzipFile(fileobj=compressedstream)
                data = gzipper.read()
            else:
                data = fd.read()

            return data
    except Exception, e:
        traceback.print_exc()
    return None

