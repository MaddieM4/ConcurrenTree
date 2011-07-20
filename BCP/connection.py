import Queue
import json
import traceback

from BCP.peer import Peer
from BCP.errors import errors

nullbyte = "\x00"

class Connection:
	''' A connection between two Peers '''
	def __init__(self, docHandler, authHandler, queue, extensions = {}, log=[]):
		self.docs = docHandler
		self.auth = authHandler
		self.queue = queue # must be a BCP.doublequeue
		self.extensions = extensions
		self.logtypes = log

		self.buffer = ""
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
		return False

	def exchange(self):
		flag = True
		while flag:
			flag = self.recv() or self.send()

	def feed(self, string=""):
		''' Read a string into the buffer and process it '''
		#print "BCP.Connection receiving %s:" % type(string), string
		if type(string)==int:
			# close this connection
			self.close(string)
			return
		self.buffer += string
		if nullbyte in self.buffer:
			length = self.buffer.index(nullbyte)
			msg, self.buffer = self.buffer[:length], self.buffer[length+1:]
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
			self.feed()

	def extend(self, name, callback):
		self.extensions[name] = callback

	def is_extended(self, name):
		return name in self.extensions

	def unextend(self, name):
		del self.extensions[name]

	def push(self, msgtype, **kwargs):
		kwargs['type'] = msgtype
		self.queue.server_push(json.dumps(kwargs))

	def select(self, docname):
		if self.here.selected != docname:
			self.push("select", docname=docname)

	def analyze(self, obj, objstring):
		if not "type" in obj:
			self.error(452, 'Missing required argument: "type"')
			return
		obt = obj['type']
		# log
		if self.logtypes == "*" or obt in self.logtypes:
			obj["selected"] = self.there.selected
			self.log.put(obj)
		# Check extensions for override on type
		if obt in self.extensions:
			return self.extensions[obt](obj)
		elif "*" in self.extensions:
			# Global extension on all message types
			return self.extensions["*"](obj)
		else:
			# No extension, do normal stuff
			self.apply(obj, objstring)

	def apply(self, obj, objstring):
		''' 
			Apply a message as a piece of remote communication.
		'''
		obt = obj['type']
		if obt=='select':
			self.there.selected = obj['docname']
		elif obt=='op':
			op = operation.Operation(protostring=objstring)
			op.apply(self.docs[self.there.selected])
		elif obt=='ad':
			if not 'hash' in obj:
				self.error(452, 'Missing required argument: "hash"')
			elif not obj['hash'] in self.here.ops:
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
		else:
			self.error(401) # Unknown Message Type

	def error(self, num=500, details=""):
		if num in errors and not details:
			details = errors[num]
		self.push("error", code=num, details=details)

	def close(self, error=0):
		self.closed = True
