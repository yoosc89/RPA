'''
parser list 등록 후  parser_db 와 code_dict - site_code 추가   

'''

import requests
from bs4 import BeautifulSoup as bs
import sql
from datetime import datetime
import re
import concurrent.futures
import os
import itertools

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}


def parser_db2():
    print(f'parser_start [{datetime.now()}]')
    convert_def = [clien_jirum, ppomppu,
                   quasarzone, ruliweb, coolenjoy]

    core = os.cpu_count()
    pool = concurrent.futures.ProcessPoolExecutor(max_workers=core)
    procs = []
    for i in convert_def:
        procs.append(pool.submit(i))
    url_list = []

    for i in concurrent.futures.as_completed(procs):
        url_list.append(i.result())

    url_list = list(itertools.chain(*url_list))
    sql.insert_alert_site(url_list)


def clien_jirum():  # parser
    domain_name = 'clien_jirum'
    url = 'https://www.clien.net'
    get_html = requests.get(url+'/service/board/jirum')
    parser = bs(get_html.text, 'html.parser')

    elements_title = parser.select('span.list_subject')

    list_title = []
    for i in elements_title:
        list_title.append(
            [domain_name, i.attrs['title'], i.a.attrs['href'], url])

    return list_title


def ppomppu():  # parser
    domain_name = 'ppomppu'
    url = 'https://www.ppomppu.co.kr/zboard/'
    get_html = requests.get(url+'zboard.php?id=ppomppu')
    parser = bs(get_html.text, 'html.parser')

    elements_title = parser.select('tr > td > div > a ')
    elements_ad = parser.select('table > tbody > tr > td > div > a ')

    list_title = []
    ad_list = []
    for i in elements_ad:
        ad_list.append(i.text)

    for i in elements_title:
        if ad_list.count(i.text) == 0:
            list_title.append([domain_name, i.text, i.attrs['href'], url])
        else:
            pass

    return list_title


def quasarzone():
    domain_name = 'quasarzone'
    url = 'https://quasarzone.com'
    get_html = requests.get(url+'/bbs/qb_saleinfo', headers=headers)
    parser = bs(get_html.text, 'html.parser')

    elements_title = parser.select('div > div.market-info-list-cont > p > a')
    list_title = []
    for i in elements_title:
        list_title.append([domain_name, i.span.text, i['href'], url])
    return list_title


def ruliweb():
    domain_name = 'ruliweb'
    url = 'https://bbs.ruliweb.com'
    get_html = requests.get(url+'/market/board/1020', headers=headers)
    parser = bs(get_html.text, 'html.parser')

    elements_title = parser.select('tr > td > div > a.deco')

    list_title = []
    for i in elements_title:
        list_title.append([domain_name, i.text, re.sub(
            'https://bbs.ruliweb.com', '', i.attrs['href']), url])

    return list_title


def coolenjoy():
    domain_name = 'coolenjoy'
    url = 'https://coolenjoy.net'
    get_html = requests.get(url+'/bbs/jirum', headers=headers)
    parser = bs(get_html.text, 'html.parser')

    elements_title = parser.select('td.td_subject > a')

    list_title = []
    # print(elements_title)
    for i in elements_title:
        title = i.text.strip()[:i.text.strip().find('댓글')].strip()
        link = re.sub('https://coolenjoy.net:443', '', i.attrs['href'])
        list_title.append([domain_name, title, link, url])

    return list_title


""" def sample():
    domain_name = ''
    url = ''
    get_html = requests.get(url+'add_url', headers=headers)
    parser = bs(get_html.text,'html.parser')

    elements_title = parser.select('')
    list_title = []
    for i in elements_title:
        list_title.append([domain_name, 'title', 'bbs_url', url])
        
    return list_title """
