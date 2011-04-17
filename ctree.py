import hasher

class CTree:
	def __init__(self, value):
		self._value = value
		self._length = len(value)
		self._deletions = [False] * len(self)
		self._children = []
		for i in range(len(self)+1):
			self._children.append(CTreeChild())
		self.hash = hasher.make(self._value)

	def insert(self, value, pos):
		result = CTree(value)
		self._children[pos].insertTree(result)
		return result

	def delete(self, pos):
		del self[pos]

	def get(self, pos, hash):
		return self._children[pos].getTree(hash)

	def mark(self, pos, marker):
		self._children[pos].insertMarker(marker)

	def children(self):
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
		return self._length

	@property
	def flattened(self):
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
		return CTree(rstring)

	def __str__(self):
		rstring = ""
		for i in range(len(self)):
			if not self._deletions[i]:
				rstring += self._value[i]
		return rstring

class CTreeChild:
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

	def insertMarker(self, marker):
		self.markers[marker.totaltype] = marker

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
		return [x.flattened for x in self.children()]
