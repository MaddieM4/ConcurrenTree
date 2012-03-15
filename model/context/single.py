from ConcurrenTree.model import operation, instruction, node
import context

class SingleContext(context.Context):
	def set(self, value):
		addr, head = self.head()
		op = operation.Operation()
		if len(head._children[0]) > 0:
			# Extend head
			op += instruction.InsertSingle(addr, 1)
			addr += [1, '/single']
			head = head.head()[1]
		# Insert value
		vnode = node.make(value)
		op += instruction.InsertNode(addr, 0, vnode)
		return op

	def get(self):
		# Return (addr, node) for current value
		addr, head = self.head()
		vn = head.value_node()
		if vn == None:
			return (None, None)
		return addr+[0, vn.key], vn

	def head(self):
		# Return (addr, node) for the current head SingleNode
		return self.node.head()
