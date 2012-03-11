from ConcurrenTree.util.hasher import strict
from ConcurrenTree.model import document
import jack

class Gear(object):
	# Tracks clients in router, and documents.
	def __init__(self, storage, router, mkclient):
		self.storage = storage
		self.router = router
		self.mkclient = mkclient
		self.clients = {}

	def client(self, interface):
		self.makejack(interface)
		interface = strict(interface)
		if not interface in self.clients:
			self.clients[interface] = self.mkclient(self.router, interface, self.resolve)
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
		for c in self.clients:
			try:
				return self.clients[c].send(iface, msg)
			except:
				print>>stderr, c,"->",iface,"failed"
		print>>stderr, "All clients failed to contact", iface

	def makejack(self, iface):
		iface = tuple(iface[:2])
		if not self.router.jack(iface):
			return jack.make(self.router, iface)

	def resolve(self, iface):
		iface = strict(iface)
		return self.resolve_table[iface][0]

	def resolve_set(self, iface, key, sigs = []):
		iface = strict(iface)
		value = [key, sigs]
		self.resolve_table[iface] = value

	@property
	def resolve_table(self):
		return self.document("?resolve").wrapper()
