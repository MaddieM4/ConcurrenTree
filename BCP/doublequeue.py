''' 
	A two-way queue that allows strongly directionalized
	thread-safe communication.
'''

from Queue import Queue

class DQ:
	''' 
		Always consistently use the same postfix for your
		functions in the same code. For example, always call
		pull_client and push_client from the client side,
		and pull_server and push_server from the server side.
		They're not named for their destinations but from what
		side the calling code is on.
	'''
	def __init__(self):
		self.server = Queue()
		self.client = Queue()

	def push_client(self, obj, timeout=None):
		self.server.put(obj, timeout=timeout)

	def push_server(self, obj, timeout=None):
		self.client.put(obj, timeout=timeout)

	def pull_client(self, timeout=None):
		return self.client.get(timout=timeout)

	def pull_server(self, timeout=None):
		return self.server.get(timout=timeout)
