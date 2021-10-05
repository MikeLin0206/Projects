#!/usr/bin/env python3

import cgi
import cgitb

cgitb.enable()

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
print("</body>"
      "</html>")
