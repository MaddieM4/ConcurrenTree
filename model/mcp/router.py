'''
	MCP Router.

	This virtual device takes jacks on one side for external communication,
	and clients on the other side for internal message routing.
'''

from message import Message
from ConcurrenTree.util.crashnicely import Guard

class Router(object):
	def __init__(self, jacks=[], clients=[]):
		self._jacks = {}
		self._clients = {}
		self._loadjacks(jacks)
		self._loadclients(clients)
		self.logging = True
		self.log = []

	def recv(self, msg):
		# Accepts string or message.Message
		#print "\nRouter incoming message: "+repr(str(msg))
		if self.logging:
			self.log.append(msg)
		try:
			msg = Message(msg)
		except Exception as e:
			print "Could not parse message:", repr(msg)
			print e
			return
		if msg.type == "r":
			recvr = self.client(msg.addr) or self.jack(msg.addr)
			if recvr:
				with Guard():
					recvr.route(msg)
			else:
				print "Could not deliver message:", str(msg.addr)
		elif msg.type == "s":
			print "Message recieved directly from "+str(msg.addr)

	def jack(self, addr):
		# Return jack registered at addr, or None
		for (t, l) in self._jacks:
			if t == addr[0]:
				return self._jacks[(t,l)]
		return None

	def client(self, addr):
		# Return client registered at addr, or None
		addr = rtuple(addr[:3])
		if addr in self._clients:
			return self._clients[addr]
		else:
			return None

	def thread_all(self):
		# Run all Jack threads
		for i in self._jacks:
			self._jacks[i].run_threaded()

	def _loadjacks(self, jacks):
		for j in jacks:
			self._loadjack(j)

	def _loadclients(self, clients):
		for c in clients:
			self._loadclient(c)

	def _loadjack(self, jack):
		key = rtuple(jack.interface[:2])
		self._jacks[key] = jack

	def _loadclient(self, client):
		key = rtuple(client.interface[:3])
		self._clients[key] = client

def rtuple(obj):
	# Convert lists into tuples recursively
	if type(obj) in (list, tuple):
		return tuple([rtuple(i) for i in obj])
	else:
		return obj
