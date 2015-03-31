#Simple Packets Payload analyser

class simpleAnalyser():

	def __init__(self):
		self.mode="http"

	def payload2dict(self,payload):
		#split payload string into multiple line
		lines = payload.split("\r\n")
		

