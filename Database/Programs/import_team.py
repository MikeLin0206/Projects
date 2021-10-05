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

    name = soup.find_all('h3')
    index = 7
    for i in name:
        cur.execute("insert into class(CID,Name,nLevel) values({},'{}',2);".format(index,i.string))
        index += 1
    cur.close
    conn.close

def main():
    sql()

main()
