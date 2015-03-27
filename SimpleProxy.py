#!/usr/bin/python

import sys

from twisted.web import proxy,http
from twisted.internet import reactor

class ProxyFactory(http.HTTPFactory):
	def buildProtocol(self,addr):
		return proxy.Proxy()

def start(port):
	reactor.listenTCP(int(port),ProxyFactory())
	#reactor.run(installSignalHandlers=False)
	print "Proxy Server is running on port: "+str(port)

def main():
	start(999)

if __name__=="__main__":
	main()


