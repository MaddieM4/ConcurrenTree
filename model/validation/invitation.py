import request

class Invitation(request.ValidationRequest):
	'''
	Represents another participant inviting you to
	load a document from them.
	'''
	def __init__(self, author, docname, callback):
		self.author = author
		self.docname = docname
		self.callback = callback

	def desc_string(self):
		return "A user invited you to join a document and load a copy from them."

	def __str__(self):
		'''
		>>> i = Invitation("x", "y", lambda z:z)
		>>> str(i)
		"A user invited you to join a document and load a copy from them. author: 'x', docname: 'y'"
		'''
		return self.desc_string() + " author: %r, docname: %r" % (
			self.author,
			self.docname,
		)
