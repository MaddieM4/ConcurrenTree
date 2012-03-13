import encryptor

class RotateEncryptor(encryptor.Encryptor):
	def __init__(self, offset):
		self.offset = offset

	def encrypt(self, source):
		return self.rotate(source, self.offset)

	def decrypt(self, source):
		return self.rotate(source, -self.offset)

	def rotate(self, source, offset):
		result = ""
		for i in source:
			result += chr((ord(i)+offset) % 256)
		return result

	def proto(self):
		return ['rotate', self.offset]
