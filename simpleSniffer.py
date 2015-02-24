#!/usr/bin/python

from scapy.all import *
import threading

class simpleSniffer():
	
	def __init__(self,client,clientPort,server,serverPort):
		self.client=client
		self.server=server
		self.clientPort=clientPort
		self.serverPort=serverPort
		self.filter = "(src host "+self.client+" and dst host "+self.server+")"
		self.filter += " or (src host "+self.server+" and dst host "+self.client+")"

	def sniff(self):
		self.pkts=sniff(filter=self.filter)

	def write(self,filename):
		wrpcap(filename,self.pkts)

	def summary(self):
		return str(self.pkts.summary())
		
def main():
	s=simpleSniffer("127.0.0.1","2222","128.199.255.155","23232")
	print "debug filter"
	print str(s.filter)
	s.sniff()

if __name__=="__main__":
	main()
