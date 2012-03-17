from ConcurrenTree.model import operation, instruction, address, node
import context

class MapContext(context.Context):

	# Model level - accurate to data model

	def get(self, key):
		return self.node.get(key, "/single")

	def set(self, key, value):
		if self.has(key):
			# Use existing SingleNode
			r = self.get(key).context().set(value)
			return address.Address([key, "/single"])+r
		else:
			# Make Singlenode
			s = instruction.InsertSingle([], key)
			# Make actual node
			n = node.make(value).op(0, [key, "/single"])
			return s + n

	def has(self, key):
		return key in self.node._data

	# Virtual level - treat null values as removed, drop ops, etc.

	def __getitem__(self, key):
		return self.get(key).flatten()

	def __setitem__(self, key, value):
		self.live.set(key, value)

	def __contains__(self, key):
		return self.has(key) and (self[key] != None)
