from ConcurrenTree import operation, instruction, address, node
import context

class StringContext(context.Context):
	def insert(self, pos, value):
		iaddr, ipos = self._traceindex(pos)
		i = instruction.InsertNode(iaddr, ipos, node.make(value))
		return operation.Operation([i])

	def delete(self, pos, size=1):
		killzones = [self._traceelem(pos+x) for x in range(size)]
		return operation.Operation([instruction.Delete(*k) for k in killzones])

	def _traceelem(self, pos, node = None, addr = [], fail=True):
		# Returns (addr, pos) for a char in the flat rep of the node
		node = node or self.node
		addr = address.Address(addr)

		for i in range(len(node)+1):
			for c in node._children[i]:
				# naddr = new address
				# pos   = overwritten with leftovers
				naddr, pos = self._traceelem(pos,
					node.get(i,c), addr+[i,c], False)
				if naddr != None:
					return naddr, pos
			if i < len(node) and not node._del[i]:
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
			for c in node._children[i]:
				# naddr = new address
				# pos   = overwritten with leftovers
				naddr, pos = self._traceindex(pos,
					node.get(i,c), addr+[i,c], False)
				if naddr != None:
					return naddr, pos

			# Check for finish, kill one for nondeleted characters
			if pos == 0:
				return addr, i
			elif i < len(node) and not node._del[i]:
				pos -= 1
		if fail:
			raise IndexError("pos out of range, longer than len(node.flatten())")
		else:
			return None, pos

