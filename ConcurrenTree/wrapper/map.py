from wrapper import Wrapper

class MapWrapper(Wrapper):
	def __getitem__(self, i):
		# Compute address of landing node
		addr, node = self.context.get(i).head()
		node = node.value_node()
		if node == None:
			return None
		addr = [i, '/single'] + addr + [0, node.key]
		return self.childnode(node, addr)

	def __setitem__(self, i, v):
		self.opsink(self.context.set(i, v))

	def __delitem__(self, i):
		'''
		Delete an element of a map.

		>>> from ConcurrenTree import document
		>>> w = document.Document({}).wrapper()
		>>> "sample" in w
		False
		>>> w['sample'] = "value"
		>>> "sample" in w
		True
		>>> w['sample'] = {}
		>>> "sample" in w
		True
		>>> del w['sample']
		>>> w['sample']
		w<None>
		>>> "sample" in w
		False
		'''
		self.opsink(self.context.set(i, None))

	def __contains__(self, i):
		return i in self.node and self[i].value != None

	def __iter__(self):
		return self.node.__iter__()

	def __len__(self):
		return len(self.value)

	def apply(self, op):
		self.node.apply(op)

	def update(self, d):
		for k in d:
			self[k] = d[k]
