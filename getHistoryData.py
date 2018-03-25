#-*- coding:utf-8 -*-
import json
import os
import sys
import redis

r = redis.Redis(host='127.0.0.1',port=6379,db=0)
def load_dict():
    for s in os.listdir('./history'):
        prefix = s.replace('.txt','')
        f = open('./history/%s'%s)
        for line in f.readlines():
            dateList = line.strip().split('\t')
            if len(dateList) == 7:
                key = '%s_%s'%(prefix, dateList[0])
                ret = r.set(key, dateList[4]) 
                if not ret:
                    print 'redis set error'

if __name__ == '__main__':
    loadDic = load_dict()
