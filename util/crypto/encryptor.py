class Encryptor(object):
	def encrypt(self, s):
		raise NotImplementedError("Encryptor must define 'encrypt'")

	def decrypt(self, s):
		raise NotImplementedError("Encryptor must define 'decrypt'")

class Flip(Encryptor):
	def __init__(self, parent):
		self.encrypt = parent.decrypt
		self.decrypt = parent.encrypt
