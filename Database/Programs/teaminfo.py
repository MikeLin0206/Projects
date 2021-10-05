#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import pymysql

cgitb.enable()
def sql():
    conn = pymysql.connect(host = 'localhost',user = 'root',passwd = '123' ,db = 'baseball',autocommit=True)
    cur = conn.cursor()
    cur.execute("select Name from class where CID > 6 and CID < 37")
    team = cur.fetchall()
    teams = []
    for i in range(0,30):
        teams.append(team[i][0])
    return teams

def getrecord(team):
    conn = pymysql.connect(host = 'localhost',user = 'root',passwd = '123' ,db = 'baseball',autocommit=True)
    cur = conn.cursor()
    cur.execute("select p.cid from class c,class p,inheritance i where c.cid = i.ccid and i.pcid = p.cid"
                " and c.Name = '{}'".format(team))
    division = cur.fetchone()[0];
    cur.execute("select r.rank,c.name,r.win,r.lose,r.gb from class c,class p,inheritance i,CO,object o,record r "
                "where p.cid = i.pcid and i.ccid = c.cid and c.cid = CO.cid and CO.oid = o.oid and o.oid = r.rid "
                "and p.cid = {} order by r.rank".format(division))
    data = cur.fetchall();
    table = [[],[],[],[],[]]

    for i in range(0,5):
        for j in range(0,5):
            table[i].append(data[i][j])
    return table

def gethitleader(team):
    conn = pymysql.connect(host = 'localhost',user = 'root',passwd = '123' ,db = 'baseball',autocommit=True)
    cur = conn.cursor()
    cur.execute("select c.Name,h.* from class p,class c,inheritance i,CO,object o,H_record h where "
                "p.cid = i.pcid and i.ccid = c.cid and c.cid = CO.cid and CO.oid = o.oid and o.oid = h.hid "
                " and p.Name = '{}' and h.team = p.describes order by h.war desc".format(team))
    data = cur.fetchall();
    table = [[],[],[],[],[]]
    for i in range(0,5):
         for j in range(0,20):
              if j != 1 and j != 2:
                  table[i].append(data[i][j])
    return table;

def getpitchleader(team):
    conn = pymysql.connect(host = 'localhost',user = 'root',passwd = '123' ,db = 'baseball',autocommit=True)
    cur = conn.cursor()
    cur.execute("select c.Name,pc.* from class p,class c,inheritance i,CO,object o,P_record pc where "
                "p.cid = i.pcid and i.ccid = c.cid and c.cid = CO.cid and CO.oid = o.oid and o.oid = pc.pid "
                " and p.Name = '{}' and pc.team = p.describes order by pc.war desc".format(team))
    data = cur.fetchall();
    table = [[],[],[],[],[]]
    for i in range(0,5):
         for j in range(0,20):
              if j != 1 and j != 2:
                  table[i].append(data[i][j])
    return table;


def getvalue():
    form = cgi.FieldStorage()
    Team_value = 0
    if form.getvalue('TeamName'):
       Team_value = form.getvalue('TeamName')
    else:
       Team_value = "no"
    return Team_value

def main():
    print("Content-type:text/html")
    print()
    print("<html>")
    print("<head>")
    print("<style type = 'text/css'>")
    print("a.linkpos1{position:absolute; right:20px; top:30px;}")
    print("a.linkpos2{position:absolute; right:160px;top:30px;}")
    print("</style> </head>")
    print("<body>")
    print("<a href = 'main.py' style='text-decoration: none; color:#444; font-size:50px;'>PLAYBALL!</a>")
    print("<a href = 'player.py' style='text-decoration: none;  color:#444; font-size:30px;' class ='linkpos1'>PLAYER</a>")
    print("<a href = 'team.py' style='text-decoration: none;  color:#444; font-size:30px;' class ='linkpos2'>TEAM</a>")

    input_team = getvalue()
    print("<h3 style='font-size:50px;LINE-HEIGHT:200px' align='center'>{}</h3>".format(input_team))

    print("<table border='1'>")
    print("<tr>"
          "<td>Rank</td>"
          "<td>Team</td>"
          "<td>W</td>"
          "<td>L</td>"
          "<td>GB</td>"
          "</tr>")
    record_tab = getrecord(input_team)
    for i in range(0,5):
        print("<tr>")
        for j in range(0,5):
            print("<td>{}</td>".format(record_tab[i][j]))
        print("</tr>")
    print("</table>")

    print("<h2 style='font-size:30px;position:absolute;top:280px;right:420px;'>Hitting State Leader</h2>")
    state = ['Name','G','PA','HR','RBI','SB','BB%','K%','ISO','BABIP','AVG','OBP','SLG','wOBA','wRC+','Off','Def','WAR']
    record_tab = gethitleader(input_team)
    print("<table border = '1' style='position:absolute;top:370px;right:160px'>")
    print("<tr>")
    for i in state:
        print("<td>{}</td>".format(i))
    print("</tr>")
    for i in range(0,5):
        print("<tr>")
        for j in range(0,18):
            print("<td>{}</td>".format(record_tab[i][j]))
        print("</tr>")
    print("</table>")

    print("<h2 style='font-size:30px;position:absolute;top:580px;right:420px;'>Pitching State Leader</h2>")
    state = ['Name','W','L','SV','G','GS','IP','K/9','BB/9','HR/9','BABIP','LOB%','GB%','HR/FB','ERA','FIP','xFIP','WAR']
    record_tab = getpitchleader(input_team)
    print("<table border = '1' style='position:absolute;top:670px;right:160px'>")
    print("<tr>")
    for i in state:
        print("<td>{}</td>".format(i))
    print("</tr>")
    for i in range(0,5):
        print("<tr>")
        for j in range(0,18):
            print("<td>{}</td>".format(record_tab[i][j]))
        print("</tr>")
    print("</table>")



    print("<form action='teaminfo.py' method='post' target='_blank'>")
    print("<select name='TeamName' style='position:absolute;right:590px;top:100px;font-size:20px;'>")
    for i in range(0,30):
          name = (sql()[i])
          print("<option value='{}'>{}</option>".format(name,name))
    print("</select>"
          "<input type='submit' value='submit' style='position:absolute;right:515px;top:100px;font-size:18px'</input>"
          "</form>")
    print("</body>"
          "</html>")

main()

