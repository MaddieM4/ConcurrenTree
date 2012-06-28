__all__ = [
	'address',
	'mcp',
	'instruction',
	'operation',
	'node',
	'document',
	'validation'
]

from ejtp.util import hasher

class ModelBase(object):
	def proto(self):
		''' Python protocol representation '''
		raise NotImplementedError("Subclasses of ModelBase must define self.proto()")

	def __str__(self):
		return hasher.strict(self.proto())

	@property
	def hash(self):
		return hasher.checksum(self.proto())
