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
    print("<form action='teaminfo.py' method='post' target='_blank'>")
    print("<select name='TeamName' style='position:absolute;right:590px;top:100px;font-size:20px;'>")
    for i in range(0,30):
          name = (sql()[i])
          print('<option value="{}">{}</option>'.format(name,name))
    print("</select>"
          "<input type='submit' value='submit' style='position:absolute;right:515px;top:100px;font-size:18px'/>"
          "</form>")
    print("</body>"
          "</html>")

main()
