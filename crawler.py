# -*- coding: UTF-8 -*-

__author__ = 'mork'

"""
this python script is used to catch proxy from www.cnproxy.com
"""

import urllib2
from bs4 import BeautifulSoup
import re
import proxy


def get_urllist():
    cnproxy_url = 'http://www.cnproxy.com/'
    request = urllib2.Request(cnproxy_url)
    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response, 'lxml', from_encoding='gb18030')

    urllist = []
    for i in soup.find('div', id='plist').find_all('a'):
        urllist.append(cnproxy_url+i.get('href'))
    return urllist


def get_proxylist(url):
    proxylist = []
    port_map ={'v': '3',
               'm': '4',
               'a': '2',
               'l': '9',
               'q': '0',
               'b': '5',
               'i': '7',
               'w': '6',
               'r': '8',
               'c': '1'}
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    response = urllib2.urlopen(request)
    t = re.compile(r'''<td>(.+?)<SCRIPT type=text/javascript>document.write\(":"\+(.+?)\)</SCRIPT></td><td>(.+?)</td><td>.+?</td><td>(.+?)</td></tr>''')
    s = response.read()
    matches = t.findall(s)
    for match in matches:
        p = proxy.Proxy(match[0], ''.join(map(lambda x: port_map[x], match[1].split('+'))), match[2], match[3].decode('gb18030').encode('UTF-8'), -1)
        proxylist.append(p)
    return proxylist


def craw():
    proxylist = []
    urllist = get_urllist()
    for url in urllist:
        proxylist.extend(get_proxylist(url))
    return proxylist

if __name__ == '__main__':
    # urllist = get_urllist()
    # for url in urllist:
    #     f = file('proxylist.txt', 'a')
    #     proxylist = get_proxylist(url)
    #     for i in proxylist:
    #         line = i['ip'] + ',' + i['port'] + ',' + i['type'] + ',' + i['info'] + '\n'
    #         f.write(line)
    #     f.close()

    urllist = get_urllist()
    proxylist = []
    for url in urllist:
        proxylist.extend(get_proxylist(url))
    for i in proxylist:
        i.print_proxy()

