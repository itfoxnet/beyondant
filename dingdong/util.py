#!/usr/bin/python
# -*- coding:utf-8 -*-
# Copyright 2013 Beyondant. All Right Reserved.
# Date: 2013-07-10
import chardet

__author__ = 'cuberub@gmail.com'

def utf8_to_gbk(s):
  return unicode(s, 'utf8', 'ignore').encode('gbk', 'ignore')

def coding_to_utf8(s):
  curr_coding = chardet.detect(s)["encoding"]
  if curr_coding != "utf-8":
    return s.decode(curr_coding, 'ignore').encode('utf-8')
  return s
