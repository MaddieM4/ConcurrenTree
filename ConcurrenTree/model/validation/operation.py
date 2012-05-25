import request

class OperationRequest(request.ValidationRequest):
	'''
	Represents an operation from a remote source.
	'''
	def __init__(self, author, docname, op, callback):
		self.author = author
		self.docname = docname
		self.op = op
		self.callback = callback

	def desc_string(self):
		return "A user sent you an operation."

	def __str__(self):
		return self.desc_string() + " author: %r, docname: %r, op: %r" % (
			self.author,
			self.docname,
			self.op,
		)

