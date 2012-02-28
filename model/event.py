class EventGrid(object):
	# Stores callbacks (they should take args (evgrid, label))
	def __init__(self, labels=[]):
		self.handlers = {}
		self.setup_labels(labels)

	def setup_labels(self, labels):
		for i in labels:
			self.handlers[i] = []

	def register(self, label, func):
		if func in self[label]:
			del self[label].index(func)
		self[label].append(func)

	def happen(self, label):
		for i in self[label]:
			i(self, label)

	def __getitem__(self, label):
		return self.handlers[label]

	def __setitem__(self, label, value):
		self.handlers[label] = value

	def __delitem__(self, label):
		del self.handlers[label]
