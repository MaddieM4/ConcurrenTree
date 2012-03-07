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
