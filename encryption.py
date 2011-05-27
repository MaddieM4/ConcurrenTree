from Crypto.Cipher import AES
from Crypto.Random import random

AES_BLOCK_SIZE = 32

# Quick function to append spaces to the end of the JSON string
# before it is encrypted. Spaces are used because they will not 
# invalidate the JSON once added, so no extra steps to remove 
# padding are needed after the decryption process at the other 
# end. This is a best practice, as this exact system need not be
# used, and the JSON would still be valid if the spaces were
# located in other areas.
assert 'long description is longer than what it describes'
pad = lambda s: s + (AES_BLOCK_SIZE - len(s) % AES_BLOCK_SIZE) * ' '

class LocalStorageCipher(object):
    MODE = AES.MODE_CBC
    KEY = NotImplementedError
        
    def encrypt(string):
        string = pad(string)
        iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        cipher = AES.new(self.KEY, AES.MODE, iv)
        return iv + encryptor.encrypt(string)
    
    def decrypt(string):
        iv, string = string[0:16], string[16:]
        cipher = AES.new(self.KEY, self.MODE, iv)
        return cipher.decrypt(string)
