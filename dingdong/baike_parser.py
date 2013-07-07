#!/usr/bin/python
# -*- coding:utf-8 -*-
# Copyright 2013 Beyondant. All Right Reserved.
# Date: 2013-05-10

__author__ = 'cuberub@gmail.com'

import sys
import datetime
import random
import socket
import time
import urllib
from lxml import etree
import http_util
import util

def fetch_baidu_baike_by_keyword(keyword):
  url = "http://baike.baidu.com/search/word?pic=1&sug=1&enc=utf8&word=" + keyword
  return http_util.fetch_url(url)

def acquire_baidu_baike_summary_by_html(html):
  value = ""
  tree = etree.HTML(html)
  nodes = tree.xpath(u'//div[@class="card-summary-content"]/div[@class="para"]//text()')
  for node in nodes:
    value = "".join([value, node])
  return value

def acquire_baidu_baike_summary_by_url(url):
  html = http_util.fetch_url(url)
  return acquire_baidu_baike_summary_by_html(html)

def acquire_baidu_baike_summary_by_keyword(keyword):
  beg_time = int(time.time())
  html = fetch_baidu_baike_by_keyword(keyword)
  end_time = int(time.time())
  print "fetch_time:", end_time - beg_time 
  return acquire_baidu_baike_summary_by_html(html)

def main(argv):
  keyword = sys.argv[1]
  summary = acquire_baidu_baike_summary_by_keyword(keyword)
  print summary

if __name__ == '__main__':
  main(sys.argv)
