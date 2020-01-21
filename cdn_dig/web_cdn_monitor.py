#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pycurl
import os
from prettytable import PrettyTable

#参数不够直接退出程序
if len(sys.argv) != 4:
    print "Usage : python web_cdn_monitor.py ip_file domain port"
    exit(1)

table = PrettyTable(["CDN节点", "HTTP状态码", "DNS解析时间", "建立连接时间", "准备传输时间", "传输开始时间", "传输结束总时间", "下载数据包大小", "HTTP头部大小", "平均下载速度"])
ip_file=sys.argv[1]
domain=sys.argv[2]
port=sys.argv[3]
checkurl = "http://"+domain+"/do_not_delete/noc.gif"

fd = open(ip_file)
for ip in fd:
    proxy=ip+':'+port
    #print proxy
    c=pycurl.Curl()
    #写回调
    c.setopt(pycurl.URL, checkurl)  # 指定连接的URL
    # 连接超时时间,5秒
    c.setopt(pycurl.CONNECTTIMEOUT, 5)
    # 下载超时时间,5秒
    c.setopt(pycurl.TIMEOUT, 5)
    c.setopt(pycurl.FORBID_REUSE, 1)
    c.setopt(pycurl.MAXREDIRS, 2)
    c.setopt(pycurl.NOPROGRESS, 1)
    c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)
    #设置代理
    c.setopt(pycurl.PROXY, proxy.replace("\n", ""))
    indexfile = open(os.path.dirname(os.path.realpath(__file__)) + "/content.txt", "wb")
    c.setopt(pycurl.WRITEHEADER, indexfile)
    c.setopt(pycurl.WRITEDATA, indexfile)
    try:
        c.perform()
    except Exception, e:
        print ip + " connecion error: " + str(e)
        table.add_row(["%s" %(ip), "error", " -- ", " -- ", " -- ", " -- ", " -- ", " -- ", " -- ", " -- "])
        continue

    NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME)
    CONNECT_TIME = c.getinfo(c.CONNECT_TIME)
    PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME)
    STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME)
    TOTAL_TIME = c.getinfo(c.TOTAL_TIME)
    HTTP_CODE = c.getinfo(c.HTTP_CODE)
    SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD)
    HEADER_SIZE = c.getinfo(c.HEADER_SIZE)
    SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD)

    table.add_row(["%s" %(ip), "%s" % (HTTP_CODE), "%.2f ms" % (NAMELOOKUP_TIME * 1000), "%.2f ms" % (CONNECT_TIME * 1000), "%.2f ms" % (PRETRANSFER_TIME * 1000), "%.2f ms" % (STARTTRANSFER_TIME * 1000), "%.2f ms" % (TOTAL_TIME * 1000), "%d bytes/s" % (SIZE_DOWNLOAD), "%d bytes/s" % (HEADER_SIZE), "%d bytes/s" % (SPEED_DOWNLOAD)]) 
    indexfile.close()
    c.close()

print table

