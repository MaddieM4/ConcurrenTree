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

	@property
	def key(self):
		return self.keysum("t"+self.value)

	def proto(self):
		return [] # TODO - advanced type representations
