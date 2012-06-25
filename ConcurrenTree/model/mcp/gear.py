from ejtp import frame, address as ejtpaddress, client as ejtpclient
from ejtp.util.hasher import strict
from ejtp.util import crypto

from ConcurrenTree.model import document, operation
import ConcurrenTree.model.validation as validation

from sys import stderr
import json

class Gear(object):
	# Tracks clients in router, and documents.
	def __init__(self, storage, router):
		self.storage = storage
		self.router = router
		self.clients = {}
		self.structures = {}
		self.validation_queue = validation.ValidationQueue(filters = std_gear_filters)
		self.validation_queue.gear = self
		self.client_cache = ClientCache(self)

		self.storage.listen(self.on_storage_event)

	# Functional creators

	def client(self, interface, encryptor=None):
		iface = strict(interface)
		if encryptor != None:
			self.resolve_set(interface, encryptor)
		if not iface in self.clients:
			self.clients[iface] = ejtpclient.Client(self.router, interface, self.client_cache)
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

	# Basic messages

	def hello(self, target):
		# Send your EJTP encryption credentials to an interface
		for c in self.clients:
			client = self.clients[c]
			client.write_json(
				target,
				{
					'type':'hello',
					'interface':client.interface,
					'key':self.resolve(client.interface),
				},
				False,
			)

	def error(self, target, code=500, message="", data={}):
		self.send(target, {
			"type":"mcp-error",
			"code":code,
			"msg":message,
			"data":data
		})

	# Sender functions

	def send(self, iface, msg, senders=None):
		# Try multiple clients until it sends or fails
		# Will use self.clients unless variable "senders" is set.

		# Create a list of interfaces to try to send from.
		clients = senders or self.clients

		# Try until something sends without raising an exception.
		from ejtp.util.crashnicely import Guard
		for c in clients:
			if type(c) not in (str, unicode):
				c = strict(c)
			with Guard():
				self.clients[c].write_json(iface, msg)
				return
			print>>stderr, c,"->",iface,"failed"
		print>>stderr, "All clients failed to contact", iface

	def send_op(self, docname, op, targets=[], senders=[], structure=False):
		# Send an operation frame.
		# targets defaults to document.routes_to for every sender.
		# senders defaults to self.clients
		proto = op.proto()
		proto['docname'] = docname
		proto['structure'] = structure

		if not senders:
			senders = [json.loads(x) for x in self.clients]
		senders = [x for x in senders if self.can_write(x, docname)]

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
		self.send_op(docname, doc.root.childop(), targets, senders)

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
			self.validate_hello(content['interface'], content['key'])
		elif t == "op":
			docname = content['docname']
			op = operation.Operation(content['instructions'])
			self.validate_op(sender, docname, op)
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
		self.validation_queue.filter(request)

	def validate_pop(self):
		# Get the next item out of the queue
		return self.validation_queue.pop()

	def validate_op(self, author, docname, op):
		def callback(result):
			if result:
				self.storage.op(docname, op)
			else:
				print "Rejecting operation for docname: %r" % docname
		self.validate(
			validation.make("operation", author, docname, op, callback)
		)

	def validate_hello(self, author, encryptor):
		def callback(result):
			if result:
				self.resolve_set(author, encryptor)
			else:
				print "Rejecting hello from sender: %r" % encryptor
		self.validate(
			validation.make("hello", author, encryptor, callback)
		)

	def validate_load(self, author, docname):
		def callback(result):
			if result:
				self.send_full(docname, [author], [self.owner(docname)])
			else:
				print "Rejecting load request from sender: %r" % encryptor
		self.validate(
			validation.make("load", author, docname, callback)
		)

	# Utilities and conveninence functions.
	def owns(self, docname):
		# Returns bool for whether document owner is a client.
		owner = self.owner(docname)
		return owner in self.clients

	def sign(self, iface, obj):
		return ""
		#return self.clients[iface].sign(iface, obj)

	def sig_verify(self, iface, obj, sig):
		return True
		#for c in self.clients:
		#	try:
		#		return self.clients[c].sig_verify(iface, obj, sig)
		#	except KeyError:
		#		return False

	def hash(self, obj):
		return crypto.make(['sha1']).enc(strict(obj))

	def add_participant(self, docname, iface):
		# Adds person as a participant and sends them the full contents of the document.
		doc = self.document(docname)
		doc.add_participant(iface)

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
		iface = ejtpaddress.str_address(iface)
		encryptor = self.host(iface)['encryptor'].value
		if encryptor == None:
			raise IndexError("No encryptor information stored for interface %r" % iface)
		return encryptor[0]

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

class ClientCache(object):
	def __init__(self, gear):
		self.gear = gear

	def __getitem__(self, k):
		return self.gear.resolve(k)

	def __setitem__(self, k, i):
		self.gear.resolve_set(k, i)

# FILTERS

def filter_op_approve_all(queue, request):
	if isinstance(request, validation.OperationRequest):
		return request.approve()
	return request

def filter_op_is_doc_stored(queue, request):
	if isinstance(request, validation.OperationRequest):
		if not request.docname in queue.gear.storage:
			queue.gear.error(request.author, message="Unsolicited op")
			return request.reject()
	return request

def filter_op_can_write(queue, request):
	if isinstance(request, validation.OperationRequest):
		if not queue.gear.can_write(request.author, request.docname):
			queue.gear.error(request.author, message="You don't have write permissions.")
			return request.reject()
	return request

def filter_invite_accept_to_own(queue, request):
	# Auto-accept invites to documents you own
	if isinstance(request, validation.InvitationRequest):
		if queue.gear.owns(request.docname):
			return request.approve()
	return request


std_gear_filters = [
	filter_op_is_doc_stored,
	filter_op_can_write,
	filter_op_approve_all,
	filter_invite_accept_to_own,
]
