from ConcurrenTree.model import ModelBase
from ConcurrenTree.model.node import make
from ConcurrenTree.model.operation import Operation, FromNode

from ConcurrenTree.util.hasher import strict

class Document(ModelBase):
	''' Stores a node and tracks operations. '''

	def __init__(self, root={}, applied = []):
		self.root = make(root)

		self.own_opsink = True
		self.private = dict({
			'ops':{
				'known'  : {},
				'applied': {}
				# MCP negotiation data should go here too
			}
		})
		for ophash in applied:
			self.applied[ophash] = True;
		self.routing
		self.content

	def apply(self, op, track=True):
		''' Apply an operation and track its application '''
		if self.is_applied(op):
			return
		op.apply(self.root)
		if track:
			ophash = op.hash # cache
			if not ophash in self.applied:
				self.applied[ophash] = True
			if not ophash in self.private['ops']['known']:
				self.private['ops']['known'][ophash] = op.proto()

	def is_applied(self, op):
		return op.hash in self.applied

	def load(self, json):
		self.apply(Operation(json[0]), False)
		self.private = json[1]

	def opsink(self, op):
		#print op.proto()
		self.apply(op)

	def wrapper(self):
		return self.root.wrapper(self.opsink)

	def flatten(self):
		return self.root.flatten()

	def proto(self):
		''' Fully serializes document. Not a terribly fast function. '''
		return [self.root.childop().proto(), self.private]

	def pretty(self):
		# Pretty-prints the JSON content
		print self.wrapper().pretty()

	@property
	def applied(self):
		return self.private['ops']['applied']

	@applied.setter
	def applied(self, new_applied):
		self.private['ops']['applied'] = new_applied

	# Metadata properties

	def prop(self, key, default = {}):
		# Returns a wrapped top-level property
		wrap = self.wrapper()
		if not key in self.root:
			wrap[key] = default
		return wrap[key]

	@property
	def content(self):
		return self.prop("content")

	@property
	def routing(self):
		return self.prop("routing")

	@property
	def version(self):
		# Document format version, not related to blockchain
		return self.prop("version", 0)

	@property
	def consensus(self):
		return self.prop("consensus", {
			"read":{},
			"write":{}
		})

	@property
	def permissions(self):
		return self.prop("permissions", {
			"universal": {
				"read":{},
				"write":{},
				"read-meta":{},
				"write-meta":{},
				"meta-meta":{}
			}
		})

	# Advanced properties and metadata functions

	@property
	def participants(self):
		# All routing sends and recieves
		if not "routing" in self.root:
			return []
		parts = set()
		routes = self.routing
		for sender in routes:
			parts.add(sender)
			for reciever in routes[sender]:
				parts.add(reciever.strict)
		import json
		return [json.loads(s) for s in parts]

	def add_participant(self, iface, permissions=[], can_read=True, can_write=True):
		routes = self.routing
		striface = strict(iface)
		if can_read:
			permissions.append(("universal", "read"))
		if can_write:
			permissions.append(("universal", "write"))
		for cat, name in permissions:
			self.add_permission(iface, cat, name)
		if not iface in routes:
			routes[striface] = {}

	def has_permission(self, iface, category, name):
		# If self.permissions does not already exist, will always return false.
		if "permissions" not in self.root:
			return False
		perm = self.permissions[category][name]
		return strict(iface) in perm

	def add_permission(self, iface, category, name):
		self.permissions[category][name][strict(iface)] = True

	def remove_permission(self, iface, category, name):
		del self.permissions[category][name][strict(iface)]

	def can_read(self, iface):
		return self.has_permission(iface, "universal", "read")

	def can_write(self, iface):
		return self.has_permission(iface, "universal", "write")

	def routes_to(self, iface):
		# Returns which interfaces this interface sends to.
		return [x for x in self.routes_to_unfiltered(iface) if self.can_read(x)]

	def routes_to_unfiltered(self, iface):
		# Does not take read permissions into account.
		istr = strict(iface)
		if istr in self.routing and len(self.routing[istr]) > 0:
			result = set()
			for target in self.routing[istr]:
				result.add(target)
			import json
			return [json.loads(s) for s in result]
		else:
			parts = self.participants
			if iface in parts:
				parts.remove(iface)
			return parts
