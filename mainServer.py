#!/usr/bin/python
import os
import subprocess
from twisted.internet import protocol,reactor,endpoints
import SimpleProxyV2 as myProxy
import threading

class mainServer(protocol.Protocol):
	def dataReceived(self,data):
		hostIP=str(self.transport.getPeer().host)
		hostPort=str(self.transport.getPeer().port)
		#print repr(data)
		#self.transport.write(data)
		tempClient = (c for c in clients if (c["host"] == hostIP and c["port"]==hostPort)).next()
		port=tempClient["proxyPort"]
		message = data.strip("\r\n")
		#client send "start" command to start Proxy+Capture Server
		print "[status]recieved message:%s from %s:%s"%(data,hostIP,hostPort)
		if(message=="start" and tempClient["proxy"]!=True):
			self.transport.write("200 OK Server Start\n")
			try:
				t=threading.Thread(target=myProxy.start,args=(port,))
				t.daemon=True
				t.start()
				self.transport.write("201 Running Proxy OK on port:"+str(port)+"\n")
				#remove client in clients and replcae with tempClient
				clients.remove(tempClient)
				tempClient["proxy"]=True
				clients.append(tempClient)
			except Exception as e:
				self.transport.write("[Error]"+str(e)+"\n")
		elif(message=="start" and tempClient["proxy"]==True):
			self.transport.write("202 Proxy Server is running already\n")
		#client senf "stop" command to stop Proxy+Capture Server
		elif(message=="stop"):
			self.transport.write("203 OK Server Stop\n")
			#change tempClient proxy status to False and replace in clients
			clients.remove(tempClient)
			tempClient["proxy"]=False
			clients.append(tempClient)
		elif(message=="exit"):
			print "999 bye: "+str(hostIP)
			self.transport.loseConnection()
		elif(message=="dbg"):
			showClients()
		elif(message==""):
			pass
		else:
			self.transport.write("500 Error Unknown Command\n")
	
	#called when connection lost
	def connectionLost(self,reason):
		hostIP=str(self.transport.getPeer().host)
		hostPort=str(self.transport.getPeer().port)
		tempClient = (c for c in clients if (c["host"] == hostIP and c["port"]==hostPort)).next()
		clients.remove(tempClient)

class mainFactory(protocol.Factory):
	def buildProtocol(self,addr):
		print "[status]"+str(addr.host)+":"+str(addr.port)+" is Connected."
		#making couple client
		client={'host':None,'port':None,'proxyPort':None,'proxy':False}
		client['host']=str(addr.host)
		client['port']=str(addr.port)
		client['proxyPort']=str(get_open_port())
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
endpoints.serverFromString(reactor,"tcp:2222").listen(mainFactory())
reactor.run()

