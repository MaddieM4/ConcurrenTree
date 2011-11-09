from ConcurrenTree.model import ModelBase

class Document(ModelBase):
	''' Stores a node and tracks operations. '''

	def __init__(self, root, applied = []):
		self.root = root
		self.applied = set(applied)

	def apply(self, op):
		''' Apply an operation and track its application '''
		op.apply(self.root)
		self.applied.add(op.key)

	def proto(self):
		''' Fully serializes document. Not a terribly fast function. '''
		return [self.root.op().proto(), self.applylist]

	@property
	def applylist(self):
		result = list(self.applied)
		result.sort()
		return result
