# -*- coding:utf-8 -*
import MySQLdb
import sys
import time
import json
import traceback
reload(sys)
sys.setdefaultencoding('utf-8')

lcdb = {'user':'', 'passwd':'', 'dhost':'127.0.0.1', 'dport':3306}

def build_insert_sql(conn, talbe_name, k_v):
    k_v['update_time'] = int(time.time())
    k_v['create_time'] = int(time.time())
    names=[]
    values=[]
    for key in k_v.keys():
        names.append(key)
        value = k_v[key]
        if isinstance(value, basestring) or isinstance(value, str):
            values.append("'%s'"% conn.escape_string(value))
        elif isinstance(value, int):
            values.append("%d"%value)
        elif isinstance(value, float):
            values.append("%f"%value)
        else:
            values.append("%d"%value)
    return "insert ignore into %s (%s) values (%s);" % (talbe_name, ",".join(names), ",".join(values))

def writeDB(talbe_name, k_v, dbase='stock'):
    try:
        conn=MySQLdb.connect(host = lcdb['dhost'], user = lcdb['user'], passwd = lcdb['passwd'], db = dbase, port = lcdb['dport'])
        executeSql = build_insert_sql(conn, talbe_name, k_v)
        cur=conn.cursor()
        cur.execute("SET NAMES utf8")
        try:
            print executeSql
            cur.execute(executeSql)
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        cur.close()
        conn.commit()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error insertList"


def getDB(executeSql, dbase='stock'):
    try:
        conn=MySQLdb.connect(host = lcdb['dhost'], user = lcdb['user'], passwd = lcdb['passwd'], db = dbase, port = lcdb['dport'])
        cur=conn.cursor()
        cur.execute("SET NAMES utf8")
        try:
            cur.execute(executeSql)
            results=cur.fetchall()
            return results
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        cur.close()
        conn.commit()
        conn.close()
    except MySQLdb.Error,e:
        print e
        print "Mysql Error selectList"

def doDB(executeSql, dbase='stock'):
    try:
        conn=MySQLdb.connect(host = lcdb['dhost'], user = lcdb['user'], passwd = lcdb['passwd'], db = dbase, port = lcdb['dport'])
        cur=conn.cursor()
        cur.execute("SET NAMES utf8")
        try:
            print executeSql
            cur.execute(executeSql)
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        cur.close()
        conn.commit()
        conn.close()
    except MySQLdb.Error,e:
        print traceback.print_exc()
        print "Mysql Error insertList"

