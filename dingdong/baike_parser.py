#!/usr/bin/python
# Copyright 2013 Beyondant. All Right Reserved.
# Date: 2013-05-10

__author__ = 'cuberub@gmail.com'

import sys
import datetime
import random
import socket
import time
import urllib
import chardet
import codecs
from lxml import etree
import http_util

def utf8_to_gbk(s):
  return unicode(s, 'utf8', 'ignore').encode('gbk', 'ignore')

def coding_to_utf8(s):
  curr_coding = chardet.detect(s)["encoding"]
  if curr_coding != "utf-8":
    return s.decode(curr_coding, 'ignore').encode('utf-8')
  return s

def fetch_url(url):
  socket.setdefaulttimeout(3)
  headers = {}
  headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
  headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
  headers['Accept-Language'] = 'zh-cn,en-us;q=0.7,en;q=0.3'
  headers['Accept-Charset'] = 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
  headers['Referer'] = ''
  fetcher = http_util.UrlFetcher()
  resp = fetcher.fetch(url, headers = headers)
  return resp.body

def fetch_baidu_baike_by_keyword(keyword):
  socket.setdefaulttimeout(3)
  headers = {}
  headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
  headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
  headers['Accept-Language'] = 'zh-cn,en-us;q=0.7,en;q=0.3'
  headers['Accept-Charset'] = 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
  headers['Referer'] = ''
  fetcher = http_util.UrlFetcher()
  url = "http://baike.baidu.com/search/word?pic=1&sug=1&enc=utf8&word=" + keyword
  resp = fetcher.fetch(url, headers = headers)
  return resp.body

def acquire_baidu_baike_summary_by_html(html):
  beg_time = int(time.time())
  value = ""
  tree = etree.HTML(html)
  nodes = tree.xpath(u'//div[@class="card-summary-content"]/div[@class="para"]//text()')
  for node in nodes:
    value = "".join([value, node])
  end_time = int(time.time())
  print "parse_time:", end_time - beg_time 
  return value

def acquire_baidu_baike_summary_by_url(url):
  html = fetch_url(url)
  return acquire_baidu_baike_summary_by_html(html)

def acquire_baidu_baike_summary_by_keyword(keyword):
  beg_time = int(time.time())
  html = fetch_baidu_baike_by_keyword(keyword)
  end_time = int(time.time())
  print "fetch_time:", end_time - beg_time 
  return acquire_baidu_baike_summary_by_html(html)

def main(argv):
  keyword = sys.argv[1]
  socket.setdefaulttimeout(1)

  summary = acquire_baidu_baike_summary_by_keyword(keyword)
  print summary

if __name__ == '__main__':
  main(sys.argv)
