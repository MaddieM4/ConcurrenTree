from ConcurrenTree.model import instruction, operation
import context

class NumberContext(context.Context):
	def __init__(self, node, unique = None):
		context.Context.__init__(self, node)
		if unique == None:
			print "WARNING: Random unique being used in NumberNode."
			print "Uniques should be based on personal id data to avoid collisions."
			import random
			unique = random.randint(0, 2**32)
		self.unique = unique

	def delta(self, amount, unique=None):
		addr = self.node.head()[0]
		return operation.Operation([
			instruction.InsertNumber(addr, 0, amount, self.unique)])

	def incr(self):
		return self.delta(1)

	def decr(self):
		return self.delta(-1)
