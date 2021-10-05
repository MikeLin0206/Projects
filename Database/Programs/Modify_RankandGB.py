#!/usr/local/bin/python
import pymysql

def sql():
    conn = pymysql.connect(host = 'localhost',user = 'root',passwd = '123'
                           ,db = 'baseball',autocommit=True)
    cur = conn.cursor()
    path = "class p,class c,inheritance i,CO,object o,record r where p.cid = i.pcid and i.ccid = c.cid and c.cid = CO.cid and CO.oid = o.oid and o.oid = r.rid"
    for i in range(1,7):
        cur.execute("select r.rid,r.Win from {} and p.cid = {} order by r.Win desc".format(path,i))
        re = cur.fetchall()
        for j in range(1,6):
            cur.execute("update record set Rank = {} where Rid = {}".format(j,re[j-1][0]))

    for i in range(1,7):
        cur.execute("select r.rid,r.rank,r.Win from {} and p.cid = {} order by r.rank".format(path,i))
        gb = cur.fetchall()
        for j in range(0,5):
            if gb[j][1] == 1:
                cur.execute("update record set GB = {} where rid = {}".format(0,gb[j][0]))
            else :
                cur.execute("update record set GB = {} where rid = {}".format((gb[0][2] - gb[j][2])/2,gb[j][0]))
            print(gb[j][1])

    cur.close()
    conn.close()

sql()


