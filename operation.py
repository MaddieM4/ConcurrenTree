import instruction
import hasher

class Operation:
	''' A collection of instructions '''

	def __init__(self, instructions = [], protostring = None):
		''' If protostring is present, uses that existing protocol object. If not, use instructions list. '''
		if protostring:
			# process protostring
			pass
		else:
			self.instructions = instructions

	@property
	def inserts(self):
		results = []
		for i in self.instructions:
			if type(i) == instruction.Insertion:
				results.append(i)
		return results

	@property
	def dep_provides(self):
		''' The dependencies that this operation provides to the tree '''
		return set([str(i.address_object)+str(i.position)+":"+i.value for i in self.inserts])

	@property
	def dep_requires(self):
		''' The dependencies that this operation requires before it can be applied '''
		return set([str(i.address_object) for i in self.instructions]) - self.dep_provides

	def ready(self, tree):
		''' Checks a tree for existence of all dependencies '''
		for i in self.dep_requires:
			try:
				i.address_object.resolve(tree)
			except:
				return False
		return True

	@property
	def hash(self):
		return hasher.make(str(self))

	def __str__(self):
		''' Returns a protocol operation object '''
		return ""
