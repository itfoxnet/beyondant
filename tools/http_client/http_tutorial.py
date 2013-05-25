#!/usr/bin/python
'''
  show usages of urllib, urllib2, httplib
'''
import base64
import httplib
import httplib2
import socket
import sys
import urllib
import urllib2

__author__ = 'cuberub@gmail.com'

'''
  urllib2.Request()
  urllib2.urlopen(request)
  file_like_object.read()
'''
def fetch_url_open_response(url):
  timeout = 1
  data_dict = {"x_pos":"1"}
  data = urllib.urlencode(data_dict)
  headers = {}
  headers["User-Agent"] = 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
  try :
    request = urllib2.Request(url, data=data, headers=headers)
    response = urllib2.urlopen(request, timeout=timeout)
    content = response.read()
    res_url = response.geturl()
    res_code = response.getcode()
    res_headers = dict(response.info().items())
    print "res_url:", res_url
    print "res_code:", res_code
    print "res_headers:", res_headers
    print "content:", content
  except socket.timeout:
    print "socket timeout"
  except urllib2.HTTPError, e:
    print "HTTP Error code: ", e.code
  except urllib2.URLError, e:
    print "URL Error: ", e.reason

'''
  urllib2.urlopen(url)
  file_like_object.read()
'''
def fetch_url_open_url(url):
  timeout = 1
  data_dict = {"x_pos":"1"}
  data = urllib.urlencode(data_dict)
  try :
    response = urllib2.urlopen(url, data=data, timeout=timeout)
    content = response.read()
    res_url = response.geturl()
    res_code = response.getcode()
    res_headers = dict(response.info().items())
    print "res_url:", res_url
    print "res_code:", res_code
    print "res_headers:", res_headers
    print "content:", content
  except socket.timeout:
    print "socket timeout"
  except urllib2.HTTPError, e:
    print "HTTP Error code: ", e.code
  except urllib2.URLError, e:
    print "URL Error: ", e.reason

'''
  fetch http server with HTTPConnection
  httplib.HTTPConnection
  HTTPConnection.request()
  HTTPConnection.getresponse()
  Response.read()
'''
def fetch_url_with_httpconnection(server, port, path):
  method = "GET"
  data = ""
  headers = {}
  conn = httplib.HTTPConnection(server, port)
  conn.request(method, path, data, headers)
  response = conn.getresponse()
  print "status:", response.status
  print "reason:", response.reason
  print "headers:", response.getheaders()
  print "body:", response.read()
  conn.close()

'''
  fetch http server with authorization
  httplib.HTTPConnection
  HTTPConnection.request()
  HTTPConnection.getresponse()
  Response.read()
'''
def fetch_url_with_authorization(server, port, path, username, password):
  method = "GET"
  credentials = base64.b64encode("%s:%s" % (username, password))
  headers = {"Content-Type":"application/json", "Authorization":"Basic "+credentials}
  conn = httplib.HTTPConnection(server, port)
  conn.request(method, path, "", headers)
  response = conn.getresponse()
  print response.read()

def fetch_url_with_auth_handler(url, realm, auth_uri, username, password):
# Create an OpenerDirector with support for Basic HTTP Authentication...
  auth_handler = urllib2.HTTPBasicAuthHandler()
  auth_handler.add_password(realm=realm,
                            uri=auth_uri,
                            user=username,
                            passwd=password)
  opener = urllib2.build_opener(auth_handler)
  # ...and install it globally so it can be used with urlopen.
  urllib2.install_opener(opener)
  response = urllib2.urlopen(url)
  print response.read()

# support chunked format
# httplib2 might not included in old python versions
# you should install it first
def fetch_url_with_httplib2(url):
  http = httplib2.Http()
  body = urllib.urlencode({})
  headers = {}
  response, content = http.request(url, 'POST', headers=headers, body=body)
  print "response_header:", response
  print "response_body:", content

if __name__ == '__main__':
  #fetch_url_open_request(sys.argv[1])

  #fetch_url_open_url(sys.argv[1])
  
  #server = "www.baidu.com"
  #port = 80
  #path = "/"
  #fetch_url_with_httpconnection(server, port, path)

  #server = "www.google.com"
  #port = 80
  #path = "/"
  #username = "hello"
  #password = "world"
  #fetch_url_with_authorization(server, port, path, username, password)

  #realm = 'Management'
  #auth_uri='http://server:port'
  #username = "user"
  #password = "pwd"
  #path = "/"
  #url = auth_uri + path
  #fetch_url_with_auth_handler(url, realm, auth_uri, username, password)

  #url = "http://t.pp.cc/"
  #fetch_url_with_httplib2(url)
