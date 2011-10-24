from linear import LinearNode

class ListNode(LinearNode):

	def __init__(self, value):
		try:
			value = tuple(value)
		except:
			raise TypeError("ListNode value must be iterable")
		LinearNode.__init__(self, value)

	def encapsulate(self, obj):
		return [obj]

	@property
	def key(self):
		return "[]" # TODO - fix

	def proto(self):
		return [] # TODO - advanced type representations
