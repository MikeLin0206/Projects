#!/usr/local/bin/python
import pymysql
import urllib.request
import sys
from bs4 import BeautifulSoup

def sql():
    for i in range(1,31):
        quote_page = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=c,4,6,11,13,21,-1,34,35,40,41,-1,23,37,38,50,61,-1,203,199,58&season={}&month=0&season1={}&ind=0&team={}&rost=0&age=0&filter=&players=0&page=1_80'.format(sys.argv[1],sys.argv[1],i)
        print(i)
        conn = pymysql.connect(host = 'localhost',user = 'root',passwd = '123',db = 'baseball',autocommit=True)
        cur = conn.cursor()
        page = urllib.request.urlopen(quote_page)
        soup = BeautifulSoup(page, 'html.parser')

        name = soup.find_all('td','grid_line_regular')
        state = soup.find_all('td','grid_line_break')

        index = 0;
        cur.execute("SELECT MAX(CID) FROM class")
        column = cur.fetchone()
        cid = column[0] + 1

        cur.execute("SELECT MAX(OID) FROM object")
        column = cur.fetchone()
        hid = column[0]
        if hid == None:
            hid = 0
        ihid = hid + 1

        c = 0
        H_rec1 = ['Game','PA','HR','RBI','SB','K_P','ISO','BABIP','OBP','SLG','wOBA','wRC','Def','WAR']
        H_rec2 = ['BB_P','AVG','off']
        for j in name:
            if(index % 16) != 0 :
                if ord(j.string[0]) > 60 :
                    if len(j.string.split("'")) == 2:
                            s_name = j.string.split("'")[1]
                            j.string = j.string.split("'")[0] + s_name
                    cur.execute("select CID from class where Name = '{}'".format(j.string))
                    repeat = cur.fetchone()
                    if repeat == None:
                        cur.execute('insert into class(CID,Name,nLevel) values({},"{}",3)'.format(cid,j.string))
                        cur.execute("insert into inheritance(PCID,CCID) values({},{})".format(i+6,cid))
                        cur.execute("select IDPath from class where CID = {}".format(i+6))
                        T_IDPath = cur.fetchone()[0]
                        cur.execute("update class set IDPath = '{}/{}' ,describes = 'Batter' where CID = {}".format(T_IDPath,cid,cid))
                        cid += 1
                    else :
                        repeat = repeat[0]
                        cur.execute("update CO set CID = {} where OID = {}".format(repeat,hid))
                else :
                    if c == 5 :
                        cur.execute("update H_record set {} = '{}' where HID = {};".format(H_rec1[c],j.string,hid))
                    else:
                        cur.execute("update H_record set {} = {} where HID = {};".format(H_rec1[c],j.string,hid))
                    c += 1
            else :
                hid += 1
                cur.execute("insert into H_record(HID) values({})".format(hid))
                cur.execute("insert into object(OID,Since,Type) values({},{},{})".format(hid,sys.argv[1],1))
                cur.execute("insert into CO(CID,OID) values({},{})".format(cid,hid))
                cur.execute("select describes from class where CID = {}".format(i+6))
                column = cur.fetchone()
                team = column[0]
                cur.execute("update H_record set Team = '{}' where HID = {};".format(team,hid))
                c = 0
            index += 1

        c = 0
        for k in state:
            if c == 0:
                cur.execute("update H_record set {} = '{}' where HID = {}".format(H_rec2[c],k.string,ihid))
            else :
                cur.execute("update H_record set {} = {} where HID = {}".format(H_rec2[c],k.string,ihid)) 
            c += 1
            if c == 3:
               c = 0
               ihid += 1

        cur.close()
        conn.close()

sql()










