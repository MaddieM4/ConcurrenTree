from ConcurrenTree.model import ModelBase
from ConcurrenTree.util import hasher

class Node(ModelBase):
	''' Base class for all node types. '''

	# Stuff to be filled in by subclass

	@property
	def value(self):
		''' Immutable value used to generate keys '''
		raise NotImplementedError("Subclasses of Node must provide property 'value'")

	@property
	def key(self):
		''' 1-16 char long string '''
		raise NotImplementedError("Subclasses of Node must provide property 'key'")

	def flatten(self):
		''' Current value in Python types '''
		raise NotImplementedError("Subclasses of Node must provide function 'flatten'")

	def get(self, pos, key):
		''' Retrieves child at position "pos" and key "key" '''
		raise NotImplementedError("Subclasses of Node must provide function 'get'")

	def put(self, pos, obj):
		''' Set a child at pos, acquiring the key from the object's .key property '''
		raise NotImplementedError("Subclasses of Node must provide function 'put'")

	def delete(self, pos):
		''' Mark value[pos] as deleted '''
		raise NotImplementedError("Subclasses of Node must provide function 'delete'")

	def proto(self):
		ModelBase.proto(self)

	# Provided by base class

	def apply(self, op):
		''' For operations, instructions, and anything else that takes self.apply(tree) '''
		op.apply(self)

	def keysum(self, string):
		return hasher.key(string)

class UnsupportedInstructionError(Exception): pass

class Unputable(UnsupportedInstructionError): pass
class Ungetable(UnsupportedInstructionError): pass
class Undelable(UnsupportedInstructionError): pass

class ChildSet:
	def __init__(self, types=None):
		if types != None:
			try:
				self.types = tuple(types)
			except TypeError:
				self.types = (types,)
		else:
			self.types = None
		self.children = {}

	def insert(self, obj):
		self[obj.key] = obj

	def validtype(self, value):
		for i in self.types:
			if isinstance(value, i): return True
		return False

	def __setitem__(self, key, value):
		if self.types != None and not self.validtype(value):
			raise TypeError("Must be of one of the types: "+repr(self.types))
		if type(key) != str or len(key)<1 or len(key)>16:
			raise KeyError("Key must be a string of 1-16 characters")
		if key != value.key:
			raise ValueError("Key mismatch: cannot insert object with key %s as key %s" % (repr(value.key), repr(key)))
		self.children[key] = value

	def __getitem__(self, key):
		return self.children[key]

	def __delitem__(self, key):
		del self.children[key]

	def __iter__(self):
		return self.sorted.__iter__()

	def __len__(self):
		return __len__(self.children)

	@property
	def sorted(self):
		keys = self.children.keys()
		keys.sort()
		# always have "/single" win
		if "/single" in keys:
			keys.remove("/single")
			keys.append("/single")
		return keys

	@property
	def values(self):
		return [self[x] for x in self.sorted]

	@property
	def head(self):
		''' Child with highest key '''
		return self.values[-1]

	@property
	def tail(self):
		''' Child with lowest key '''
		return self.values[0]
