#!/usr/local/bin/python
import pymysql
import urllib.request
import sys
from bs4 import BeautifulSoup

def sql():
    for i in range(1,31):
        quote_page = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=8&season={}&month=0&season1={}&ind=0&team={}&rost=0&age=0&filter=&players=0&page=1_50'.format(sys.argv[1],sys.argv[1],i)
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
        pid = column[0]
        if pid == None:
            pid = 0
        ipid = pid + 1

        c = 0
        P_rec1 = ['W','L','SV','G','GS','IP','BB9','HR9','BABIP','LOB','GB','HRFB','FIP','xFIP']
        P_rec2 = ['K9','ERA','WAR']
        for j in name:
            if(index % 16) != 0 :
                if ord(j.string[0]) > 60 :
                    if len(j.string.split("'")) == 2:
                            s_name = j.string.split("'")[1]
                            j.string = j.string.split("'")[0] + s_name
                    cur.execute("select CID from class where Name = '{}'".format(j.string))
                    repeat = cur.fetchone()
                    if repeat == None:
                        ctrl = 1
                        cur.execute('insert into class(CID,Name,nLevel) values({},"{}",3)'.format(cid,j.string))
                        cur.execute("insert into inheritance(PCID,CCID) values({},{})".format(i+6,cid))
                        cur.execute("select IDPath from class where CID = {}".format(i+6))
                        T_IDPath = cur.fetchone()[0]
                        cur.execute("update class set IDPath = '{}/{}' ,describes = 'Pitcher' where CID = {}".format(T_IDPath,cid,cid))
                        cid += 1
                    else :
                        repeat = repeat[0]
                        cur.execute("update CO set CID = {} where OID = {}".format(repeat,pid))
                else :
                    if c == 9 or c == 10 or c == 11 :
                        cur.execute("update P_record set {} = '{}' where PID = {};".format(P_rec1[c],j.string,pid))
                    else:
                        cur.execute("update P_record set {} = {} where PID = {};".format(P_rec1[c],j.string,pid))
                    c += 1
            else :
                pid += 1
                cur.execute("insert into P_record(PID) values({})".format(pid))
                cur.execute("insert into object(OID,Since,Type) values({},{},{})".format(pid,2018,2))
                cur.execute("insert into CO(CID,OID) values({},{})".format(cid,pid))
                cur.execute("select describes from class where CID = {}".format(i+6))
                column = cur.fetchone()
                team = column[0]
                cur.execute("update P_record set Team = '{}' where PID = {};".format(team,pid))
                c = 0
            index += 1

        c = 0
        for k in state:
            cur.execute("update P_record set {} = {} where PID = {}".format(P_rec2[c],k.string,ipid))
            c += 1
            if c == 3:
               c = 0
               ipid += 1

        cur.close()
        conn.close()

sql()










