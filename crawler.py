# -*- coding: UTF-8 -*-

__author__ = 'mork'

import urllib2
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from proxy import Proxy
import datetime
import random
import time


def get_db_session():
    engine = create_engine('sqlite:///proxy.db')
    db_session = sessionmaker(bind=engine)
    return db_session()


def get_raw_page(page_url):
    time.sleep(random.randint(2, 5))
    request = urllib2.Request(page_url)
    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    response = urllib2.urlopen(request)
    return BeautifulSoup(response, 'lxml')


def get_urls(type='all'):
    def get_specific_urls(t):
        specific_page_list = []
        specific_url = 'http://www.xicidaili.com/'+t+'/'
        nn = get_raw_page(specific_url)
        lastpage_num = nn.find('div', class_='pagination').find_all('a')[-2].string
        for num in range(1, int(lastpage_num)+1):
            specific_page_list.append(specific_url+str(num))
        return specific_page_list
    url_list = []
    if type == 'all':
        url_list.extend(get_specific_urls('nn'))
        url_list.extend(get_specific_urls('nt'))
        url_list.extend(get_specific_urls('wn'))
        url_list.extend(get_specific_urls('wt'))
        url_list.extend(get_specific_urls('qq'))
    else:
        url_list.extend(get_specific_urls(type))
    return url_list


def get_proxies(page_url):
    print page_url
    raw_page = get_raw_page(page_url)
    proxy_list = []
    for tr in raw_page.find('table', id='ip_list').find_all('tr')[1:]:
        td = tr.find_all('td')
        p = Proxy()
        p.proxy_country = td[1].img.get('alt').upper()
        p.proxy_ip = td[2].string
        p.proxy_port = td[3].string
        p.proxy_location = td[4].text.replace('\n', '').replace(' ', '')
        p.proxy_type = td[5].string
        p.connection_type = td[6].string.replace(u'代理', '').upper()
        p.validation_delay = td[7].find('div', {'class': 'bar'})['title'].replace(u'秒', '')
        p.connection_delay = td[8].find('div', {'class': 'bar'})['title'].replace(u'秒', '')
        p.validate_time = datetime.datetime.strptime('20'+td[9].string, '%Y-%m-%d %H:%M')
        proxy_list.append(p)
    return proxy_list


if __name__ == '__main__':
    session = get_db_session()
    url_list = get_urls()
    print 'get urls ready'
    for url in url_list:
        proxy_list = get_proxies(url)
        print 'crawling from %s' % url
        for proxy in proxy_list:
            session.add(proxy)
        session.commit()
    session.close()




