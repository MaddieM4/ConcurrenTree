import json
import traceback

from ConcurrenTree.util.hasher import strict
from ConcurrenTree.model import operation, address
from peer import Peer
from errors import errors

nullbyte = "\x00"

class BCPConnection(object):
	''' A connection between two Peers '''

	def __init__(self, docs, auth, stream):
		''' 
			docs   - key/value access to docname/document pairs
			auth   - TBD
			stream - (input, output) tuple of Queues.
		'''
		Connection.__init__(self)
		self.poolsubs = {}
		self.buffer = ""

		self.docs = docs
		self.auth = auth
		self.stream = stream

		self.here = Peer()
		self.there = Peer()
		self.initialize_documents()


	def run(self):
		try:
			while 1:
				self.read()
				self.frame()
		except IOError:
			print "Connection closed"


	def initialize_documents(self):
		subs = self.docs.subscribed
		self.subscribe(subs)
		for subname in subs:
			self.check(subname)

	# STREAM INPUT

	def read(self):
		''' Reads raw data into the buffer '''
		if self.closed:
			raise IOError("Connection Closed")
		value = self.input.get()
		if value == "":
			self.close()
			raise IOError("Connection Closed")
		self.buffer += string

	def inject(self, string):
		self.input.put(string)

	def frame(self):
		''' Parses buffer into frames, as many as are in the buffer '''
		if nullbyte in buffer:
			length = buffer.index(nullbyte)
			try:
				self.recv_frame(buffer[:length])
			finally:
				self.buffer = buffer[length+1:]
				self.frame()

	def recv_frame(self, msg):
		''' Processes a raw frame before passing it to self.analyze '''

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

	# STREAM OUTPUT

	def send_frame(self, frame):
		if self.closed:
			raise IOError("Connection Closed")
		print "sending message:", frame
		self._send(frame)

	def _send(self, frame):
		self.output.put(frame)

	def send(self, msg):
		self.send_frame(strict(msg)+nullbyte)

	def push(self, msgtype, **kwargs):
		''' Convenience function for sending a frame '''
		kwargs['type'] = msgtype
		self.send(kwargs)

	# HIGH-LEVEL UTILITIES

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

	def check(self, name, addr = []):
		addr = address.Address(addr).proto() # Make sure it's proto
		self.select(name)
		self.push("check", address=addr)

	def sendop(self, name, addr = []):
		addr = address.Address(addr)

		result = operation.FromStructure(self.docs[name].root, addr)

		self.select(name)
		self.push("op", address = addr.proto(), instructions=result.proto()['instructions'])

	# MESSAGE ANALYSIS

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
					print "New hash: '%s'" % self.fdoc.hash
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
			sum = addr.resolve(self.fdoc.root).hash
			self.select(self.there.selected)
			self.push("tsum",address=addr.proto(), value=sum)
		elif obt=='tsum':
			if not self.check_selected():return
			if not self.require("address", obj):return
			if not self.require("value", obj):return
			# Compare to our own hash
			addr = address.Address(obj['address'])
			sum = addr.resolve(self.fdoc.root).hash
			if sum != obj['value']:
				self.sendop(self.there.selected, addr)
				self.push("get", address=addr.proto(), depth=1)
		elif obt=='get':
			if not self.check_selected():return
			if not self.require("address", obj):return
			self.sendop(self.there.selected, obj['address'])
		elif obt=='subscribe':
			if "docnames" not in obj:
				if not self.check_selected(): return
				obj[docnames] = [self.there.selected]
			for name in obj['docnames']:
				self.docs[name].subscribed = True
				self.pool_push({"type":"subscribe", "docname":name})
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
		''' Confirm that remotely selected docname exists '''
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
	def input(self):
		return self.stream[0]

	@property
	def output(self):
		return self.stream[1]

	def close(self):
		self.file.close()

	@property
	def closed(self):
		return self.file.closed

def QueuePair():
	from Queue import Queue
	A = Queue()
	B = Queue()
	return [(A, B), (B, A)]
