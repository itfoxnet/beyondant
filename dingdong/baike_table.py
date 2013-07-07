#!/usr/bin/python
# -*- coding:utf-8 -*-
# Copyright 2013 Beyondant. All Right Reserved.
# Date: 2013-07-06

__author__ = 'cuberub@gmail.com'
import sqlite3
import db_config

baike_table_name = "baike_catalog"
class BaikeTable :
  def __init__(self) :
    self.db_path = db_config.db_path
    self.table_name = baike_table_name

  def create(self):
    db = sqlite3.connect(self.db_path)
    c = db.cursor()
    c.execute("create table " + self.table_name + "(\
                  keyword varchar(64) unique,\
                  content varchar(4096))")
    db.commit()
    
  def update(self, keyword, content):
    db = sqlite3.connect(self.db_path)
    c = db.cursor()
    insert_sql = "insert into " + self.table_name + " values('%s', '%s')" % (keyword, content)
    c.execute(insert_sql)
    db.commit()

  def select(self, keyword):
    db = sqlite3.connect(self.db_path)
    c = db.cursor()
    select_sql = "select content from " + self.table_name + " where keyword = '%s'" % keyword
    c.execute(select_sql)
    result = c.fetchone()
    if result:
      return result[0]
    else:
      return ""

if __name__ == '__main__':
  table = BaikeTable()
  table.create()
