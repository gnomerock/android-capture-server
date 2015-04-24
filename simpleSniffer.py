#!/usr/bin/python

from scapy.all import *
import threading
import simpleAnalyser as myAnalyser

class simpleSniffer(threading.Thread):
	
	def __init__(self,client,clientPort,server,serverPort):
		threading.Thread.__init__(self)
		self.client=client
		self.server=server
		self.clientPort=clientPort
		self.serverPort=serverPort
		self.filter = "(src host "+self.client+" and dst host "+self.server+")"
		self.filter += " or (src host "+self.server+" and dst host "+self.client+")"
		self.pkts=[]

		self.analyser=myAnalyser.simpleAnalyser()

	def run(self):
		self.pkts=sniff(filter=self.filter,prn=lambda x:self.pkts.append(x))

	#def write(self,filename):
	#	wrpcap(filename,self.pkts)

	def summary(self):
		summary=""
		for pkt in self.pkts:
			summary+=str(pkt.summary())+" "+str(self.getColorCode(pkt))+"\n"
		summary+="END\n"
		return summary

	def getPktDetail(self,index):
		from cStringIO import StringIO
		import sys
		#ls() print to stdout, so we need to redirect result from stdout to variable
		#set new stdout
		mystdout=StringIO()
		save_stdout = sys.stdout
		sys.stdout = mystdout
		ls(self.pkts[index])
		result=mystdout.getvalue()
		sys.stdout = save_stdout
		result+="END\n"
		return result

	def filterByDstPort(self,port):
		result = []
		for pkt in self.pkts:
			#print str(pkt.dport)
			if pkt.dport == port:
				result.append(pkt)
		return result

	def printSumOf(self,pkts):
		summary=""
		for pkt in pkts:
			summary+=str(pkt.summary())+"\n"
		summary+="END\n"
		return summary

	def getColorCode(self,pkt):
		#1 for http
		#2 for https
		#3 for tcp
		try:
			data = self.analyser.payload2dict(pkt.load)
		except:
			return 3
		#HTTP
		if "get" in data:
			return 1
		if "connect" in data:
			return 2


def main():
	s=simpleSniffer("127.0.0.1","2222","128.199.255.155","23232")
	print "debug filter"
	print str(s.filter)
	#s.sniff()

if __name__=="__main__":
	main()
