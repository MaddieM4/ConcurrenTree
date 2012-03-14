from ConcurrenTree.util import crypto
from ConcurrenTree.util.hasher import strict
from ConcurrenTree.model import document, operation
import message

from sys import stderr
import jack
import json

class Gear(object):
	# Tracks clients in router, and documents.
	def __init__(self, storage, router, mkclient):
		self.storage = storage
		self.router = router
		self.mkclient = mkclient
		self.clients = {}

	def client(self, interface, encryptor=None):
		self.makejack(interface)
		iface = strict(interface)
		if encryptor != None:
			self.resolve_set(interface, encryptor)
		if not iface in self.clients:
			self.clients[iface] = self.mkclient(self.router, interface, self.resolve)
		return self.setclientcallback(iface)

	def setclientcallback(self, interface):
		self.clients[interface].rcv_callback = self.rcv_callback
		return self.clients[interface]

	def document(self, docname):
		if docname in self.storage:
			# Return existing document
			return self.setdocsink(docname)
		else:
			# Create blank document
			self.storage[docname] = document.Document({})
			return self.setdocsink(docname)

	def setdocsink(self, docname):
		doc = self.storage[docname]
		def opsink(op):
			self.document(docname).apply(op)
			self.send(docname, op, doc.participants)
		doc.opsink = opsink
		return doc

	def send(self, docname, op, ifaces):
		proto = op.proto()
		proto['track'] = 1
		proto['docname'] = docname
		proto['version'] = 0
		for i in ifaces:
			self.client_send(i, strict(proto))

	def send_client(self, iface, msg):
		# Try multiple clients until it sends or fails
		if type(msg) == dict:
			msg = 'j\x00' + strict(msg)
		for c in self.clients:
			try:
				return self.clients[c].write(iface, msg)
			except:
				print>>stderr, c,"->",iface,"failed"
		print>>stderr, "All clients failed to contact", iface

	def rcv_callback(self, msg, client):
		self.rcv_json(msg.ciphercontent, msg.addr)

	def rcv_json(self, content, sender = None):
		content = json.loads(content)
		t = content['type']
		if t == "hello":
			self.resolve_set(content['interface'], content['key'])
		elif t == "op":
			op = operation.Operation(content.instructions)
			self.storage.op(content['docname'], op)
		elif t == "dm":
			print "Direct message from", sender
			print repr(content['contents'])

	def hello(self, target):
		for c in self.clients:
			self.clients[c].hello(target)

	def dm(self, target, message):
		self.send_client(target, {"type":"dm", "contents":message})

	def makejack(self, iface):
		iface = tuple(iface[:2])
		if not self.router.jack(iface):
			j = jack.make(self.router, iface)
			j.run_threaded()
			return j

	def resolve(self, iface):
		iface = strict(iface)
		return json.loads(str(self.resolve_table[iface]))[0]

	def resolve_self(self):
		# Client encryptor prototypes
		result = {}
		for iface in self.clients:
			if iface in self.resolve_table:
				result[iface] = self.resolve_table[iface]
			else:
				result[iface] = None

	def resolve_set(self, iface, key, sigs = []):
		iface = strict(iface)
		value = strict([key, sigs])
		self.resolve_table[iface] = value

	@property
	def resolve_table(self):
		return self.document("?resolve").wrapper()
