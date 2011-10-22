from ConcurrenTree.model import ModelBase

class Node(ModelBase):
	''' Base class for all node types. '''

	@property
	def value(self):
		raise NotImplementedError("Subclasses of Node must provide property 'value'")

	@property
	def key(self):
		raise NotImplementedError("Subclasses of Node must provide property 'key'")

	@property
	def flatten(self):
		raise NotImplementedError("Subclasses of Node must provide function 'flatten'")
