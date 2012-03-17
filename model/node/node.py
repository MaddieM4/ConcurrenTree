from ConcurrenTree.model import ModelBase, event
from ConcurrenTree.util import hasher
from ConcurrenTree.model.address import Address

class Node(ModelBase):
	''' Base class for all node types. '''

	def __init__(self):
		self.evgrid = event.EventGrid(['insert','delete',
			'childinsert', 'childdelete'])

	# Stuff to be filled in by subclass:

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

	def _get(self, pos, key):
		''' Retrieves child at position "pos" and key "key" '''
		raise NotImplementedError("Subclasses of Node must provide function 'get'")

	def _put(self, pos, obj):
		''' Set a child at pos, acquiring the key from the object's .key property '''
		raise NotImplementedError("Subclasses of Node must provide function 'put'")

	def _delete(self, pos):
		''' Mark value[pos] as deleted '''
		raise NotImplementedError("Subclasses of Node must provide function 'delete'")

	# Properties to be defined by subclass:

		# self._deletions - list of deleted positions
		# self._children  - list of node.ChildSets

		# If you define self.deletions and self.children, respectively,
		# self._deletions and self._children will not be used externally.

	# Provided by base class:

	def get(self, pos, key):
		return self._get(pos, key)

	def put(self, pos, n):
		self._put(pos, n)
		n.register('insert', lambda grid, label: self.evgrid.happen('childinsert'))
		n.register('delete', lambda grid, label: self.evgrid.happen('childdelete'))
		self.evgrid.happen('insert')

	def delete(self, pos):
		self._delete(pos)
		self.evgrid.happen('delete')

	def register(self, *args):
		self.evgrid.register(*args)

	@property
	def deletions(self):
		''' Return a compressed list of deletions '''
		return compress_deletions(self._deletions)

	@property
	def children(self):
		''' Return a dict of position: childhashes, each of which is a dict of key:hash. '''
		positions = {}
		for p in range(len(self._children)):
			if self._children[p]:
				positions[p] = self._children[p].proto()
		return positions

	def proto(self):
		return [self.key, self.children, self.deletions]

	def apply(self, op):
		''' For operations, instructions, and anything else that takes self.apply(tree) '''
		op.apply(self)

	def keysum(self, string):
		return hasher.key(string)

	def resolve(self, addrlist):
		''' Map overrides this '''
		addrlist = list(addrlist)
		if len(addrlist) == 0:
			return self
		if type(addrlist[0])==int:
			pos = addrlist[0]
			key = addrlist[1]
			return self.get(pos, key).resolve(addrlist[2:])
		else:
			pos = len(self)
			key = addrlist[0]
			return self.get(pos, key).resolve(addrlist[1:])

	# High level imports

	def context(self, *args):
		from ConcurrenTree.model import context
		return context.make(self, *args)

	def wrapper(self, *args):
		from ConcurrenTree.model import wrapper
		return wrapper.make(self, *args)

	def op(self, pos, addr = []):
		from ConcurrenTree.model import operation
		addr = Address(addr)
		return addr + operation.FromNode(self, pos)

	def childop(self):
		from ConcurrenTree.model import operation
		return operation.FromChildren(self)

class UnsupportedInstructionError(Exception): pass

class Unputable(UnsupportedInstructionError): pass
class Ungetable(UnsupportedInstructionError): pass
class Undelable(UnsupportedInstructionError): pass

class ChildSet:
	def __init__(self, types=None, limit=None):
		if types != None:
			try:
				self.types = tuple(types)
			except TypeError:
				self.types = (types,)
		else:
			self.types = None
		self.limit = limit
		self.children = {}

	def insert(self, obj):
		self[obj.key] = obj

	def validtype(self, value):
		for i in self.types:
			if isinstance(value, i): return True
		return False

	def proto(self):
		result = {}
		for i in self:
			result[i] = self[i].hash
		return result

	def __setitem__(self, key, value):
		if self.types != None and not self.validtype(value):
			raise TypeError("Must be of one of the types: "+repr(self.types))
		if type(key) != str or len(key)<1 or len(key)>16:
			raise KeyError("Key must be a string of 1-16 characters")
		if key != value.key:
			raise ValueError("Key mismatch: cannot insert object with key %s as key %s" % (repr(value.key), repr(key)))
		if self.limit != None and key != self.limit:
			raise ValueError("Childset only accepts key "+self.limit)
		if key in self:
			print "Warning: clobbering over key "+repr(key)
		self.children[key] = value

	def __contains(self, key):
		return key in self.children

	def __getitem__(self, key):
		return self.children[key]

	def __delitem__(self, key):
		del self.children[key]

	def __iter__(self):
		return self.sorted.__iter__()

	def __len__(self):
		return len(self.children)

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

def enumerate_deletions(l):
	''' Takes a list of bools and return a list of the positions in l where l[i] is true '''
	return [i for i in range(len(l)) if l[i]]

def compress_deletions(l):
	''' Takes a list of deleted positions, returns list of ints and ranges '''
	l.sort()
	stream = []
	start = None
	current = None
	for p in l:
		if start == None:
			start = p
			current = p
		else:
			if p == current + 1:
				current = p
			else:
				# append to stream
				if start == current:
					stream.append(start)
				else:
					stream.append((start, current))
				start = p
				current = p
	if start != None:
		if start == current:
			stream.append(start)
		else:
			stream.append((start, current))

	return stream

def ce_deletions(l):
	''' Enumerate and compress a deltetion list in one step. '''
	return compress_deletions(enumerate_deletions(l))
