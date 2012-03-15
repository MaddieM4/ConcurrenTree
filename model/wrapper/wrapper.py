from ConcurrenTree.model.address import Address

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

	@property
	def value(self):
		return self.context.value

	def __repr__(self):
		return "w<%r>" % self.value
