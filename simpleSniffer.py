#!/usr/bin/python

from scapy.all import *

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
		return self.pkts.summary()

	def write(self,filename):
		wrpcap(filename,self.pkts)
		
def main():
	s=simpleSniffer("127.0.0.1","12345","128.199.255.155","23232")
	print "debug filter"
	print str(s.filter)
	s.sniff()
	s.write("test.cap")

if __name__=="__main__":
	main()
