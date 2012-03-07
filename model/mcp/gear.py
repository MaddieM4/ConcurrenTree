from ConcurrenTree.util.hasher import strict
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
			self.clients[interface] = self.mkclient(self.router, interface)
		return self.clients[interface]

	def document(self, docname):
		return self.storage[docname]

	def makejack(self, iface):
		iface = tuple(iface[:2])
		if not iface in self.router._jacks:
			return jack.make(self.router, iface)

	def resolve(self, iface):
		iface = strict(iface)
		return self.resolve_table[iface][0]

	def resolve_set(self, iface, key, sigs = [])
		iface = strict(iface)
		value = [key, sigs]
		self.resolve_table[iface] = value

	@property
	def resolve_table(self):
		return self.document("?resolve").wrapper()
