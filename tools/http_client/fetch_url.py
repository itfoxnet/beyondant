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

import http_util

url = sys.argv[1]
def main(argv):
  socket.setdefaulttimeout(30)

  headers = {}
  headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
  headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
  headers['Accept-Language'] = 'zh-cn,en-us;q=0.7,en;q=0.3'
  headers['Accept-Charset'] = 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
  headers['Referer'] = ''

  fetcher = http_util.UrlFetcher()
  resp = fetcher.fetch(url, headers = headers)
  print resp

if __name__ == '__main__':
  main(sys.argv)
