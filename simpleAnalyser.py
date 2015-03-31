#Simple Packets Payload analyser

class simpleAnalyser():

	def __init__(self):
		self.mode="http"

	def payload2dict(self,payload):
		#split payload string into multiple line
		lines = payload.split("\r\n")
		result={}
		#split each line in the list into lists of key-value
		for line in lines:
			kv=line.split(" ",1)
			k=kv[0]
			v=kv[1]
			#add into result
			result[k]=v
		#result = lines
		return result
		

