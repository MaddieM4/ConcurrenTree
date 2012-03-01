import node

class SingleNode(node.Node):
	def __init__(self, limit=None):
		self.limit = limit
		self._children = [node.ChildSet(limit=self.limit),
			node.ChildSet(types=(SingleNode,))]

	# Node interface

	@property
	def value(self):
		return ""

	@property
	def key(self):
		return "/single"

	def flatten(self):
		v = self.head()[1].value_node()
		if v:
			return v.flatten()
		else:
			return None

	def get(self, pos, key):
		return self._children[pos][key]

	def put(self, pos, obj):
		self._children[pos].insert(obj)

	def delete(self):
		raise node.Undelable("SingleNodes do not support deletion. Recursive set to null instead.")

	@property
	def deletions(self):
		return []

	# Extra
	def head(self):
		if len(self._children[1]) > 0:
			addr, node = self._children[1]['/single'].head()
			return [1, '/single'] + addr, node
		else:
			return [], self

	def value_node(self):
		if len(self._children[0]) > 0:
			return self._children[0].head
		else:
			return None
