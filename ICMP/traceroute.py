import socket
import os
import array
import struct
import sys
import time

class Ping():
    def __init__(self, timeout):
        self.PID = os.getpid()
        self.timeout = timeout;
        pass

    def createSocket(self,ttl):
        icmp = socket.getprotobyname("icmp")
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        sock.setsockopt(socket.SOL_IP, socket.IP_TTL,ttl)
        return sock

    def calculateChecksum(self, packet):
        checksum = 0
        words = array.array("h",packet)
        for word in words:
            checksum += word

        return ~checksum

    def makeICMPPacket(self):
        header = struct.pack("bbhhh", 8, 0, 0, self.PID, 0)
        data = struct.pack("qqqq", 1, 1, 1, 1)
        packet = header + data
        checksum = self.calculateChecksum(packet)
        newHeader =  struct.pack("bbhhh", 8, 0, checksum, self.PID, 0)
        packet = newHeader +  data
        return packet

    def sendPing(self,targetHost,ttl):
        targetAddr = socket.gethostbyname(targetHost)
        ICMPSock = self.createSocket(ttl)
        packet = self.makeICMPPacket()
        ICMPSock.settimeout(self.timeout)

        startTime = time.time()
        complete = 0
        returnInfo = []
        ICMPSock.sendto(packet,(targetHost,20001))
        try:
            ac_ip = ICMPSock.recvfrom(1024)[1][0]
            if ac_ip == targetAddr:
                complete = 1
            recvTime = time.time()
            totalTime = (recvTime - startTime) * (10 ** 3)
            ICMPSock.close()
            returnInfo.append(int(totalTime))
            returnInfo.append(ac_ip)
            returnInfo.append(complete)
           # print(totalTime)
            return totalTime, ac_ip, complete
        except socket.timeout:
            ICMPSock.close()
            return 0

#argvLen = len(sys.argv)
#targetName = sys.argv[argvLen - 1]

lost = 0
times = 0
totalTime = 0
maximumTime = 0
minimumTime = 1000000
hop = 30
ttl = 1
complete = 1
d_flag = 0
timeout = 1
addr = ""
argvLen = len(sys.argv)
target = sys.argv[argvLen - 1]


if argvLen == 1:
    print("\nUsage: traceroute.py [-d] [-h maximum_hop] [-w timeout]\n")
    print("Option:")
    print("     -d               Do not resolve address to hostnames.")
    print("     -h maximum_hop   Maximum number of hops to search for target.")
    print("     -w timeout       Wait timeout milliseconds for each reply.")
    exit()
    
try:
    targetHost = socket.gethostbyname(target)
    targetName = target
except:
    targetHost = target
    targetName = socket.gethostbyaddr(target)
    
if "-d" in sys.argv:
    d_flag = 1

if "-h" in sys.argv:
    index = sys.argv.index("-h")
    hop = int(sys.argv[index + 1])
    
if "-w" in sys.argv:
    index = sys.argv.index("-w")
    timeout = int(sys.argv[index + 1])

pinger = Ping(timeout)

print("Tracing route to {} [{}]".format(targetName,targetHost))
print("over a maximum of {} hops:".format(hop))

for i in range(1,hop + 1):
    print("{:>2}.".format(i),end = "")
    for k in range(0,3):
        info = pinger.sendPing(targetName,ttl)
        if info == 0:
            times = "*"
        else:
            addr = info[1]
            complete = info[2]
            times = int(info[0])
            if times < 1:
                times = "<1"

        print("{:>5} ms".format(times),end = "")
    if d_flag == 0:
        try:
            print("  {} {}".format(socket.gethostbyaddr(addr)[0],addr))
        except:
            print("  {}".format(addr))
    else:
        print("  {}".format(addr))       
            
    if complete == 1:
        print()
        print("Trace complete.")
        break
    ttl += 1

