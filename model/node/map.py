import node

class MapNode(node.Node):
	def __init__(self, keys=[], source={}):
		self._value = list(set(keys) + set(source.keys())) # unique all the keys
		self._value = [str(x) for x in self.value] # convert them to strings
		self._value.sort()
		self._children = [node.ChildSet() for i in range(0, len(self))]
		self.extension = node.ChildSet(MapNode)

	def __len__(self):
		return len(self.value)

	@property
	def value(self):
		return self._value

	@property
	def key(self):
		return self.keysum("{%s}" % ",".join(self.value))
