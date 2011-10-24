__all__ = ['address', 'bcp', 'instruction', 'operation', 'tree']

from ConcurrenTree.util import hasher

class ModelBase:
	def proto(self):
		''' Python protocol representation '''
		raise NotImplementedError("Subclasses of ModelBase must define self.proto()")

	def __str__(self):
		return hasher.strict(self.proto())

	@property
	def hash(self):
		return hasher.checksum(self.proto())
