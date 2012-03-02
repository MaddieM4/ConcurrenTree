import node

class ListNode(node.Node):

	def __init__(self, value):
		node.Node.__init__(self)
		try:
			self._value = [str(x) for x in value]
		except:
			raise TypeError("ListNode value must list of keys")
		self._length = len(self._value)
		self._children = [node.ChildSet(childtypes) for i in range(self.biglength)]
		self._del = [False for i in range(len(self))]

	@property
	def value(self):
		return self._value

	@property
	def key(self):
		return self.keysum("[%s]" % ",".join(self.value))

	def flatten(self):
		result = []
		for i in range(len(self)+1):
			for c in self.index(i):
				result += self.index(i)[c].flatten()
			if i<len(self) and not self._del[i]:
				result.append(self.elem(i).head.flatten())

	def _get(self, pos, key):
		return self._children[pos][key]

	def _put(self, pos, n):
		if pos < len(self) and n.key != self.value[pos]:
			raise ValueError("Node has key "+repr(n.key)+
				", expected key "+repr(self.value[pos]))
		self._children[pos].insert(n)

	def _delete(self, pos):
		self._del[pos] = True

	@property
	def _deletions(self):
		return node.enumerate_deletions(self._del)

	def __len__(self):
		return self._length

	def __getitem__(self, i):
		return self._value[i]

	def index(self, i):
		return self._children[i+len(self)]

	def elem(self, i):
		return self._children[i]

	@property
	def biglength(self):
		# Total number of slots for children
		return 2*len(self)+1
