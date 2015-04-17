#!/usr/bin/python
import os
import subprocess
from twisted.internet import protocol,reactor,endpoints
import SimpleProxy
import simpleSniffer as mySniffer
import threading
import multiprocessing
import sys

import proxyWithHttps

from twisted.python import log
#log.startLogging(sys.stdout)

class mainServer(protocol.Protocol):

	def __init__(self):

		self.sniffer=None
		self.t1=None
		self.t2=None
		self.p1=None
		self.p2=None

	def dataReceived(self,data):

		#protect Exception error by assign variable 1st
		hostIP=str(self.transport.getPeer().host)
		hostPort=str(self.transport.getPeer().port)
		
		#find client in the client list
		tempClient = (c for c in clients if (c["host"] == hostIP and c["port"]==hostPort)).next()
		port=tempClient["proxyPort"]
		message = data.strip("\r\n")

		#client send "start" command to start Proxy+Capture Server
		print "[status]recieved message:%s from %s:%s"%(data,hostIP,hostPort)

		#Checking Message from CLients
		#Start
		if(message.strip()=="start" and tempClient["proxy"]!=True):
			self.transport.write("200 OK Server Start\n")
			try:
				#run Proxy for client
				self.transport.write("201 Running Proxy OK on port:"+str(port)+"\n")

				#Create Proxy Sevice and listen to the port that send to client
				#import twisted.web.http
				#factory = twisted.web.http.HTTPFactory()
				#factory.protocol = proxyWithHttps.ConnectProxy
				#endpoints.serverFromString(reactor,"tcp:"+port).listen(factory)

				#Change proxy status of client
				clients.remove(tempClient)
				tempClient["proxy"]=True
				clients.append(tempClient)

			except Exception as e:
				self.transport.write("[Error]"+str(e)+"\n")

		#Start
		elif(message.strip()=="start" and tempClient["proxy"]==True):
			self.transport.write("202 Proxy Server is running already\n")

		#sniff command to start sniffing
		elif(message.strip()=="sniff" ):

			#start the sniff
			self.transport.write("204 start sniffing"+"\n")
			self.sniffer=mySniffer.simpleSniffer(tempClient["host"],tempClient["proxy"],"128.199.255.155",tempClient["proxyPort"])
			

			#t2=threading.Thread(target=sniffer.sniff)
			#result=sniffer.sniff()
			#t2.daemon=True
			#t2.start()
			
			#self.p2=multiprocessing.Process(target=self.sniffer.sniff)
			#self.p2.daemon = True
			#self.p2.start()
			#self.p2.is_alive()
			
			self.sniffer.daemon=True
			self.sniffer.start()

		elif(message.strip()=="getsum"):
			self.transport.write(self.sniffer.summary())
		#client senf "stop" command to stop Proxy+Capture Server
		elif(message.strip()=="stop"):
			self.transport.write("203 OK Server Stop\n")
			#change tempClient proxy status to False and replace in clients
			clients.remove(tempClient)
			tempClient["proxy"]=False
			clients.append(tempClient)
			
		elif(message.strip()=="stopsniff"):
			self.sniffer.join(1)
			self.transport.write("206 Stop sniffing\n")

		elif(message.strip()=="exit"):
			print "999 bye: "+str(hostIP)
			self.transport.loseConnection()
		elif(message.strip()=="dbg"):
			showClients()
		elif(message==""):
			pass
		elif message == "getdummy":
			file = open("capfiles/test.cap")
			rawData = file.read()
			self.transport.write(rawData)
		#get detail each  packet by packetIndex
		elif message[0:3] == "sum":
			index = int(message.strip("sum"))
			print str(index)+" type: "+str(type(index))
			returnMessage=self.sniffer.getPktDetail(index)
			self.transport.write(returnMessage)
		else:
			self.transport.write("500 Error Unknown Command\n")
	
	#called when connection lost
	def connectionLost(self,reason):
		hostIP=str(self.transport.getPeer().host)
		hostPort=str(self.transport.getPeer().port)
		tempClient = (c for c in clients if (c["host"] == hostIP and c["port"]==hostPort)).next()
		clients.remove(tempClient)
		print hostIP+" is disconnected."

class mainFactory(protocol.Factory):
	def buildProtocol(self,addr):
		print "[status]"+str(addr.host)+":"+str(addr.port)+" is Connected."
		#making couple client
		client={'host':None,'port':None,'proxyPort':None,'proxy':False}
		client['host']=str(addr.host)
		client['port']=str(addr.port)
		#i commend line below for making static proxy 
		#client['proxyPort']=str(get_open_port())
		client['proxyPort']="999"
		clients.append(client)
		#print str(clients)
		print "[status]"+str(client['proxyPort'])+" is open for "+str(client['host'])
		return mainServer()

#random unbinded port
def get_open_port():
		import socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(("",0))
		s.listen(1)
		port = s.getsockname()[1]
		s.close()
		return port

#show clients table
def showClients():
	print "################"
	print "# Service Table#"
	print "################"
	print "%20s%12s%12s%12s"%("clientIP","clientPort","proxyPort","proxyStat")
	for client in clients:
		print "%20s%12s%12s%12s"%(client["host"],client["port"],client["proxyPort"],client["proxy"])

#search a list of dictionaries
def find(host,port):
	result = (c for c in clients if (c["host"]==host and c["port"]==port)).next()


print "################"
print "# Project 492  #"
print "################"


clients=[]
#Create Proxy Sevice and listen to the port that send to client
import twisted.web.http
factory = twisted.web.http.HTTPFactory()
factory.protocol = proxyWithHttps.ConnectProxy
endpoints.serverFromString(reactor,"tcp:999").listen(factory)
endpoints.serverFromString(reactor,"tcp:2222").listen(mainFactory())
reactor.run()

