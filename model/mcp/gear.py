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

		self.storage.listen(self.on_storage_event)

	# Functional creators

	def client(self, interface, encryptor=None):
		self.makejack(interface)
		iface = strict(interface)
		if encryptor != None:
			self.resolve_set(interface, encryptor)
		if not iface in self.clients:
			self.clients[iface] = self.mkclient(self.router, interface, self.resolve)
		return self.setclientcallback(iface)

	def document(self, docname):
		if docname in self.storage:
			# Return existing document
			return self.setdocsink(docname)
		else:
			# Create blank document
			self.storage[docname] = document.Document({})
			return self.setdocsink(docname)

	# Assistants to the functional creators

	def setclientcallback(self, interface):
		self.clients[interface].rcv_callback = self.rcv_callback
		return self.clients[interface]

	def setdocsink(self, docname):
		doc = self.storage[docname]
		def opsink(op):
			self.storage.op(docname, op)
			#self.document(docname).apply(op)
			#self.send(docname, op, doc.participants)
		doc.opsink = opsink
		return doc

	def makejack(self, iface):
		iface = tuple(iface[:2])
		if not self.router.jack(iface):
			j = jack.make(self.router, iface)
			j.run_threaded()
			return j

	# Basic messages

	def hello(self, target):
		# Send your encryption credentials to an interface
		for c in self.clients:
			self.clients[c].hello(target)

	def dm(self, target, message):
		# Send a direct message to an interface
		self.send(target, {"type":"dm", "contents":message})

	# Sender functions

	def send(self, iface, msg, senders=None):
		# Try multiple clients until it sends or fails
		# Will use self.clients unless variable "senders" is set.

		# Convert dicts to type J messages.
		if type(msg) == dict:
			msg = 'j\x00' + strict(msg)

		# Create a list of interfaces to try.
		clients = senders or self.clients

		# Try until something sends without raising an exception.
		from ConcurrenTree.util.crashnicely import Guard
		for c in clients:
			if type(c) not in (str, unicode):
				c = strict(c)
			with Guard():
				return self.clients[c].write(iface, msg)
			print>>stderr, c,"->",iface,"failed"
		print>>stderr, "All clients failed to contact", iface

	def send_op(self, docname, op, ifaces=[]):
		# Send an operation message.
		# If you specify the interfaces variable, it will send only to those interfaces.
		# Otherwise, it'll use the result of the document's routes_to().
		proto = op.proto()
		proto['docname'] = docname
		proto['version'] = 0
		if ifaces:
			for i in ifaces:
				self.send(i, proto)
		else:
			for c in self.clients:
				client = self.clients[c]
				ciface = client.interface
				targets = self.document(docname).routes_to(ciface)
				for t in targets:
					self.send(t, proto, [c])

	def send_full(self, docname, ifaces=[]):
		# Send a full copy of a document.
		doc = self.document(docname)
		self.send_op(docname, doc.root.childop(), ifaces)

	# Callbacks for incoming data

	def rcv_callback(self, msg, client):
		self.rcv_json(msg.ciphercontent, msg.addr)

	def rcv_json(self, content, sender = None):
		content = json.loads(content)
		t = content['type']
		if t == "hello":
			self.resolve_set(content['interface'], content['key'])
		elif t == "op":
			#print content
			op = operation.Operation(content['instructions'])
			self.storage.op(content['docname'], op)
		elif t == "dm":
			print "Direct message from", sender
			print repr(content['contents'])

	def on_storage_event(self, typestr, docname, data):
		# Callback for storage events
		if typestr == "op":
			self.send_op(docname, data)

	# Utilities and conveninence functions.

	def add_participant(self, docname, iface):
		# Adds person as a participant and sends them the full contents of the document.
		doc = self.document(docname)
		doc.add_participant(iface)
		self.send_full(docname, [iface])

	def resolve(self, iface):
		# Return the cached encryptor proto for an interface.
		iface = strict(iface)
		return self.resolve_table[iface].value[0]

	def resolve_self(self):
		# Encryptor protos for each of your clients.
		result = {}
		for iface in self.clients:
			if iface in self.resolve_table:
				result[iface] = self.resolve_table[iface]
			else:
				result[iface] = None
		return result

	def resolve_set(self, iface, key, sigs = []):
		# Set the encryptor proto for an interface in the cache table.
		iface = strict(iface)
		value = [key, sigs]
		self.resolve_table[iface] = value

	@property
	def resolve_table(self):
		# Cache table document for interface:encryptor proto relationships.
		return self.document("?resolve").wrapper()
