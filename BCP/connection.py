import Queue
from json.decoder import JSONDecoder as Decoder
from json import dumps

from BCP.peer import Peer

class Connection:
	''' A connection between two Peers '''
	def __init__(self, docHandler, authHandler, queue, extensions = {}, log=[]):
		self.docs = docHandler
		self.auth = authHandler
		self.queue = queue # must be a BCP.doublequeue
		self.extensions = extensions
		self.logtypes = log

		self.buffer = ""
		self.outbuffer = ""
		self.decoder = Decoder()
		self.log = Queue.Queue()
		self.here = Peer()
		self.there = Peer()
		self.closed = False

	def recv(self):
		''' 
			Returns True if there was data to read,
			False if there was a timeout.
		'''
		if self.closed: return False
		try:
			self.feed(self.queue.server_pull(timeout=0))
			return True
		except Queue.Empty:
			return False

	def send(self):
		if self.closed: return False
		if self.outbuffer:
			self.queue.server_push(self.outbuffer)
			self.outbuffer = ""
			return True
		else:
			return False

	def exchange(self):
		flag = True
		while flag:
			flag = self.recv() or self.send()

	def feed(self, string=""):
		''' Read a string into the buffer and process it '''
		if type(string)==int:
			# close this connection
			self.close()
			return
		self.buffer += string
		try:
			obj, length = self.decoder.raw_decode(self.buffer)
			msg, self.buffer = self.buffer[:length], self.buffer[length:]
			self.dedict(obj, msg)
			self.feed()
		except:
			pass

	def extend(self, name, callback):
		self.extensions[name] = callback

	def unextend(self, name):
		del self.extensions[name]

	def push(self, msgtype, **kwargs):
		kwargs['type'] = msgtype
		outbuffer += dumps(kwargs)

	def select(self, docname):
		if self.here.selected != docname:
			self.push("select", docname=docname)

	def dedict(self, obj, objstring):
		''' 
			The part of the Peer class that analyzes the
			remote communication.
		'''
		obt = obj['type']
		if obt in self.logtypes:
			self.log.put((obj, self.there.selected))
		if obt in self.extensions:
			self.extensions[obt](obj)
			return
		if obt=='select':
			self.there.selected = obj['docname']
		elif obt=='op':
			op = operation.Operation(protostring=objstring)
			op.apply(self.docs[self.there.selected])
		elif obt=='ad':
			if not obj['hash'] in self.here.ops:
				self.select(self.there.selected)
				self.push("getop", hash=obj['hash'])
		elif obt=='getop':
			op = self.docs[self.there.selected].operations[obj['hash']]
			self.outbuffer += str(op)
		elif obt=='check':
			pass
		elif obt=='thash':
			pass
		elif obt=='get':
			pass
		elif obt=='era':
			pass
		elif obt=='subscribe':
			if "subtype" not in obj or obj['subtype']=="live":
				# live subscription
				for name in obj['docnames']:
					self.there.subscriptions[name] = ("live")
			elif obj['subtype']=="notify":
				# notify subscription (ad-only)
				for name in obj['docnames']:
					self.there.subscriptions[name] = ("notify")
			elif obj['subtype']=="marked":
				# notify subscription (read/unread)
				for name in obj['docnames']:
					self.there.subscriptions[name] = ("marked", 0) # TODO use tree hash

		elif obt=='unsubscribe':
			if "docnames" in obj and len(obj['docnames']) > 0:
				for name in obj['docnames']:
					del self.there.subscriptions[name]
			else:
				self.there.subscriptions.clear()


	def close(self):
		self.closed = True
