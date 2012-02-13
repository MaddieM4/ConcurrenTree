from ConcurrenTree.model import ModelBase
import re
import json

# Internal storage format: assorted strings and (int, str) tuples.

class Address(ModelBase):
	''' Address format: [4,"hello"," dolly"] '''

	def __init__(self, target=[]):
		if type(target)==list:
			self.layers = []
			self.parse(target)
		elif isinstance(target, Address):
			self.layers = list(target.layers) # copies data, not ref
		elif type(target) in (str, unicode):
			self.layers = json.loads(target)
		else:
			raise TypeError("Expected list or address.Address, got "+str(type(target)))

	def parse(self, l):
		''' Reads and processes a list '''
		pos = None
		progress = list(self.layers)
		for i in expand(l):
			if type(i)==int:
				if pos==None:
					pos = i
				else:
					raise ValueError("Address list cannot contain consecutive ints")

			elif type(i) in (str, unicode):
				if pos==None:
					progress.append(i)
				else:
					progress.append((pos,i))
					pos = None
			else:
				raise TypeError("Address cannot parse element %s" % str(i))
		if pos == None:
			self.layers = progress
		else:
			raise ValueError("Address list cannot end with int")

	def resolve(self, tree):
		x = tree
		error = 0
		for i in self.layers:
			error += 1
			if type(i) in (str, unicode):
				i = (len(x), i)
			x = x.get(i[0],i[1])
		return x


	def proto(self):
		return expand(self.layers)

	def append(self, value):
		''' Value may be a 2-tuple or a string '''
		self.layers.append(value)

	def prepend(self, value):
		''' Value may be a 2-tuple or a string '''
		self.layers.insert(0,value)

	def jump(self, pos, max, key):
		if pos==max:
			return key
		else:
			return pos, key

	@property
	def parent(self):
		''' Address for the parent node of self's node '''
		if self.layers == []:
			raise ValueError("Root has no parent")
		new = Address(self) # copy
		new.layers = new.layers[:-1]
		return new

	def position(self, root):
		''' Position of final jump '''
		tail = self.layers[-1]
		if type(tail) == tuple:
			return tail[0]
		else:
			return len(self.parent.resolve(root))

	# Plumbing

	def __len__(self):
		''' Number of hops '''
		return len(self.layers)

	def __eq__(self, other):
		return type(self)==type(other) and self.layers == other.layers

	def __add__(self, other):
		new = Address(self) # Copy layers
		new += other
		return new

	def __iadd__(self, other):
		if type(other) == list:
			self.parse(other)
		elif isinstance(other, Address):
			self.layers += other.layers
		else:
			self += [other]
		return self

	def __radd__(self, other):
		if type(other) == list:
			return Address(other) + self
		else:
			return [other] + self

	__hash__ = None

	def __repr__(self):
		classname = repr(self.__class__).split()[1]
		return "<%s instance %s at %s>" % (classname, str(self), hex(long(id(self)))[:-1])

def expand(l):
	''' Expands all sub-lists '''
	result = []
	for i in l:
		if type(i) in (tuple, list):
			result += list(i)
		else:
			result.append(i)
	return result
