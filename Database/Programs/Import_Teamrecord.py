#!/usr/local/bin/python
import pymysql
import urllib.request
from bs4 import BeautifulSoup

def sql():
    conn = pymysql.connect(host = 'localhost',user = 'root',passwd = '123'
                           ,db = 'baseball',autocommit=True)
    cur = conn.cursor()
    quote_page = 'https://www.fangraphs.com/depthcharts.aspx?position=Standings'

    page = urllib.request.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    
    cur.execute("select max(OID) from object")
    oid = cur.fetchone()[0]

    name = soup.find_all('td')
    c = 0
    s = 0
    index = 0
    t_rec = ['Win','Lose','W_P']
    for i in name:
       if c == 643:
           break
       if c > 12 :
           if s % 21 == 0:
               oid += 1
               cur.execute("select CID from class where Name like '%{}'".format(i.string))
               cid = cur.fetchone()[0]
               print(cid)
               cur.execute("insert into CO(CID,OID) values({},{})".format(cid,oid))
               cur.execute("insert into object(OID,Since,Type) values({},2018,3)".format(oid))
               cur.execute("insert into record(RID) values({})".format(oid))
           elif s % 21 == 2 or s % 21 == 3 or s % 21 == 4 :
               cur.execute("update record set {} = {} where RID = {}".format(t_rec[index],i.string,oid))
               index += 1
               if index == 3:
                   index = 0
           s +=1
       c += 1


    cur.close()
    conn.close()

def main():
    sql()

main()
