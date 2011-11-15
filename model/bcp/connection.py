import json
import traceback

from ConcurrenTree.util.hasher import strict
from ConcurrenTree.model import operation, address
from ConcurrenTree.util.server.pool.connection import Connection
from peer import Peer
from errors import errors

nullbyte = "\x00"

class BCPConnection(Connection):
	''' A connection between two Peers '''
	def __init__(self, docs, auth):
		Connection.__init__(self)
		self._id = None
		self.poolsubs = {}

		self.docs = docs
		self.auth = auth

		self.here = Peer()
		self.there = Peer()
		self.initialize_documents()

	def incoming(self, value):
		''' Processes IO buffer '''
		if nullbyte in value:
			length = value.index(nullbyte)
			try:
				self.recv(value[:length])
			finally:
				return self.incoming(value[length+1:])
		else:
			return value

	def recv(self, msg):
		''' Takes a textual BCP message of unknown validity '''
		print "recving message:",msg
		try:
			obj = json.loads(msg)
		except ValueError:
			self.error(451) # Bad JSON
			return
		if type(obj)!=dict:
			self.error(454) # Wrong root type
			return
		try:
			self.analyze(obj, msg)
		except:
			traceback.print_exc()
			self.error(500)

	def outgoing(self, msg):
		''' Accepts messages from pool '''
		mtype = msg['type']
		mname = msg['docname']

		if mtype == "op":
			if mname in self.there.subscriptions:
				self.select(mname)
				self.send(msg['value'].proto())
		elif mtype == "subscribe":
			timeout = msg['timeout']
			if not mname in self.poolsubs:
				self.poolsubs[mname] = 0
				self.subscribe([mname])
			self.poolsubs[mname] = max(self.poolsubs[mname], timeout)
			# TODO: Expire subscriptions

	def pool_push(self, msg):
		print "Pool pushing",msg
		self.queue.client_push(msg)

	def push(self, msgtype, **kwargs):
		kwargs['type'] = msgtype
		self.send(kwargs)

	def send(self, msg):
		print "sending message:",msg
		self.ioqueue.client_push(strict(msg)+nullbyte)

	def select(self, docname):
		if self.here.selected != docname:
			self.push("select", docname=docname)
		self.here.selected = docname

	def subscribe(self, docnames=None):
		if docnames==None:
			if self.here.selected:
				self.push("subscribe")
			else:
				raise ValueError("Cannot subscribe to selected with no document selected")
		else:
			docnames = list(docnames)
			self.push("subscribe", docnames=docnames)
			self.here.subscriptions.update(docnames)

	def initialize_documents(self):
		subs = self.docs.subscribed
		self.subscribe(subs)
		for subname in subs:
			self.check(subname)

	def check(self, name, addr = []):
		addr = address.Address(addr).proto() # Make sure it's proto
		self.select(name)
		self.push("check", address=addr)

	def analyze(self, obj, objstring):
		''' 
			Apply a message as a piece of remote communication.
		'''
		obt = obj['type']
		if obt=='select':
			if not self.require("docname", obj): return
			self.there.selected = obj['docname']
		elif obt=='op':
			if not self.check_selected():return
			if not self.require("instructions", obj): return
			try:
				op = operation.Operation(instructions = obj['instructions'])
			except operation.ParseError:
				return self.error(453)
			# TODO: authorize
			if not op.applied(self.fdoc):
				try:
					op.apply(self.fdoc)
					print "Tree '%s' modified: '%s'" % (self.there.selected, self.fdoc.flatten())
					self.pool_push({
						"type":"op",
						"docname":self.there.selected,
						"value":op
					})
				except operation.OpApplyError:
					self.error(500) # General Local Error
			else:
				print "Op was already applied"
		elif obt=='check':
			# TODO - error testing
			if not self.check_selected():return
			if not self.require("address", obj):return
			addr = address.Address(obj['address'])
			sum = addr.resolve(self.fdoc.root).treesum
			self.select(self.there.selected)
			self.push("tsum",address=addr.proto(), value=sum)
		elif obt=='tsum':
			if not self.check_selected():return
			if not self.require("address", obj):return
			if not self.require("value", obj):return
			# Compare to our own treesum
			addr = address.Address(obj['address'])
			sum = addr.resolve(self.fdoc.root).treesum
			if sum != obj['value']:
				self.push("get", address=addr.proto(), depth=1)
		elif obt=='get':
			if not self.check_selected():return
			if not self.require("address", obj):return
			addr = address.Address(obj['address'])

			result = operation.FromStructure(self.fdoc.root, addr)

			self.select(self.there.selected)
			self.push("op", address = addr.proto(), instructions=result.proto()['instructions'])
		elif obt=='subscribe':
			if "docnames" not in obj:
				if not self.check_selected(): return
				obj[docnames] = [self.there.selected]
			for name in obj['docnames']:
				self.docs[name].subscribed = True
				self.there.subscriptions.add(name)
		elif obt=='unsubscribe':
			if "docnames" in obj:
				if len(obj['docnames']) > 0:
					for name in obj['docnames']:
						self.there.subscriptions.discard(name)
				else:
					self.there.subscriptions.clear()
			else:
				if not self.check_selected(): return
				self.there.subscriptions.discard(self.there.selected)
		elif obt=='error':
			print obj
		else:
			self.error(401) # Unknown Message Type

	def check_selected(self, is_loaded=True):
		if not self.there.selected:
			return self.error(405) # No document selected
		if is_loaded and not self.there.selected in self.docs:
			return self.error(404) # Document not found
		return True

	def require(self, arg, obj):
		if not arg in obj:
			self.error(452, 'Missing required argument: "%s"' % arg, arg)
			return False
		return True

	def error(self, num=500, details="", data=None):
		if num in errors and not details:
			details = errors[num]
		if data != None:
			self.push("error", code=num, details=details, data=data)
		else:
			self.push("error", code=num, details=details)

	@property
	def fdoc(self):
		''' Foreign selected document '''
		return self.docs[self.there.selected]

	@property
	def ldoc(self):
		''' Locally selected document '''
		return self.docs[self.here.selected]

	@property
	def id(self):
		if self._id == None:
			self._id = self.getunique("conn")
		return self._id
