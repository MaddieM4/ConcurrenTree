from linear import LinearNode

class StringNode(LinearNode):

	def __init__(self, value):
		try:
			value = str(value)
		except:
			raise TypeError("ListNode value must str, or something that can be turned into one")
		LinearNode.__init__(self, value, StringNode) # can only contain other StringNodes

	def encapsulate(self, obj):
		return str(obj)

	def flatitem(self, i):
		return self[i]

	@property
	def key(self):
		return self.keysum("t"+self.value)

	def proto(self):
		runningstr = ""
		result = []
		for i in range(len(self)+1):
			if len(self.children[i]) > 0:
				# Append children
				if runningstr:
					result.append(runningstr)
					runningstr = ""
				result.append(self.children[i].proto())
			if i < len(self):
				runningstr += self.value[i]
		if runningstr:
			result.append(runningstr)
		result.append(self.deletions)
		return result
