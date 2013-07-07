#!/usr/bin/python
# Copyright 2013 Beyondant. All Right Reserved.
# Date: 2013-07-06

__author__ = 'cuberub@gmail.com'
import sqlite3

db_path = "/tmp/baike.db"

def create_db():
  db = sqlite3.connect(db_path)
  c = db.cursor()
  c.execute("""create table catalog (
                keyword varchar(64) unique,
                content varchar(4096))""")
  db.commit()
  
def update_db(keyword, content):
  db = sqlite3.connect(db_path)
  c = db.cursor()
  insert_sql = "insert into catalog values('%s', '%s')" % (keyword, content)
  c.execute(insert_sql)
  db.commit()

def select_db(keyword):
  db = sqlite3.connect(db_path)
  c = db.cursor()
  select_sql = "select content from catalog where keyword = '%s'" % keyword
  c.execute(select_sql)
  result = c.fetchone()
  if result:
    return result[0]
  else:
    return ""

if __name__ == '__main__':
  create_db()
