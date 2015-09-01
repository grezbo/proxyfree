# -*- coding: UTF-8 -*-

__author__ = 'mork'

import multiprocessing
import urllib2
import time
import ConfigParser
import proxy
import crawler
import threading
import threadpool

mutex = threading.Lock()


config = ConfigParser.ConfigParser()
config.read('setting.conf')

validate_url = config.get('validate', 'validate_url')
validate_keyword = config.get('validate', 'validate_keyword')
validate_timeout = int(config.get('validate', 'validate_timeout'))

thread_num = int(config.get('thread', 'thread_num'))

useable_proxylist = []

def get_proxylist_from_file(file_name):
    proxylist = []
    f = file(file_name, 'r')
    for line in f.readlines():
        t = line.split(',')
        p = proxy.Proxy(t[0], t[1], t[2], t[3], -1)
        proxylist.append(p)
    return proxylist

def get_proxylist_from_crawler():
    return crawler.craw()


def validate_proxy(proxy):
    proxy_url = 'http://%s:%s' % (proxy.ip, proxy.port)
    proxy_handler = urllib2.ProxyHandler({"http": proxy_url})
    opener = urllib2.build_opener(proxy_handler)
    opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]

    try:
        t = time.time()
        response = opener.open(validate_url, timeout=validate_timeout)
        result = response.read()
        delay = time.time() - t
        pos = result.find(validate_keyword)
        if pos > 1:
            proxy.delay = delay
            return proxy
        else:
            proxy.delay = -1
            return proxy
    except Exception, e:
        proxy.delay = -1
        return proxy


def join_proxylist(request, result):
    if result.delay != -1:
        result.print_proxy()
        useable_proxylist.append(result)
    else:
        pass


def get_useable_proxy(poolzise, proxylist):
    pool = threadpool.ThreadPool(poolzise)
    requests = threadpool.makeRequests(validate_proxy, proxylist, join_proxylist)
    [pool.putRequest(req) for req in requests]
    pool.wait()


if __name__ == '__main__':
    # useable_proxy = []
    # plist = get_proxylist_from_file('proxylist.txt')
    plist = get_proxylist_from_crawler()
    print 'crawl finished, get ' + str(len(plist)) + ' proxies'
    get_useable_proxy(thread_num, plist)
    print 'validate finished, get ' + str(len(useable_proxylist)) + ' usable proxies'






