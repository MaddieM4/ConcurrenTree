from ConcurrenTree.model import operation, instruction, node
import context

class MapContext(context.Context):
	def __getitem__(self, key):
		return self.node.get(key, "/single").flatten()

	def __setitem__(self, key, value):
		self.live.set(key, value)

	def set(self, key, value):
		# Make Singlenode
		s = instruction.InsertSingle([], key)
		# Make actual node
		n = instruction.InsertNode([key, "/single"], 0, node.make(value))
		return operation.Operation([s,n])
