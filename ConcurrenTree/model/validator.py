class Validator(dict):
	# Callback collector for validating operations.
	# If things look wrong to your callback, raise an exception.
	# Return values are ignored.

	def __init__(self):
		dict.__init__(self)
		self['pre'] = set()
		self['instr'] = set()
		self['post'] = set()

	def pre(self, op, tree):
		for i in self['pre']:
			i(op, tree)

	def post(self, op, tree):
		for i in self['post']:
			i(op, tree)

	def instr(self, op, tree, instr):
		for i in self['instr']:
			i(op, tree, instr)

	def add(self, hook, callback):
		self[hook].add(callback)

	def remove(self, hook, callback):
		if callback in self[hook]:
			self[hook].remove(callback)

