from ConcurrenTree.model import operation, instruction, address

class Context:
	''' Base class for context objects '''
	def __init__(self, node, addr):
		self.node = node
		self.addr = addr
