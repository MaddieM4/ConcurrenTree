'''
	MCP Router.

	This virtual device takes jacks on one side for external communication,
	and clients on the other side for internal message routing.
'''

from message import Message

class Router(object):
	def __init__(self, jacks=[], clients=[]):
		self._jacks = {}
		self._clients = {}
		self._loadjacks(jacks)
		self._loadclients(clients)

	def recv(self, msg):
		# Accepts string or message.Message
		try:
			msg = Message(msg)
		except Exception as e:
			print "Could not parse message:", repr(msg)
			print e
			return
		if msg.type == "r":
			recvr = self.client(msg.addr) or self.jack(msg.addr)
			if recvr:
				recvr.route(msg)
			else:
				print "Could not deliver message:", str(msg.addr)
		elif msg.type == "s":
			print "Message recieved directly from "+str(msg.addr)

	def jack(self, addr):
		# Return jack registered at addr, or None
		addr = addr[0]
		if addr in self._jacks:
			return self._jacks[addr]
		else:
			return None

	def client(self, addr):
		# Return client registered at addr, or None
		addr = rtuple(addr[:3])
		if addr in self._clients:
			return self._clients[addr]
		else:
			return None


	def _loadjacks(self, jacks):
		for j in jacks:
			self._loadjack(j)

	def _loadclients(self, clients):
		for c in clients:
			self._loadclient(c)

	def _loadjack(self, jack):
		key = jack.interface[0]
		self._jacks[key] = jack

	def _loadclient(self, client):
		key = tuple(client.interface[:3])
		self._clients[key] = client

def rtuple(obj):
	# Convert lists into tuples recursively
	for i in range(len(obj)):
		if type(obj[i]) in (list, tuple):
			obj[i] = rtuple(obj[i])
	return tuple(obj)
