__all__ = [
	'address',
	'document',
	'instruction',
	'mcp',
	'node',
	'operation',
	'user',
	'validation',
	'wrapper',
]

from ejtp.util import hasher
import os.path

class ModelBase(object):
	def proto(self):
		''' Python protocol representation '''
		raise NotImplementedError("Subclasses of ModelBase must define self.proto()")

	def __str__(self):
		return hasher.strict(self.proto())

	@property
	def hash(self):
		return hasher.checksum(self.proto())

def file(*subpaths):
	return os.path.join(__path__[0], *subpaths)
