from ConcurrenTree.model.node.context import *
from ConcurrenTree.model.node import make

class MapContext(Context):

	def extend(self, newvalues = {}):
		''' Return op extending the map '''

		newmap = make(newvalues)

		if len(self.node.extension) > 0:
			# extend child
			headkey = self.node.extension.head.key
			op = self.node.make_flatcontext(self.addr+[len(self.node), headkey]).extend(newvalues)
			return op
		else:
			# extend self
			op = newmap.op(len(self.node))
			op.prefix(self.addr)
			return op
