'''
	BaseClient

	Base class for router clients.
'''

import message
from ConcurrenTree.util.crypto.encryptor import Flip

class BaseClient(object):
	def __init__(self, router):
		self.router = router
		self.router._loadclient(self)

	def send(self, msg):
		# Send message to router
		self.router.recv(msg)

	def route(self, msg):
		# Recieve message from router
		raise NotImplementedError("Subclasses of BaseClient must define route()")

class SimpleClient(BaseClient):
	def __init__(self, router, interface, getencryptor):
		'''
			getencryptor should be a function that accepts an argument "iface"
			and returns an object that fits the "encryptor" API - that is, it
			has member functions encrypt(string) and decrypt(string).
		'''
		self.interface = interface
		BaseClient.__init__(self, router)
		self.getencryptor = getencryptor

	def route(self, msg):
		# Recieve message from router (will be type 'r', which contains message)
		msg = self.unpack(msg)
		if msg.type == 'r':
			self.send(msg)
		elif msg.type == 's':
			print "Recieved from %s: %s" % (repr(msg.addr),repr(self.unpack(msg).content))

	def unpack(self, msg):
		# Return the message inside a Type R
		encryptor = self.getencryptor(msg.addr)
		if msg.addr = self.interface:
			encryptor = Flip(encryptor)
		msg.decode(encryptor)
		return message.Message(msg)

	def write(self, addr, txt):
		# Write and send a message to addr
		sig_s = self.getencryptor(self.interface)
		msg   = message.make('s', self.interface, sig_e, txt)
		sig_r = self.getencryptor(addr)
		self.send(message.make('r', addr, sig_r, str(msg)))
