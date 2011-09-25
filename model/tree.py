from ConcurrenTree.model import ModelBase
from ConcurrenTree.util.hasher import key, sum, checksum

import operation

def sort(d):
	k = d.keys()
	k.sort()
	return k

class Tree(ModelBase):
	def __init__(self, value=""):
		''' Do not manipulate children externally. Use class methods. '''
		self._value = value
		self._length = len(value)
		self._deletions = [False] * len(self)
		self._children = []
		for i in range(len(self)+1):
			self._children.append(dict())

	def insert(self, pos, value):
		''' Insert a child to the tree with string "value" at position "pos" '''
		result = Tree(value)
		self.insert_tree(pos, result)
		return result

	def delete(self, pos):
		''' Mark a character in a tree as deleted '''
		del self[pos]

	def insert_tree(self, pos, obj):
		''' Insert an object as a child tree, setting its era properties '''
		obj.initplace(self, self.level+1, self._shortcut)
		obj.name = self.name
		self._children[pos][obj.key] = obj

	def get(self, pos, key):
		''' Return the subtree with key "key" from position "pos" '''
		return self._children[pos][key]

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
				x = child._trace(togo)
				print "///",x
				if type(x) == tuple:
					return [[i, child.key]]+x[0], x[1]
				else:
					togo -= x
			if togo == 0:
				return ([],i)
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
		pass

	@property
	def sum(self):
		return checksum(self.summable)

	@property
	def key(self):
		return key(self._value)

class Flat(Tree):
	def __init__(self, key, value, sum):
		self._key = key
		self._value = value
		self._sum = sum

class BeyondFlatError(Exception):
	def __init__(self, flataddr):
		''' Flataddr should be the address of the node that needs to be loaded. '''
		Exception.__init__(self, "Target flat not loaded: "+str(flataddr))
		self.addr = flataddr

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
