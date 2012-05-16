import request

class HelloRequest(request.ValidationRequest):
	'''
	Represents introductory information from a remote source.
	'''
	def __init__(self, author, encryptor, callback):
		self.author = author
		self.encryptor = encryptor
		self.callback = callback

	def desc_string(self):
		return "A remote interface is telling you its encryptor proto."

	def __str__(self):
		return self.desc_string() + " author: %r, encryptor: %r" % (
			self.author,
			self.encryptor,
		)


