from ConcurrenTree.model.address import Address
from ConcurrenTree.util.hasher import strict

class Wrapper(object):
	# Lets you treat nodes directly like the objects they
	# represent, with implementation details abstracted
	# away (other than initialization).
	def __init__(self, node, opsink):
		# Takes a node object, and a callback.
		# The callback should accept an op.
		self.node = node
		self.opsink = opsink
		self.context = self.node.context()

	def childsink(self, address):
		# A simple mechanism to ripple ops to the top level.
		# You should use this as the default opsink when creating child wrappers.
		address = Address(address)
		def sink(op):
			self.opsink(address+op)
		return sink

	def childnode(self, node, address):
		# Create a child wrapper based on a childsink
		from ConcurrenTree.model.wrapper import make
		return make(node, self.childsink(address))

	@property
	def value(self):
		return self.context.value

	@property
	def strict(self):
		# The strict string rep of self.value
		return strict(self.value)

	def __repr__(self):
		return "w<%r>" % self.value
