from ejtp import frame, address as ejtpaddress, client as ejtpclient

from ConcurrenTree.model import document, operation
import ConcurrenTree.model.validation as validation

import host_table
import message as mcp_message

from sys import stderr
import json

class Gear(object):
	# Tracks clients in router, and documents.
	def __init__(self, storage, router, interface, encryptor=None):
		self.storage = storage
		self.router = router

		# Components
		self.writer = mcp_message.Writer(self)
		self.client_cache = ClientCache(self)
		self.client = setup_client(self, interface)
		
		self.hosts = host_table.HostTable(self.document('?host'))
		if encryptor != None:
                        self.hosts.crypto_set(interface, encryptor)

		self.validation_queue = validation.ValidationQueue(filters = std_gear_filters)
		self.validation_queue.gear = self

		self.storage.listen(self.on_storage_event)

	# Functional creators

	def document(self, docname):
		if docname in self.storage:
			# Return existing document
			return self.setdocsink(docname)
		else:
			# Create blank document
			self.storage[docname] = document.Document({})
			return self.setdocsink(docname)

	# Assistants to the functional creators

	def setdocsink(self, docname):
		# Set document operation sink callback and add owner with full permissions
		doc = self.storage[docname]
		if doc.own_opsink:
			# Prevent crazy recursion
			doc.own_opsink = False

			# Add owner with full permissions
			try:
				owner = json.loads(document.owner(docname))
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

	# Sender functions

	def send(self, iface, msg):
		from ejtp.util.crashnicely import Guard
		with Guard():
			self.client.write_json(iface, msg)
			return
		print>>stderr, self.interface,"->",iface,"failed"

	def send_op(self, docname, op, targets=[]):
		# Send an operation frame.
		# targets defaults to document.routes_to for every sender.
		proto = op.proto()
		proto['type'] = 'mcp-op'
		proto['docname'] = docname

		targets = targets or self.document(docname).routes_to(self.interface)

		for i in targets:
			self.send(i, proto)

	def send_full(self, docname, targets=[]):
		# Send a full copy of a document.
		doc = self.document(docname)
		self.send_op(docname, doc.root.childop(), targets)

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
		if t == "mcp-hello":
			self.validate_hello(content['interface'], content['key'])
		elif t == "mcp-op":
			docname = content['docname']
			op = operation.Operation(content['instructions'])
			self.validate_op(sender, docname, op)
		elif t == "mcp-error":
			print "Error from:", sender, ", code", content["code"]
			print repr(content['msg'])
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
				self.hosts.crypto_set(author, encryptor)
			else:
				print "Rejecting hello from sender: %r" % encryptor
		self.validate(
			validation.make("hello", author, encryptor, callback)
		)

	# Utilities and conveninence functions.
	@property
	def interface(self):
		return self.client.interface

	def owns(self, docname):
		# Returns bool for whether document owner is a client.
		owner = document.owner(docname)
		return owner == ejtpaddress.str_address(self.interface)

	def add_participant(self, docname, iface):
		# Adds person as a participant, does not send them data though.
		doc = self.document(docname)
		doc.add_participant(iface)

	def can_read(self, iface, docname):
		# Returns whether an interface can read a document.
		# If iface == None, assumes self.interface
		if self.owns(docname) or docname[0] == "?":
			return True

		if iface == None:
			iface = self.interface

		doc = self.document(docname)
		return doc.can_read(iface)

	def can_write(self, iface, docname):
		# Returns whether an interface can write a document.
		# If iface == None, assumes self.interface
		if self.owns(docname) or docname[0] == "?":
			return True

		if iface == None:
			iface = self.interface

		doc = self.document(docname)
		return doc.can_write(iface)

class ClientCache(object):
	def __init__(self, gear):
		self.gear = gear

	def __getitem__(self, k):
		return self.gear.hosts.crypto_get(k)

	def __setitem__(self, k, i):
		self.gear.hosts.crypto_set(k, i)

# FILTERS

def filter_op_approve_all(queue, request):
	if isinstance(request, validation.OperationRequest):
		return request.approve()
	return request

def filter_op_is_doc_stored(queue, request):
	if isinstance(request, validation.OperationRequest):
		if not request.docname in queue.gear.storage:
			queue.gear.writer.error(request.author, message="Unsolicited op")
			return request.reject()
	return request

def filter_op_can_write(queue, request):
	if isinstance(request, validation.OperationRequest):
		if not queue.gear.can_write(request.author, request.docname):
			queue.gear.writer.error(request.author, message="You don't have write permissions.")
			return request.reject()
	return request

std_gear_filters = [
	filter_op_is_doc_stored,
	filter_op_can_write,
	filter_op_approve_all,
]

# EJTP client setup

def setup_client(gear, interface):
	client = ejtpclient.Client(gear.router, interface, gear.client_cache)
	client.rcv_callback = gear.rcv_callback
	return client
