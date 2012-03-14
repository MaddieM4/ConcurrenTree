import encryptor

from Crypto.Hash import SHA
from Crypto.Cipher import AES

class AESEncryptor(encryptor.Encryptor):
	def __init__(self, password):
		self.password = password
		hash = SHA.new(password).digest()
		self.cipher = AES.new(hash[:16]) # Must be multiple of 16, cuts 20 char digest to 16 char

	def encrypt(self, value):
		# Uses custom format to encrypt arbitrary length strings with padding
		code = str(len(value)) + "\x00" + value
		code += (16 - len(code) % 16) * "\x00"
		return self.cipher.encrypt(code)

	def decrypt(self, value):
		code = self.cipher.decrypt(value)
		split = code.index('\x00')
		length = int(code[:split])
		code = code[split+1:]
		return code[:length]

	def proto(self):
		return ['aes', self.password]
