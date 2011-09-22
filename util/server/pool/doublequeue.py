''' 
	A two-way queue that allows strongly directionalized
	thread-safe communication.
'''

from Queue import Queue, Empty
from thread import error as threaderror

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
		self._servernotify = None
		self._clientnotify = None

	def client_push(self, obj, timeout=None):
		self.notify(self._servernotify)
		self.server.put(obj, timeout=timeout)

	def server_push(self, obj, timeout=None):
		self.notify(self._clientnotify)
		self.client.put(obj, timeout=timeout)

	def client_pull(self, timeout=None):
		return self.client.get(timeout=timeout)

	def server_pull(self, timeout=None):
		return self.server.get(timeout=timeout)

	def client_notify(self, function):
		self._clientnotify = function

	def server_notify(self, function):
		self._servernotify = function

	def notify(self, function):
		if function:
			return function()
