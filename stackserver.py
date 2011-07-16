''' 
	A class that lets you stack services according to
	configurations.
'''

from BCP.serverpool import ServerPool

class StackServer(ServerPool):
	def __init__(self, configstring=""):
		self.configure(configstring)

	def configure(self, configstring):
		pass

	def run(self):
		pass

	def policy(self):
		pass

	def starting(self):
		pass

	def close(self):
		pass
