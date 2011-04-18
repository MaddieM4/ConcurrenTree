import re

class Address:
	''' Address format: index:hash/index:hash '''

	def __init__(self, string):
		self.layers = []
		if not self.process(string):
			raise ValueError(string+" is not a valid address of form index:hash")

	def process(self, string):
		pieces = string.split("/")
		if len(pieces) == 0:
			return False
		for i in pieces:
			match = re.match("^(\d+):([0-9a-fA-F]+)$", i)
			if match:
				groups = match.groups()
				self.layers.append((int(groups[0]), groups[1]))
			else:
				return False
		return True

	def resolve(self, tree):
		x = tree
		for i in self.layers:
			x = x.get(i[0],i[1])
		return x
