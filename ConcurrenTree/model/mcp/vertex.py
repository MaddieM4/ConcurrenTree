import hardlupa

class Vertex(hardlupa.SBRuntime):
	'''
	Class for validating an op by a vertex's rules.
	'''

	def __init__(self, model):
		self.name    = model.name
		self.sandbox = model.sandbox
		# TODO: setup API module

	def validate_instruction(self, instruction):
		if self['validate_instruction ~= nil']:
			return self['validate_instruction(%r)' % instruction.lua]
		else:
			return True

	def validate_state(self, tree_before, tree_after):
		if self['validate_state ~= nil']:
			return self['validate_state()']
		else:
			return True

	def validate_op(self, op, tree):
		return validate_state(self, tree, tree)
