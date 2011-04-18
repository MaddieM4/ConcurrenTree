import re

class Address:
	''' Address format: index:hash/index:hash '''

	def __init__(self, target):
		self.layers = []
		if type(target)==str:
			if not self.process(target):
				raise ValueError(target+" is not a valid address of form index:hash")
		elif type(target) == Address:
			self.layers = target.layers

	def process(self, string):
		if len(string) == 0:
			# Root tree
			return True
		pieces = string.split("/")
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

	def __str__(self):
		return "/".join(["%d:%s" % i for i in self.layers])
