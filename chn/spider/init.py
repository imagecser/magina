"""
created on 10/24/2017

"""
#! /usr/bin/python3
# coding: utf-8
import multiprocessing
import re
import time
import os
import requests
from style import *
import queue
from bs4 import BeautifulSoup

start_url = "http://www.nju.edu.cn"
que = multiprocessing.Queue()
pages = set(start_url)
header = {
    'User-Agent': 'Baiduspider+(+http://www.baidu.com/search/spider.htm)'
}
invalid_urls = set()
page_lock = multiprocessing.Lock()
print_lock = multiprocessing.Lock()
extensions = ('.doc', '.pdf', 'docx', '.rar', '.xls',
              '.xlsx', '.txt', '.zip', '.jpg', ',png')


def request_page(url):
    try:
        context = requests.get(url, headers=header, timeout=3).text
        return True, url, context
    except requests.Timeout:
        invalid_urls.add(url)
        return False, url, ""


def parse_page(url, context):
    global que, pages
    soup = BeautifulSoup(context, 'lxml')
    base_url = '/'.join(url.split('/')[:3])
    for url in soup.find_all('a', href=True):
        href = re.sub('#[^/]+?$', '', url.attrs['href'])
        if href.lower().endswith(extensions):
            continue
        if re.match('^http', href):
            if re.match(base_url, href) and href not in pages:
                with page_lock:
                    pages.add(href)
                que.put(href)
        else:
            if len(href) > 0:
                if href[0] != '/':
                    href = '/' + href
                href = base_url + href
                if href not in pages:
                    with page_lock:
                        pages.add(href)
                    que.put(href)
    for unused in soup(['script', 'style']):
        unused.extract()
    return ' '.join(soup.get_text().split())


def work():
    global que
    while que.qsize() > 0:
        url = que.get()
        status, url, context = request_page(url)
        if status:
            with print_lock:
                print(url + stylish(' ok', fore='green'))
            parse_page(url, context)
        else:
            with print_lock:
                print(url + stylish(' error', fore='red'))


que.put(start_url)
size_threads = 100
# threads = []
# for i in range(size_threads):
#     threads.append(multiprocessing.Process(target=work, name=str(i)))
# for i in range(size_threads):
#     with print_lock:
#         print("thread %d start." % i)
#     threads[i].start()
# for t in threads:
#     t.join()
pool = multiprocessing.Pool(size_threads)
for i in range(size_threads):
    pool.apply_async(work)
pool.close()
pool.join()
