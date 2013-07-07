#!/usr/bin/python
# -*- coding:utf-8 -*-
# Copyright 2013 Beyondant. All Right Reserved.
# Date: 2013-07-06

__author__ = 'cuberub@gmail.com'
import cgi
import os
import socket
import sys
import time
from xml.dom import minidom

sys.path.append('/srv/www/dingdong.com/application')
import baike_parser
import baike_table
import cook_parser
import cook_table

os.environ['PYTHON_EGG_CACHE'] = '/srv/www/dingdong.com/.python-egg'

def validate(environ, start_response):
    status = '200 OK'
    query_string = environ['QUERY_STRING']
    output = query_string.split("&")[1].split("=")[1]
    response_headers = [('Content-Type', 'text/plain'),
                    ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]

def is_cook_request(content) :
  if (content.startswith("cp ")
      or content.startswith("CP ")
      or content.find("caipu") != -1
      or content.find("菜谱") != -1) :
    return True
  else :
    return False

def is_baike_request(content) :
  return True

def rewrite_cook_request(content) :
  return content.replace("caipu", "").replace("菜谱", "").replace("cp", "").replace("CP", "").replace(":", "").replace(" ", "")

def random_echo():
  ans = "Tomorrow will be better"
  return ans

def make_response(request):
  dom = minidom.parseString(request)
  from_user_name = ""
  to_user_name = ""
  content = ""
  msg_type = ""
  msg_id = ""
  for node in dom.getElementsByTagName("FromUserName"):
    from_user_name = str(node.firstChild.data)
  for node in dom.getElementsByTagName("ToUserName"):
    to_user_name = str(node.firstChild.data)
  for node in dom.getElementsByTagName("Content"):
    content = str(node.firstChild.data.encode('utf8'))
  for node in dom.getElementsByTagName("MsgType"):
    msg_type = str(node.firstChild.data)
  for node in dom.getElementsByTagName("MsgId"):
    msg_id = str(node.firstChild.data)
  cur_time = int(time.time())

  ans = ""
  if is_cook_request(content):
    content = rewrite_cook_request(content)
    table = cook_table.CookTable()
    ans = table.select(content)
    if ans == "" :
      ans = cook_parser.acquire_cook_summary_by_keyword(content)
      if ans != "" and len(ans) > 0 :
        table.update(content, ans)
    else :
      ans = str(ans.encode("utf8"))
  elif is_baike_request(content) :
    table = baike_table.BaikeTable()
    ans = table.select(content)
    if ans == "" :
      ans = baike_parser.acquire_baidu_baike_summary_by_keyword(content)
      if ans != "" and len(ans) > 0 :
        ans = str(ans.encode("utf8"))
        table.update(content, ans)
    else :
      ans = str(ans.encode("utf8"))

  if ans == "" :
    ans = random_echo()
    ans = str(ans.encode("utf8"))

  xml_str = """<xml>\
   <ToUserName><![CDATA[%s]]></ToUserName>\
   <FromUserName><![CDATA[%s]]></FromUserName>\
   <CreateTime>%s</CreateTime>\
   <MsgType><![CDATA[text]]></MsgType>\
   <Content><![CDATA[%s]]></Content>\
   <FuncFlag>0</FuncFlag>\
</xml>""" % (from_user_name, to_user_name, cur_time, ans)
  return xml_str

def application(environ, start_response):
    print environ
    if environ['REQUEST_METHOD'] == 'GET' :
        return validate(environ, start_response)
    status = '200 OK'

    body= ''  # b'' for consistency on Python 3.0
    try:
        length = int(environ.get('HTTP_CONTENT_LENGTH', '0'))
    except ValueError:
        length= 0
    if length != 0:
        body = environ['wsgi.input'].read(length)
    print body
    response = make_response(body)
    print response

    response_headers = [('Content-type', 'text/html'),
                    ('Content-length', str(len(response)))]
    start_response(status, response_headers)
    return [response,]
