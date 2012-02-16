import node

class StringNode(node.Node):
	def __init__(self, value):
		node.Node.__init__(self)
		try:
			self._value = str(value)
		except:
			raise TypeError("StringNode value must str, or something that can be turned into one")
		self._length = len(self._value)
		self._children = [node.ChildSet(childtypes) for i in range(len(self)+1)]
		self._del = [False for i in range(len(self))]

	@property
	def value(self):
		return self._value

	@property
	def key(self):
		return self.keysum("t"+self.value)

	def flatten(self):
		result = self.type() # blank object of same type as self.value
		for i in range(len(self)+1):
			for child in self._children[i].values:
				result += child.flatten()
			if i < len(self) and not self._del[i]:
				result += self[i]
		return result

	def _get(self, pos, key):
		return self._children[pos][key]

	def _put(self, pos, obj):
		self._children[pos].insert(obj)

	def _delete(self, pos):
		self._del[pos] = True

	@property
	def _deletions(self):
		return node.enumerate_deletions(self._del)

	def __len__(self):
		return self._length

	def __getitem__(self, i):
		return self._value[i]
