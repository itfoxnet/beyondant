#!/usr/bin/python
# Copyright 2013 Beyondant. All Right Reserved.
# http fetcher
# support IP binding
# Date: 2013-05-10

__author__ = 'cuberub@gmail.com'

import os
import urllib2
import socket
import httplib

class BindableHTTPConnection(httplib.HTTPConnection):
  def connect(self):
    """Connect to the host and port specified in __init__."""
    self.sock = socket.socket()
    self.sock.bind((self.source_ip, 0))
    if isinstance(self.timeout, float):
      self.sock.settimeout(self.timeout)
    self.sock.connect((self.host,self.port))

def BindableHTTPConnectionFactory(source_ip):
  def _get(host, port=None, strict=None, timeout=0):
    bhc = BindableHTTPConnection(host, port=port, strict=strict, timeout=timeout)
    bhc.source_ip=source_ip
    return bhc
  return _get

class BindableHTTPHandler(urllib2.HTTPHandler):
  def __init__(self, bind_ip=None, debuglevel=0) :
    urllib2.HTTPHandler.__init__(self, debuglevel)
    self.bind_ip = bind_ip
    
  def http_open(self, req):
    if self.bind_ip == None or self.bind_ip == "":
            return urllib2.HTTPHandler.http_open(self, req)
    return self.do_open(BindableHTTPConnectionFactory(self.bind_ip), req)

class HTTPResponse(object):
  headers = None
  status = None
  body = None
  final_url = None

  def __init__(self, final_url=None, status=None, headers=None, body=None):
    self.final_url = final_url
    self.status = status
    self.headers = headers
    self.body = body

  def __repr__(self):
    return ("[HTTP Status Code: %r --- Request URL: %s --- Response: %s" %
            (self.status, self.final_url, self.body))


class UrlFetcher(object):
  def fetch(self, url, body=None, headers=None):
    if headers is None:
      headers = {}
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
    finally:
      f.close()
    return resp

  def _makeResponse(self, urllib2_response):
    resp = HTTPResponse()
    try:
      resp.body = urllib2_response.read()
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

class BindableUrlFetcher(object):
  def __init__(self, bind_ip= None) :
    self.bind_ip = bind_ip
  def fetch(self, url, body=None, headers=None):
    if headers is None:
      headers = {}
    req = urllib2.Request(url, data=body, headers=headers)

    handler1 = urllib2.HTTPRedirectHandler()
    handler2 = urllib2.HTTPCookieProcessor()
    handler3 = BindableHTTPHandler(self.bind_ip)
    opener = urllib2.build_opener(handler1, handler2, handler3)
    urllib2.install_opener(opener)
    resp = HTTPResponse()
    try:
      url_info = opener.open(req)
      try:
        resp = self._makeResponse(url_info)
      finally:
        url_info.close()
    except urllib2.HTTPError, e:
      print e
      resp.status = e.code
    except BaseException, e:
      print e
      resp.status = -1
    return resp

  def _makeResponse(self, url_info):
    resp = HTTPResponse()
    try:
      resp.body = url_info.read()
    except socket.timeout:
      resp.status = -1
      return resp

    resp.final_url = url_info.geturl()
    resp.headers = dict(url_info.info().items())

    if hasattr(url_info, 'code'):
      resp.status = url_info.code
    else:
      resp.status = 200
    return resp
