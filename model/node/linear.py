import node

class LinearNode(node.Node):
	''' Base class for StringNode and ListNode, do not use directly '''

	def __init__(self, value, childtypes=None):
		self._value = value
		self._length = len(value)
		self._children = [node.ChildSet(childtypes) for i in range(len(self)+1)]
		self._deletions = [False for i in range(len(self))]
		self.type = type(self.value)

	# Node Interface

	@property
	def value(self):
		return self._value

	def flatten(self):
		result = self.type() # blank object of same type as self.value
		for i in range(len(self)+1):
			for child in self._children[i].values:
				result += self.encapsulate(child.flatten())
			if i < len(self) and not self._deletions[i]:
				result += self.encapsulate(self.flatitem(i))
		return result

	def get(self, pos, key):
		return self._children[pos][key]

	def put(self, pos, obj):
		self._children[pos].insert(obj)

	def delete(self, pos):
		self._deletions[pos] = True

	# Subclass responsibilities

	def encapsulate(self, obj):
		''' Create an object of self.type from obj '''
		raise NotImplementedError("Subclasses of LinearNode must define function 'encapsulate'")

	def flatitem(self, i):
		''' Python object for self[i] '''
		raise NotImplementedError("Subclasses of LinearNode must define function 'flatitem'")

	@property
	def key(self, obj):
		raise NotImplementedError("Subclasses of LinearNode must define property 'key'")

	def proto(self):
		node.Node.proto(self)

	# Plumbing

	def __len__(self):
		return self._length

	def __getitem__(self, i):
		return self.value[i]
