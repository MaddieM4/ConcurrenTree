from ConcurrenTree.model import ModelBase
from ConcurrenTree.model.node import make
from ConcurrenTree.model.operation import Operation, FromNode

class Document(ModelBase):
	''' Stores a node and tracks operations. '''

	def __init__(self, root, applied = []):
		self.root = make(root)

		self.applied = set(applied)
		self.routing

	def apply(self, op, track=True):
		''' Apply an operation and track its application '''
		op.apply(self.root)
		if track:
			self.applied.add(op.hash)

	def is_applied(self, op):
		return op.hash in self.applied

	def load(self, json):
		self.apply(Operation(json[0]), False)
		self.applied = set(json[1])

	def opsink(self, op):
		print op.proto()
		self.apply(op)

	def wrapper(self):
		return self.root.wrapper(self.opsink)

	def flatten(self):
		return self.root.flatten()

	def proto(self):
		''' Fully serializes document. Not a terribly fast function. '''
		return [FromNode(self.root, 0).proto(), self.applylist]

	def pretty(self):
		# Pretty-prints the JSON content
		import json
		print json.dumps(self.flatten(), indent=4)

	@property
	def applylist(self):
		result = list(self.applied)
		result.sort()
		return result

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

	def add_participant(self, iface):
		from ConcurrenTree.util.hasher import strict
		routes = self.routing
		iface = strict(iface)
		if not iface in routes:
			routes[iface] = {}
