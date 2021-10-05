#!/usr/local/bin/python
import pymysql
import urllib.request
from bs4 import BeautifulSoup


def sql():
    conn = pymysql.connect(host = 'localhost',user = 'root',passwd = '123'
                           ,db = 'baseball',autocommit=True)
    cur = conn.cursor()
    quote_page = 'http://m.mlb.com/teams/'

    page = urllib.request.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    cur.execute("select IDPath from class where CID > 6")
    column = cur.fetchall()
    for i in range(0,30):
        b = column[i][0].split('/')
        cur.execute("insert into inheritance(PCID,CCID) values({},{})".format(b[0],b[1]))

    cur.close()
    conn.close()

sql()


