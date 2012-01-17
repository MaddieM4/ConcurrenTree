from ConcurrenTree.model import operation, address, document
from extension import *

class Data(Extension):
	def __init__(self, docs):
		Extension.__init__(self, "data", {
			"create": self._create,
			"select": self._select,
			"op": self._op,
			"get": self._get,
			"check": self._check,
			"tsum": self._tsum,
			"subscribe": self._subscribe,
			"unsubscribe": self._unsubscribe
		}, bound = True)
		self.docs = docs

		self.here = Peer()
		self.there = Peer()

	# UTILITIES

	def select(self, conn, docname):
		if self.here.selected != docname:
			conn.push("select", docname=docname)
			self.here.selected = docname

	def subscribe(self, conn, docnames=None):
		if docnames==None:
			if self.here.selected:
				conn.push("subscribe")
			else:
				raise ValueError("Cannot subscribe to selected with no document selected")
		else:
			docnames = list(docnames)
			conn.push("subscribe", docnames=docnames)
			self.here.subscriptions.update(docnames)

	def check(self, conn, name, addr = []):
		addr = address.Address(addr).proto() # Make sure it's proto
		self.select(conn, name)
		conn.push("check", address=addr)

	def sendop(self, conn, name, addr = []):
		addr = address.Address(addr)

		result = operation.FromStructure(self.docs[name].root, addr)

		self.select(conn, name)
		conn.push("op", address = addr.proto(), instructions=result.proto()['instructions'])

	def check_selected(self, conn, is_loaded=True):
		''' Confirm that remotely selected docname exists '''
		if not self.there.selected:
			self.error(conn, 405) # No document selected
		if is_loaded and not self.there.selected in self.docs:
			self.error(conn, 404) # Document not found

	@property
	def fdoc(self):
		''' Foreign selected document '''
		return self.docs[self.there.selected]

	@property
	def ldoc(self):
		''' Locally selected document '''
		return self.docs[self.here.selected]

	# MESSAGE HANDLERS

	def _create(self, conn, obj):
		self.require(conn, "docname", obj)
		name = obj['docname']

		if not name in self.docs:
			self.docs[name] = document.Document({})

	def _select(self, conn, obj):
		self.require(conn, "docname", obj)
		name = obj['docname']

		if not name in self.docs:
			self.error(conn, 404)

		print "Selecting" + name
		self.there.selected = name

	def _op(self, conn, obj):
		self.check_selected(conn)
		self.require(conn, "instructions", obj)
		try:
			op = operation.Operation(instructions = obj['instructions'])
		except operation.ParseError:
			self.error(conn, 453)
		# TODO: authorize
		if not op.applied(self.fdoc):
			try:
				op.apply(self.fdoc)
				print "Tree '%s' modified: '%s'" % (self.there.selected, self.fdoc.flatten())
				print "New hash: '%s'" % self.fdoc.hash
				self.pool_push({
					"type":"op",
					"docname":self.there.selected,
					"value":op
				})
			except operation.OpApplyError:
				self.error(conn, 500) # General Local Error
		else:
			print "Op was already applied"

	def _get(self, conn, obj):
		self.check_selected(conn)
		self.require(conn, "address", obj)
		self.sendop(conn, self.there.selected, obj['address'])

	def _check(self, conn, obj):
		# TODO - error testing
		self.check_selected(conn)
		self.require(conn, "address", obj)

		addr = address.Address(obj['address'])
		sum = addr.resolve(self.fdoc.root).hash
		self.select(conn, self.there.selected)
		conn.push("tsum",address=addr.proto(), value=sum)

	def _tsum(self, conn, obj):
		self.check_selected(conn)
		self.require(conn, "address", obj)
		self.require(conn, "value", obj)

		# Compare to our own hash
		addr = address.Address(obj['address'])
		sum = addr.resolve(self.fdoc.root).hash
		if sum != obj['value']:
			self.sendop(conn, self.there.selected, addr)
			conn.push("get", address=addr.proto(), depth=1)

	def _subscribe(self, conn, obj):
		if "docnames" not in obj:
			self.check_selected(conn)
			obj[docnames] = [self.there.selected]
		for name in obj['docnames']:
			self.docs.subscribe(name)
			self.there.subscriptions.add(name)

	def _unsubscribe(self, conn, obj):
		# TODO Use doc unsubscription
		if "docnames" in obj:
			if len(obj['docnames']) > 0:
				for name in obj['docnames']:
					self.there.subscriptions.discard(name)
			else:
				self.there.subscriptions.clear()
		else:
			if not self.check_selected(conn): return
			self.there.subscriptions.discard(self.there.selected)

class Peer:
	''' Represents a remote endpoint. '''
	def __init__(self):
		self.selected = None
		self.subscriptions = set()
