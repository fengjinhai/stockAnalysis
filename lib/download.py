#!/usr/bin/env python
#coding=utf-8
import socket
import urllib
import traceback
import urllib2
import urllib
import httplib
import urlparse
import time
import StringIO
import gzip
import sys
import random
import md5
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
socket.setdefaulttimeout( 30 )

def getPage(url, retry=1, proxy = None, agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22'):
    t = 0
    while t < retry:
        if t > 1:
            proxy = None 
        fd = None
        try:
            request = urllib2.Request(url)
            request.add_header('Accept-encoding', 'gzip')
            request.add_header('User-Agent', agent)
            if proxy != None:
                request.set_proxy(proxy, "http")
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
            print >> sys.stderr, "download %s by proxy %s error: %s" %(url, proxy,str(e)) 
            if hasattr(e,'code') and e.code == 404: 
                return None
            t += 1
            time.sleep(3)
        if fd != None:  fd.close()
    return None

def getPage_ori(url, retry=3, interval=0.5, proxy = None, agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22'):
    t = 0
    while t < retry:
        if t > 1:
            proxy = None 
        fd = None
        try:
            request = urllib2.Request(url)
            request.add_header('Accept-encoding', 'gzip')
            request.add_header('User-Agent', agent)
            if proxy != None:
                request.set_proxy(proxy, "http")
            opener = urllib2.build_opener()
            fd = opener.open(request)
            if fd != None:
                #if 'text/html' not in fd.headers.get("Content-Type") and \
                #    "text/xml" not in fd.headers.get("Content-Type") and \
                #    "text/css" not in fd.headers.get("Content-Type")  :
                #    return None
                
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
            print >> sys.stderr, "download %s by proxy %s error: %s" %(url, proxy,str(e)) 
            if hasattr(e,'code') and e.code == 404: 
                return None
            t += 1
            time.sleep(interval * t)
            
        if fd != None:  fd.close()
        
    return None

def getPostPage(paramDic, url, retry=3, interval=0.5, proxy = None,
        agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22'):
    t = 0
    while t < retry:
        if t > 1:
            proxy = None 
        fd = None
        try:
            params = urllib.urlencode(paramDic)
            request = urllib2.Request(url, params)
            requestders = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            request.add_header('Accept-encoding', 'gzip')
            request.add_header('User-Agent', agent)
            if proxy != None:
                request.set_proxy(proxy, "http")
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
            print >> sys.stderr, "download by proxy %s error: %s" %(proxy,str(e)) 
            if hasattr(e,'code') and e.code == 404:      #ÍøÒ³²»´æÔÚ
                return None
            t += 1
            time.sleep(interval * t)
            
        if fd != None:  fd.close()
        
    return None

def getImage(url, retry = 3, interval = 0.5):
    imgData = None
    t = 0
    while t < retry:
        fd = None
        try:
            fd = urllib.urlopen(url)
            if fd != None:
                imgData = fd.read()

                return imgData
        except Exception, e:
            print >> sys.stderr, "download %s error: %s" %(url,str(e))
            t += 1
            time.sleep(interval * t)  
              
        if fd != None:  fd.close()

    return imgData
        
if __name__ == "__main__" :
    #url = 'http://ahmedabad.yellowpages.co.in/Advertising+Service+Banner'
    #print getPage(url)
    paramDic = {'mcatName':'Bumper' ,'mcatId':64785 ,'catId':39, 'end':28 ,'rand':5, 'prod_serv':'P' ,'showkm':0 ,'debug_mod':0, 'price':0 ,'cntAll':27}
    print getPostPage(paramDic)
