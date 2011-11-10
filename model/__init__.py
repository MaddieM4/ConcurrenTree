__all__ = ['address', 'bcp', 'instruction', 'operation', 'node', 'document']

from ConcurrenTree.util import hasher

class ModelBase(object):
	def proto(self):
		''' Python protocol representation '''
		raise NotImplementedError("Subclasses of ModelBase must define self.proto()")

	def __str__(self):
		return hasher.strict(self.proto())

	@property
	def hash(self):
		return hasher.checksum(self.proto())
