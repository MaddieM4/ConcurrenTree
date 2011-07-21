''' 
	A two-way queue that allows strongly directionalized
	thread-safe communication.
'''

from Queue import Queue, Empty

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

	def client_push(self, obj, timeout=None):
		self.server.put(obj, timeout=timeout)

	def server_push(self, obj, timeout=None):
		self.client.put(obj, timeout=timeout)

	def client_pull(self, timeout=None):
		return self.client.get(timeout=timeout)

	def server_pull(self, timeout=None):
		return self.server.get(timeout=timeout)
