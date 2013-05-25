#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Jike Inc. All Rights Reserved.

# HTTP POST utility, you can achieve the same function with curl
# input file format
# header_file line format:
# key:val
# key:val

# data_file line format:
# key:val
# key:val

# depend: apt-get install python-gflags

__author__ = 'cuberub@gmail.com'

import sys
import urllib2
import urllib
import time
import socket
import gflags

gflags.DEFINE_string('url', None, 'url to fetch')
gflags.DEFINE_string('header_file', None, 'header file')
gflags.DEFINE_string('data_file', None, 'post data file')

class HTTPResponse(object):
  headers = None
  status = None
  data = None
  final_url = None

  def __init__(self, final_url=None, status=None, headers=None, data=None):
    self.final_url = final_url
    self.status = status
    self.headers = headers
    self.data = data

  def __repr__(self):
    return ("[HTTP Status Code: %r --- Request URL: %s --- Response: %s" %
            (self.status, self.final_url, self.data))

class HeadersBuilder(object):
  headers = {}

  def clear(self) :
    self.headers.clear()

  def makeDefaultHeaders(self) :
    self.clear()
    self.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
    self.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    self.headers['Accept-Language'] = 'zh-cn,en-us;q=0.7,en;q=0.3'
    self.headers['Accept-Charset'] = 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
    self.headers['Referer'] = ''
    return self.headers

  def makeHeaders(self, headers_str) :
    self.clear()
    lines = headers_str.split('\n')
    for line in lines :
      line = line.strip()
      pos = line.find(':')
      if pos == -1 :
        continue
      key = line[0:pos].strip()
      val = line[pos+1:].strip()
      self.headers[key] = val
    return self.headers

  def makeHeadersFromFile(self, headers_file) :
    f = open(headers_file, 'r')
    headers_str = f.read()
    f.close()
    return self.makeHeaders(headers_str)

  def getHeaders(self) :
    return self.headers

  '''def AddHeader(self, header_str) 
     def AddHeader(self, key, val) '''

class PostDataBuilder(object):
  data = ""
  def clear(self) :
    self.data = ""

  def makePostData(self, data_str) :
    self.clear()
    lines = data_str.split('\n')
    data_dict = {}
    for line in lines :
      line = line.strip()
      pos = line.find(':')
      if pos == -1 :
        continue
      key = line[0:pos]
      val = line[pos+1:]
      data_dict[key] = val
    self.data = urllib.urlencode(data_dict)
    return self.data

  def makePostDataFromFile(self, data_file) :
    f = open(data_file, 'r')
    data_str = f.read()
    f.close()
    return self.makePostData(data_str)

  def getPostData(self) :
    return self.data

class UrlFetcher(object):
  def fetch(self, url, body=None, headers=None):
    if headers is None:
      headers = {}
    print "Request headers:"
    print headers
    print "POST data:"
    print body
    req = urllib2.Request(url, data=body, headers=headers)
    resp = HTTPResponse()
    try:
      f = urllib2.urlopen(req)
      resp = self._makeResponse(f)
    except urllib2.HTTPError, e:
      print e
      resp.status = e.code
    except BaseException, e:
      print e
      resp.status = -1
    return resp

  def _makeResponse(self, urllib2_response):
    resp = HTTPResponse()
    try:
      resp.data = urllib2_response.read()
    except socket.timeout:
      resp.status = -1
      return resp

    resp.final_url = urllib2_response.geturl()
    resp.headers = dict(urllib2_response.info().items())

    if hasattr(urllib2_response, 'code'):
      resp.status = urllib2_response.code
    else:
      resp.status = 200
    return resp

def main(argv):
  socket.setdefaulttimeout(30)
  try :
    argv = gflags.FLAGS(argv)
  except gflags.FlagsError, e :
    print "Exception: %s" % e
    sys.exit(1)
  if gflags.FLAGS.url is None :
    print "url not set!"
    sys.exit(1)

  url = gflags.FLAGS.url
  headers = {}
  body = None
  headers_builder = HeadersBuilder()
  data_builder = PostDataBuilder()
  if gflags.FLAGS.header_file is not None :
    headers = headers_builder.makeHeadersFromFile(gflags.FLAGS.header_file)
  else :
    headers = headers_builder.makeDefaultHeaders()
  if gflags.FLAGS.data_file is not None :
    body = data_builder.makePostDataFromFile(gflags.FLAGS.data_file)
  fetcher = UrlFetcher()
  resp = fetcher.fetch(url = url, body = body, headers = headers)
  if resp.status != 200:
    return
  print "Response Headers:"
  print resp.headers
  print "Response Data:"
  print resp.data

if __name__ == '__main__':
  main(sys.argv)
