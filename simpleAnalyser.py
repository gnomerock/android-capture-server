#Simple Packets Payload analyser

class simpleAnalyser():

	def __init__(self):
		self.mode="http"

	def payload2dict(self,payload):
		#split payload string into multiple line
		payload=payload.strip("\r\n")
		lines = payload.split("\r\n")
		result={}
		#split each line in the list into lists of key-value
		for line in lines:
			kv=line.split(" ",1)
			k=kv[0].strip(":")
			v=kv[1]
			#add into result
			result[k]=v
		#result = lines
		return result
	
	def getHostList(self,pkts):
		hostList=[]
		portList=[]
		for pkt in pkts[1:]:
			#check host is contain in list or not?
			#if not, append to the list

			#using try for avoid no key exception
			try:
				pkt.load
				host = self.payload2dict(pkt.load)['Host']
				print "1+"+host
				port = pkt.sport
			except:
				continue
			print "2+"+host
			if host not in hostList:
				hostList.append(host)
				portList.append(port)

		return hostList,portList


