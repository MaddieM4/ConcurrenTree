from ConcurrenTree.model.node.context import *

class MapContext(Context):

	def extend(self, newvalues = {}):
		if len(node.extension) > 0:
			# extend child
		else:
			# extend self
			inst = instruction.Instruction([])

	def makenode(self, values):
		# Create base instruction
		keys = values.keys()
		keys.sort()
		op = operation.Operation()
		op += instruction.InsertMap(self.addr, len(self.node), keys)

		# Derive child address
		childkey = None
		childaddr = address.Address(self.addr.proto()+[len(self.node), childkey])

		# Insert values
		for i in range(len(keys)):
			k = keys[i]
			op += instruction.InsertString(childaddr, k, values[k])
