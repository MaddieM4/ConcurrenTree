from ejtp import frame, address as ejtpaddress, client as ejtpclient

from ConcurrenTree.model import document

import host_table
import message as mcp_message
import gear_validator

from sys import stderr
import json

class Gear(object):
	# Tracks clients in router, and documents.
	def __init__(self, storage, router, interface, encryptor=None, make_jack=True):
		self.storage = storage
		self.router = router

		# Components
		self.writer = mcp_message.Writer(self)
		self.reader = mcp_message.Reader(self)
		self.client_cache = ClientCache(self)
		self.client = setup_client(self, interface, make_jack)
		self.gv = gear_validator.GearValidator(self)
		
		self.hosts = host_table.HostTable(self.document('?host'))
		if encryptor != None:
                        self.hosts.crypto_set(interface, encryptor)

		self.storage.listen(self.on_storage_event)

	# On-the-fly document creation and retrieval (Get-or-create semantics)

	def document(self, docname):
		if docname in self.storage:
			# Return existing document
			return self.setdocsink(docname)
		else:
			# Create blank document
			self.storage[docname] = document.Document({})
			return self.setdocsink(docname)

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

	def send_full(self, docname, targets=[]):
		# Send a full copy of a document.
		doc = self.document(docname)
		self.writer.op(docname, doc.root.childop(), targets)

	# Callbacks for incoming data

	def rcv_callback(self, msg, client):
		self.reader.read(msg.ciphercontent, msg.addr)

	def on_storage_event(self, typestr, docname, data):
		# Callback for storage events
		if typestr == "op":
			self.writer.op(docname, data)

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

# EJTP client setup

def setup_client(gear, interface, make_jack):
	client = ejtpclient.Client(gear.router, interface, gear.client_cache, make_jack = make_jack)
	client.rcv_callback = gear.rcv_callback
	return client
