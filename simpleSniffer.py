#!/usr/bin/python

from scapy.all import *
import threading

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

	def run(self):
		self.pkts=sniff(filter=self.filter,prn=lambda x:self.pkts.append(x))

	#def write(self,filename):
	#	wrpcap(filename,self.pkts)

	def summary(self):
		summary=""
		for pkt in self.pkts:
			summary+=str(pkt.summary())+"\n"
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
		result+="END"
		return result


def main():
	s=simpleSniffer("127.0.0.1","2222","128.199.255.155","23232")
	print "debug filter"
	print str(s.filter)
	#s.sniff()

if __name__=="__main__":
	main()
