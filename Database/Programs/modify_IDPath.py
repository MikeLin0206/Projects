#!/usr/local/bin/python
import pymysql

def sql():
    conn = pymysql.connect(host = 'localhost',user = 'root',passwd = '123'
                           ,db = 'baseball',autocommit=True)
    cur = conn.cursor()
    for i in range(0,7):
        cur.execute("update class set IDPath = {} where CID = {}".format(i,i))

    ALE = [8,9,15,18,20]
    ALC = [10,11,12,13,14]
    ALW = [27,16,17,19,7]
    NLE = [22,26,31,32,30]
    NLC = [23,24,29,33,34]
    NLW = [21,25,28,35,36]
    for k in range(0,5):
         cur.execute("update class set IDPath = '1/{}' where CID = {}".format(ALE[k],ALE[k]))
         cur.execute("update class set IDPath = '2/{}' where CID = {}".format(ALC[k],ALC[k]))
         cur.execute("update class set IDPath = '3/{}' where CID = {}".format(ALW[k],ALW[k]))
         cur.execute("update class set IDPath = '4/{}' where CID = {}".format(NLE[k],NLE[k]))
         cur.execute("update class set IDPath = '5/{}' where CID = {}".format(NLC[k],NLC[k]))
         cur.execute("update class set IDPath = '6/{}' where CID = {}".format(NLW[k],NLW[k]))

    cur.close()
    conn.close()

sql()


