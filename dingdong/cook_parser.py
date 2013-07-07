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

def acquire_detail_url(keyword, html):
  value = ""
  tree = etree.HTML(html)
  nodes = tree.xpath(u'//a[@class="search-target a"]')
  for node in nodes:
    anchor = str(node.text.encode("utf8"))
    if cmp(anchor, keyword) == 0 :
      return node.get("href")
  if len(nodes) > 0:
    return nodes[0].get("href")
  return ""

def fetch_cook_by_keyword(keyword):
  url = "http://www.haodou.com/search/recipe/" + keyword
  srp_html = http_util.fetch_url(url)
  detail_url = acquire_detail_url(keyword, srp_html)
  detail_html = http_util.fetch_url(detail_url)
  return detail_html

def acquire_cook_summary_by_html(html):
  value = ""
  tree = etree.HTML(html)

  material = ""
  nodes = tree.xpath(u'//div[@class="material"]//text()')
  for node in nodes:
    data = "" + node
    data = data.encode("utf8").strip()
    if len(data) > 0 :
      material = " ".join([material, data])

  steps = ""
  nodes = tree.xpath(u'//dl[@class="step"]//text()')
  for node in nodes:
    data = "" + node
    data = data.encode("utf8").strip()
    if len(data) > 0 :
      steps = "\n".join([steps, data])

  if (len(material) == 0 and len(steps) == 0) :
    return ""
  value = material + "\n" + steps
  return value 

def acquire_cook_summary_by_url(url):
  html = http_util.fetch_url(url)
  return acquire_cook_summary_by_html(html)

def acquire_cook_summary_by_keyword(keyword):
  beg_time = int(time.time())
  html = fetch_cook_by_keyword(keyword)
  end_time = int(time.time())
  print "fetch_time:", end_time - beg_time 
  return acquire_cook_summary_by_html(html)

def main(argv):
  keyword = sys.argv[1]
  summary = acquire_cook_summary_by_keyword(keyword)
  print summary

if __name__ == '__main__':
  main(sys.argv)
