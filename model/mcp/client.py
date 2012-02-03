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
		unp = self.unpack(msg)
		unp.decode(self.getencryptor(unp.addr))
		print "Unpacked: "+repr(str(unp))
		if unp.type == 'r':
			self.send(unp)
		elif unp.type == 's':
			print "Recieved from %s: %s" % (repr(msg.addr),repr(unp.content))

	def unpack(self, msg):
		# Return the message inside a Type R
		encryptor = self.getencryptor(msg.addr)
		if msg.addr == self.interface:
			encryptor = Flip(encryptor)
		msg.decode(encryptor)
		return message.Message(msg.content)

	def write(self, addr, txt):
		# Write and send a message to addr
		self.owrite([addr], txt)

	def owrite(self, hoplist, txt):
		sig_s = self.getencryptor(self.interface)
		msg   = message.make('s', self.interface, sig_s, txt)
		hoplist = [(a, self.getencryptor(a)) for a in hoplist]
		for m in message.onion(msg, hoplist):
			self.send(m)

if __name__ == "__main__":
	import router, udpjack
	from ConcurrenTree.util.crypto.rotate import RotateEncryptor
	from ConcurrenTree.util import hasher

	target = None
	proxy = []

	def getencryptor(iface):
		return RotateEncryptor(int(hasher.checksum(iface)[:4], 16))

	r = router.Router()
	j = udpjack.UDPJack(r, port=int(raw_input("Host on port: ")))
	i = j.interface + ("sample",)
	c = SimpleClient(r, i, getencryptor)
	j.run_threaded() 
	
	def command(cmd):
		target = globals()['target']
		proxy  = globals()['proxy']

		def input(prompt):
			i = ""
			while not i:
				i = raw_input(prompt)
			return i

		cmd = cmd.lower()
		if cmd=="target":
			target = eval(input("Interface to send to: "))
		elif cmd=="msg":
			c.owrite(proxy+[target], input("Message to send: "))
		elif cmd=="proxy":
			proxy = eval(input("List of addresses: "))
		else:
			print "Unknown command."
		return target, proxy

	try:
		while 1:
			if target:
				print "target:", repr(target)
				print "proxy: ", repr(proxy)
				target, proxy = command(
					raw_input("Command ['target' | 'msg' | 'proxy']: "))
			else:
				target, proxy = command("target")
	except KeyboardInterrupt:
		j.close()
