from wrapper import Wrapper

class MapWrapper(Wrapper):
	def __getitem__(self, i):
		from ConcurrenTree.model.wrapper import make
		# Compute address of landing node
		addr, node = self.context.get(i).head()
		node = node.value_node()
		if node == None:
			return None
		addr = [i, '/single'] + addr + [0, node.key]
		return make(node, self.childsink(addr))

	def __setitem__(self, i, v):
		self.opsink(self.context.set(i, v))

	def __delitem__(self, i):
		self.opsink(self.context.set(i, None))

	def apply(self, op):
		self.node.apply(op)

	def update(self, d):
		for k in d:
			self[k] = d[k]
