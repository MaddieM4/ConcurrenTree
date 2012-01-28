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
		msg = Message(msg)
		if msg.type == "r":
			recvr = self.client(msg.addr) or self.jack(msg.addr)
			if recvr:
				recvr.route(msg)
			else:
				print "Could not deliver message:", str(msg.addr)
		elif msg.type == "s":
			print "Message recieved directly from "+str(msg.addr)

	def client(self, addr):
		# Return client registered at addr, or None
		addr = tuple(addr[:3])
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
		key = tuple(jack.interface[0])
		self._jacks[key] = jack

	def _loadclient(self, client):
		key = tuple(client.interface[:3])
		self._clients[key] = client
