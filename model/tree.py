from ConcurrenTree.model import ModelBase
from ConcurrenTree.util.hasher import key, sum, checksum

import operation
from address import Address, BeyondFlatError

class Tree(ModelBase):
	def __init__(self, value=""):
		''' Do not manipulate children externally. Use class methods. '''
		self._value = value
		self._length = len(value)
		self._deletions = [False] * len(self)
		self._children = []
		for i in range(len(self)+1):
			self._children.append(dict())

	def insert(self, pos, value, override=False):
		''' Insert a child to the tree with string "value" at position "pos" '''
		result = Tree(value)
		self.insert_tree(pos, result, override)
		return result

	def insert_tree(self, pos, obj, override=True):
		''' Insert an object as a child tree '''
		if not obj.key in self._children[pos] or override:
			self._children[pos][obj.key] = obj

	def delete(self, pos):
		''' Mark a character in a tree as deleted '''
		del self[pos]

	def get(self, pos, key):
		''' Return the subtree with key "key" from position "pos" '''
		try:
			return self._children[pos][key]
		except BeyondFlatError as e:
			e.propogate(pos, len(self), key)

	def all_children(self):
		''' 
		Returns a dict (keyed on position) of sorted child hash lists.
		'''
		results = {}
		for i in range(self._length+1):
			hashes = self.children(i)
			if hashes:
				results[i] = hashes
		return results

	def children(self, i):
		''' A sorted list of all children at position i. '''
		return [self.get(i, child) for child in sort(self._children[i])]

	def __getitem__(self, i):
		return self._value[i]

	def __getslice__(self, i, j):
		if j > len(self): j = len(self)
		return [self[x] for x in range(i, j)]

	def __delitem__(self, i):
		self._deletions[i] = True

	def __delslice__(self, i, j):
		for x in range(i,j):
			del self[x]

	def __len__(self):
		''' Return the length of the internal immutable string '''
		return self._length

	def __repr__(self):
		classname = repr(self.__class__).split()[1]
		return "<%s instance '%s' at %s>" % (classname, self.key, hex(long(id(self)))[:-1])

	def flatten(self):
		''' Returns a string that summarizes self and all descendants. '''
		rstring = ""
		for i in range(self._length+1):
			for c in self.children(i):
				rstring += c.flatten()
			if i < self._length:
				# check whether to include character at this position
				if not self._deletions[i]:
					rstring += self._value[i]
		return rstring

	def flatnode(self):
		''' Returns a Flat version of this node '''
		return Flat(self.key, self.flatten(), self.treesum)

	def flattenchild(self, pos, key):
		newflat = self._children[pos][key].flatnode()
		self.insert_tree(pos, newflat)

	def trace(self, pos):
		''' 
		Given a position in the flat text, compute an (address, position) pair.
		'''
		t = self._trace(pos)
		if type(t) == tuple:
			return t
		else:
			raise IndexError("%d is out of range" % pos)

	def _trace(self, pos):
		togo = pos
		for i in range(len(self)+1):
			for child in self.children(i):
				try:
					x = child._trace(togo)
				except BeyondFlatError as e:
					e.propogate(i,len(self),child.key)
				if type(x) == tuple:
					x[0].prepend(x[0].jump(i, len(self), child.key))
					return x
				else:
					togo = x
			if togo == 0:
				return (Address(),i)
			if i < len(self) and not self._deletions[i]:
				togo -=1
		return togo

	def proto(self):
		''' Return a protocol representation '''
		runningstring = ""
		deletions = []
		result = []
		for i in range(len(self)+1):
			for child in self.children(i):
				if runningstring:
					result.append(runningstring)
					runningstring = ""
				result.append(child.proto())
			if i < len(self):
				runningstring += self._value[i]
				if self._deletions[i]: deletions.append(i)
		if runningstring: result.append(runningstring)
		result.append(deletions)
		return result

	@property
	def summable(self):
		runningstring = ""
		deletions = []
		result = []
		for i in range(len(self)+1):
			kids = {}
			for k in self._children[i]:
				kids[k] = self._children[i][k].treesum
			if kids:
				result.append(runningstring)
				runningstring = ""
				result.append(kids)
			if i < len(self):
				runningstring += self._value[i]
				if self._deletions[i]: deletions.append(i)
		if runningstring: result.append(runningstring)
		result.append(deletions)
		return result

	@property
	def treesum(self):
		return checksum(self.summable)

	@property
	def key(self):
		return key(self._value)

class Flat(Tree):
	def __init__(self, key, value, sum):
		self._key = key
		self._value = value
		self._sum = sum
		self._length = len(value)

	def __getitem__(self, pos):
		self.require()

	def __delitem__(self, pos):
		self.require()

	def flatten(self):
		return self._value

	def flatnode(self):
		return self

	def _trace(self, pos):
		if pos > len(self):
			return pos-len(self)
		else:
			self.require()

	def proto(self):
		return [self._key, self._value, self._sum]

	@property
	def _children(self):
		self.require()

	@property
	def _deletions(self):
		self.require()

	@property
	def summable(self):
		self.require()

	@property
	def treesum(self):
		return self._sum

	@property
	def key(self):
		return self._key

	def require(self):
		raise BeyondFlatError(Address())

def sort(d):
	k = d.keys()
	k.sort()
	return k

def stringparse(l):
	''' 
		Return a concatenation of all strings in a list
	'''
	return "".join([x for x in l if type(x)==str])

def positionparse(l):
	''' 
		Takes a list of strings and other objects, and returns
		a dict of the non-string objects keyed on position in the overall string
	'''
	position = 0
	result = {}
	for x in l:
		if type(x)==str:
			position += len(x)
		else:
			if position not in result:
				result[position] = [x]
			else:
				result[position].append(x)
