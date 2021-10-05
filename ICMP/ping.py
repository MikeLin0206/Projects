import socket
import os
import array
import struct
import sys
import time

class Ping():
    def __init__(self,timeout):
        self.PID = os.getpid()
        self.timeout = timeout;
        self.a_flag = 0
        
    
    def setflag(self):
        pass

    def createSocket(self):
        icmp = socket.getprotobyname("icmp")
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
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

    def sendPing(self,targetHost):
        ICMPSock = self.createSocket()
        packet = self.makeICMPPacket()
        ICMPSock.settimeout(self.timeout)


        startTime = time.time()
        ICMPSock.sendto(packet,(targetHost,1))
        try:
            ac_ip = ICMPSock.recvfrom(1024)[1][0]
            recvTime = time.time()
            totalTime = (recvTime - startTime) * (10 ** 3)
            print("Reply by {}: bytes = 32 times = {:.0f} ms".format(targetHost,totalTime))
            return totalTime
        except socket.timeout:
            return 0



lost = 0
sent = 4
times = 0
totalTime = 0
maximumTime = 0
minimumTime = 1000000
argvLen = len(sys.argv)
timeout = 1

if argvLen == 1:
    print("\nUsage: ping.py [-t] [-a] [-n count] [-w timeout]\n")
    print("Option:")
    print("     -t         Ping the specified host until stopped.")
    print("                Type Control-C to stop.")
    print("     -a         Resolve addresses to hostnames.")
    print("     -n count   Number of echo requests to send.")
    print("     -w timeout Timeout in millisecond to wait for each reply.")
    exit()

if "-a" in sys.argv:
    targetHost = sys.argv[argvLen - 1]
    targetName = socket.gethostbyaddr(targetHost)
else:
    targetName = sys.argv[argvLen - 1]
    targetHost = socket.gethostbyname(targetName)     
    
if "-t" in sys.argv:
    sent = 100000    

if "-n" in sys.argv:
    index = sys.argv.index("-n")
    sent = int(sys.argv[index + 1])
    
if "-w" in sys.argv:
    index = sys.argv.index("-w")
    timeout = int(sys.argv[index + 1])
 
pinger = Ping(timeout)
print("Ping {} [{}] <Use 32 bytes data>:".format(targetName,targetHost))

for i in range(0,sent):
    times = pinger.sendPing(targetHost)

    if times == 0:
        lost += 1
    elif times > maximumTime:
        maximumTime = times
    elif times < minimumTime:
        minimumTime = times
    totalTime += times
    time.sleep(1)

print("\nPing statistics for {}:".format(targetHost))
print("Packet: Sent = {}, Recvived = {}, Lost = {} <0% loss>".format(sent,sent - lost,lost))
print("\nApproximate round trip times in milli-seconds:")
print("Minimum = {:.0f}ms, Maximum = {:.0f}ms, Average = {:.0f}ms".format(minimumTime,maximumTime,totalTime/sent))