import hasher
import marker

class Tree:
	def __init__(self, value="", name=''):
		self.name = name
		self._value = value
		self._length = len(value)
		self._deletions = [False] * len(self)
		self._children = []
		self.operations = {}
		for i in range(len(self)+1):
			self._children.append(TreeChild())
		self.hash = hasher.make(self._value)

	def insert(self, pos, value):
		''' Insert a child to the tree with string "value" at position "pos" '''
		result = Tree(value)
		self._children[pos].insertTree(result)
		return result

	def delete(self, pos):
		''' Mark a character in a tree as deleted '''
		del self[pos]

	def get(self, pos, hash):
		''' Return the subtree with hash "hash" from position "pos" '''
		return self._children[pos].getTree(hash)

	def mark(self, pos, type, value):
		''' Set a marker on a position '''
		self._children[pos].mark(type, value)

	def markers(self):
		''' 
		Returns a dict (keyed on position) of dict[totaltype] = marker.
		'''
		results = {}
		for i in range(self._length+1):
			markers = self._children[i].markers
			if markers:
				#for x in markers:
				#	markers[x] = markers[x].value
				results[i] = markers
		return results

	def children(self):
		''' 
		Returns a dict (keyed on position) of sorted child hash lists.
		'''
		results = {}
		for i in range(self._length+1):
			hashes = self._children[i].sorted()
			if hashes:
				results[i] = hashes
		return results

	def __getitem__(self, i):
		return (self._value[i],not self._deletions[i], self._children[i].markers)

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
		''' Returns a single-level tree that summarizes all descendants. Not backwards-compatible for applying ops. '''
		# This function does not yet support markers.
		rstring = ""
		rmarkerboxes = []
		for i in range(self._length+1):
			# Set up markerbox
			rmarkerboxes.append({})
			# keep working on this function after talking to Nathaniel
			for c in self._children[i].flat_children():
				rstring += c._value
			if i < self._length:
				# check whether to include character at this position
				if not self._deletions[i]:
					rstring += self._value[i]
		return Tree(rstring)

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
			for child in self._children[i].children():
				x = child._trace(togo)
				print "///",x
				if type(x) == tuple:
					return ("%d:%s/%s" % (i,child.hash,x[0]),x[1])
				else:
					togo -= x
			if togo == 0:
				return ("",i)
			if i < len(self) and not self._deletions[i]:
				togo -=1
		return togo

	def __str__(self):
		rstring = ""
		for i in range(len(self)):
			if not self._deletions[i]:
				rstring += self._value[i]
		return rstring

class TreeChild:
	def __init__(self, trees = [], markers = []):
		self.trees = {}
		self.markers = {}
		for i in trees:
			self.insertTree(i)
		for i in markers:
			self.insertMarker(i)

	def insertTree(self, tree):
		hash = tree.hash
		if hash in self.trees:
			if tree.value != self.trees[hash].value:
				raise IndexError("Hash collision")
			# if not, ignore duplicate operation
		else:
			self.trees[hash] = tree

	def getTree(self, hash):
		return self.trees[hash]

	def insertMarker(self, type):
		cat, sub = marker.sep(type)
		self.markers[type] = marker.Marker(cat, sub)

	def mark(self, type, value):
		pass

	def getMarker(self, totaltype):
		return self.markers[totaltype]

	def sorted(self):
		''' Return a sorted list of all child hashes'''
		keys = self.trees.keys()
		keys.sort()
		return keys

	def children(self):
		''' Return a sorted array of children '''
		return [self.getTree(x) for x in self.sorted()]

	def flat_children(self):
		''' Return a sorted list of flattened children '''
		return [x.flatten() for x in self.children()]
