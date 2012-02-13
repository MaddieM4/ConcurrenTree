from ConcurrenTree.model import operation, instruction, address
import context

class StringContext(context.Context):
	def insert(self, pos, value):
		iaddr, ipos = self._traceindex(pos)
		i = instruction.InsertText(iaddr, ipos, value)
		return operation.Operation([i])

	def delete(self, pos, size):
		killzones = [self._tracechar(pos+x) for x in range(size)]
		return operation.Operation([instruction.Delete(*k) for k in killzones])

	def _tracechar(self, pos, node = None, addr = [], fail=True):
		# Returns (addr, pos) for a char in the flat rep of the node
		node = node or self.node
		addr = address.Address(addr)

		for i in range(len(node)):
			for c in node._children[i]:
				# naddr = new address
				# pos   = overwritten with leftovers
				naddr, pos = self._tracechar(pos,
					node.get(i,c), addr+[i,c], False)
				if naddr != None:
					return naddr, pos
			if pos == 0:
				return addr, i
			else:
				pos -= 1
		if fail:
			raise IndexError("pos out of range, longer than len(node.flatten())-1")
		else:
			return None, pos


	def _traceindex(self, pos, node = None, addr = [], fail=True):
		# Returns (addr, pos) for an index in the flat rep of the node
		node = node or self.node
		addr = address.Address(addr)

		for i in range(len(node)+1):
			if i < len(node):
				for c in node._children[i]:
					# naddr = new address
					# pos   = overwritten with leftovers
					naddr, pos = self._traceindex(pos,
						node.get(i,c), addr+[i,c], False)
					if naddr != None:
						return naddr, pos
				if len(node._children[i]):
					pos += 1
			if pos == 0:
				return addr, i
			else:
				pos -= 1
		if fail:
			raise IndexError("pos out of range, longer than len(node.flatten())")
		else:
			return None, pos

