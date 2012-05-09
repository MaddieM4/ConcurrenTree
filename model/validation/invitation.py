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
