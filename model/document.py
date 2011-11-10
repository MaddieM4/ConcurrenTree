from ConcurrenTree.model import ModelBase
from ConcurrenTree.model.operation import FromNode

class Document(ModelBase):
	''' Stores a node and tracks operations. '''

	def __init__(self, root, applied = []):
		self.root = root
		self.applied = set(applied)

	def apply(self, op):
		''' Apply an operation and track its application '''
		op.apply(self.root)
		self.applied.add(op.hash)

	def flatten(self):
		return self.root.flatten()

	def proto(self):
		''' Fully serializes document. Not a terribly fast function. '''
		return [FromNode(self.root, 0).proto(), self.applylist]

	@property
	def applylist(self):
		result = list(self.applied)
		result.sort()
		return result
