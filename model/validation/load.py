import request

class LoadRequest(request.ValidationRequest):
	'''
	Represents a request from a remote interface, for a full copy of a doc.
	'''
	def __init__(self, author, docname, callback):
		self.author = author
		self.docname = docname
		self.callback = callback

	def desc_string(self):
		return "A user requested to load a document from you."

	def __str__(self):
		return self.desc_string() + " author: %r, docname: %r" % (
			self.author,
			self.docname,
		)


