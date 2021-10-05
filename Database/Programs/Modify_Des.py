#!/usr/local/bin/python
import pymysql

def sql():
    conn = pymysql.connect(host = 'localhost',user = 'root',passwd = '123'
                           ,db = 'baseball',autocommit=True)
    cur = conn.cursor()
    des = ['LAA','BAL','BOS','CWS','CLE','DET','KC','MIN','NYY','OAK','SEA',
           'TB','TEX','TOR','ARI','ATL','CHC','CIN','COL','MIA','HOU','LAD'
           ,'MIL','WAS','NYM','PHI','PIT','STL','SD','SF']
    j = 7
    for i in des:
        cur.execute("update class set describes = '{}' where CID = {}".format(i,j))
        j += 1

    for i in range(0,7):
        cur.execute("update class set describes = 'Division' where CID = {}".format(i))

    cur.close()
    conn.close()

sql()


