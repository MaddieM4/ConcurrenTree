from linear import LinearNode

class ListNode(LinearNode):

	def __init__(self, value):
		try:
			value = list(value)
		except:
			raise TypeError("ListNode value must be iterable")
		LinearNode.__init__(self, value)

	def encapsulate(self, obj):
		return [obj]

	def flatitem(self, i):
		return self[i].flatten()

	@property
	def key(self):
		raw = "[%s]" % ",".join(x.key for x in self)
		return self.keysum(raw)
