from ConcurrenTree.util import crypto
from ConcurrenTree.util.hasher import strict
from ConcurrenTree.model import document, operation
from ConcurrenTree.model.validation import invitation, queue
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
		self.structures = {}
		self.validation_queue = queue.ValidationQueue()

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
		# Set document operation sink callback and add owner with full permissions
		doc = self.storage[docname]
		if doc.own_opsink:
			# Prevent crazy recursion
			doc.own_opsink = False

			# Add owner with full permissions
			try:
				owner = json.loads(self.owner(docname))
				self.add_participant(docname, owner)
			except ValueError:
				pass # No author could be decoded

			# Define opsink callback
			def opsink(op):
				if self.can_write(None, docname):
					self.storage.op(docname, op)
				else:
					print "Not applying op, you don't have permission"

			# Set document to use the above function
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

	def invite(self, target, docname):
		# Invite an interface to try to load a docname
		self.send(target, {"type":"invite", "docname":docname})

	def load(self, target, docname, accepts=[]):
		# Requests a full structural op for a document.
		# accepts is a list of interfaces the structure would be accepted from
		# The owner is always inferred whether present or not
		self.send(target, {"type":"load", "docname":docname, "accepts":accepts})

	def error(self, target, code=500, message=""):
		self.send(target, {"type":"error", "code":code, "contents":message})

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

	def send_op(self, docname, op, targets=[], senders=[], structure=False):
		# Send an operation message.
		# targets defaults to document.routes_to for every sender.
		# senders defaults to self.clients
		proto = op.proto()
		proto['docname'] = docname
		proto['version'] = 0
		proto['structure'] = structure

		if not senders:
			senders = [json.loads(x) for x in self.clients]
		senders = [x for x in senders if self.can_write(x, docname)]

		if structure:
			# Sign it
			sigs = {}
			for s in senders:
				sigs[s] = self.sign(proto, s)
			proto['sigs'] = sigs

		if targets:
			for i in targets:
				self.send(i, proto, senders)
		else:
			for c in senders:
				client = self.clients[strict(c)]
				if not targets:
					targets = self.document(docname).routes_to(c)
				for t in targets:
					self.send(t, proto, [c])

	def send_full(self, docname, targets=[], senders=[]):
		# Send a full copy of a document.
		doc = self.document(docname)
		self.send_op(docname, doc.root.childop(), targets, senders, structure=True)

	# Callbacks for incoming data

	def rcv_callback(self, msg, client):
		self.rcv_json(msg.ciphercontent, msg.addr)

	def rcv_json(self, content, sender = None):
		try:
			content = json.loads(content)
		except:
			print "COULD NOT PARSE JSON:"
			print content
		t = content['type']
		if t == "hello":
			self.resolve_set(content['interface'], content['key'])
		elif t == "dm":
			print "Direct message from", sender
			print repr(content['contents'])
		elif t == "op":
			docname = content['docname']

			# Check if we have interest in this op
			if not docname in self.storage:
				print "Dropping op for unwanted docname %r" % docname
				return self.error(sender, message="Unsolicited op")

			# Permissions
			validsig = False
			if content['structure'] == True:
				# check for any valid signature
				sigs = content['sigs']
				sigless = dict(content)
				del sigless['sigs']
				for iface in sigs:
					if self.sig_verify(iface, sigless, sigs[iface]):
						validsig=True
						self.structure[docname][iface] = content

			# Check for sender's write permission
			if not self.can_write(sender, docname) and not validsig:
				return self.error(sender, message="You don't have write permissions.")
			op = operation.Operation(content['instructions'])
			self.storage.op(docname, op)
		elif t == "invite":
			docname = content['docname']
			self.validate_invitation(sender, docname)
		elif t == "load":
			docname, accepts = content['docname'], content['accepts']
			# New logic
			owner = self.owner(docname)
			if owner in self.clients:
				# You own the document
				self.send_full(docname, [sender], [owner])
			else:
				# Check cache
				if docname in self.structures:
					accepts.append(owner)
					for i in accepts:
						if i in self.structures[docname]:
							# Send cached structure
							msg = self.structures[docname][i]
							return self.send(sender, msg)
				# Silently drop for now
				# self.error(sender, message="No cached structure for %r" % docname)
				return
		elif t == "error":
			print "Error from:", sender, ", code", content["code"]
			print repr(content['contents'])
		else:
			print "Unknown msg type %r" % t

	def on_storage_event(self, typestr, docname, data):
		# Callback for storage events
		if typestr == "op":
			self.send_op(docname, data)

	# Validation stuff.

	def validate(self, request):
		self.validation_queue.add(request)

	def validate_pop(self):
		# Get the next item out of the queue
		return self.validation_queue.pop()

	def validate_invitation(self, author, docname):
		def callback(result):
			if result:
				self.document(docname)
				self.load(author, docname)
			else:
				print "Ignoring invitation to document %r" % docname
		self.validate(
			invitation.Invitation(author, docname, callback)
		)

	# Utilities and conveninence functions.
	def sign(self, iface, obj):
		return self.clients[iface].sign(iface, obj)

	def sig_verify(self, iface, obj, sig):
		for c in self.clients:
			try:
				return self.clients[c].sig_verify(iface, obj, sig)
			except KeyError:
				return False

	def hash(self, obj):
		return crypto.make(['sha1']).enc(strict(obj))

	def add_participant(self, docname, iface):
		# Adds person as a participant and sends them the full contents of the document.
		doc = self.document(docname)
		doc.add_participant(iface)
		self.invite(iface, docname)

	def owner(self, docname):
		# Returns the owner string in a docname
		return docname.partition("\x00")[0]

	def mkname(self, iface, name):
		return strict(iface)+"\x00"+name

	def can_read(self, iface, docname):
		# Returns whether an interface can read a document.
		# If iface == None, tests all client interfaces.
		if self.owner(docname) == strict(iface) or docname[0] == "?":
			return True

		if iface == None:
			for c in self.clients:
				if self.can_read(json.loads(c), docname):
					return True
			return False

		doc = self.document(docname)
		return doc.can_read(iface)

	def can_write(self, iface, docname):
		# Returns whether an interface can write a document.
		# If iface == None, tests all client interfaces.
		if self.owner(docname) == strict(iface) or docname[0] == "?":
			return True

		if iface == None:
			for c in self.clients:
				if self.can_write(json.loads(c), docname):
					return True
			return False

		doc = self.document(docname)
		return doc.can_write(iface)

	def resolve(self, iface):
		# Return the cached encryptor proto for an interface.
		iface = strict(iface)
		return self.host(iface)['encryptor'].value[0]

	def resolve_self(self):
		# Encryptor protos for each of your clients.
		result = {}
		for iface in self.clients:
			if iface in self.host_table['content']:
				result[iface] = self.resolve(iface)
			else:
				result[iface] = None
		return result

	def resolve_set(self, iface, key, sigs = []):
		# Set the encryptor proto for an interface in the cache table.
		iface = strict(iface)
		value = [key, sigs]
		self.host(iface)['encryptor'] = value

	def host(self, iface):
		default = {
			"owner": None,
			"encryptor": None
		}
		if not iface in self.host_table['content']:
			self.host_table['content'][iface] = default
		return self.host_table['content'][iface]

	@property
	def host_table(self):
		# Cached host information
		return self.document("?host").wrapper()
