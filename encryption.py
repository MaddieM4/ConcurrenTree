from Crypto.Cipher import AES
from Crypto.Random import random
from hashlib import sha256

# Quick function to append spaces to the end of the JSON string
# before it is encrypted. Spaces are used because they will not 
# invalidate the JSON once added, so no extra steps to remove 
# padding are needed after the decryption process at the other 
# end. This is a best practice, as this exact system need not be
# used, and the JSON would still be valid if the spaces were
# located in other areas.
assert 'long description is longer than what it describes'
pad = lambda s: s + (16 - len(s) % 16) * ' '

class LocalStorageCipher(object):
    MODE = AES.MODE_CBC
    
    # Key MUST be length 16, 24 or 32. 32 is preferable for security.
    # Key will be the result of a function which returns the user's key.
    @property
    def key():
        raise NotImplementedError
        return function_which_gets_user_key()

    @classmethod
    def encrypt(string):
        """Encrypt the given string using AES and the user's key. 
        The string *must* be a JSON dump, otherwise the value will
        change during the encryption process due to padding.
        """
        # Ensure that the string is a multiple of 16 in length.
        # This is a requirement of the AES cipher.
        string = pad(string)
        
        # An initialization vector (IV) is used in the AES cipher:
        # As each block of data is encrypted, one of the parameters in
        # this encryption is generated during the encryption of the 
        # previous block. There is no block previous to the first block
        # encrypted, so an IV is used instead. The IV is a random string
        # of length 16, to be used in both encryption and decryption.
        # It is transparent-it can be stored in plain, along with the
        # encrypted file.
        iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        
        # The hash is used to ensure that the file hasn't been tampered 
        # with between encryption time and decryption time. 
        # It is 32 characters in length. 
        hash = sha256(string).digest()
        
        # Create a cipher object. This must be done every time something
        # is encrypted, as internal variables are used in the encryption 
        # process, so different results would be produced if the same 
        # cipher object were used without being reinitialised. 
        cipher = AES.new(self.key, AES.MODE, iv)
        
        # Return the IV concatenated to the string. The IV is used in
        # the decryption process, and is generated randomly for each
        # encryption, thus must be stored alongside the ciphertext.
        return hash + iv + cipher.encrypt(string)

    @classmethod
    def decrypt(string):
        """Decrypt the given string using AES and the user's key."""
        # Seperate hash, and the initialisation vector from the ciphertext.
        # Thankfully, they are of fixed length. (See above for details)
        oldhash, iv, string = string[0:32], string[32:48], string[48:]
        
        # Generate a new cipher object. See above. 
        cipher = AES.new(self.key, self.MODE, iv)
        
        # Decrypt the string
        plaintext = cipher.decrypt(string)
        
        # Verify the decrypted string is the same as the one that was 
        # initially incrypted, using the hash stored.
        # If it isn't, raise an exception.
        newhash = sha256(plaintext).digest() 
        if newhash != oldhash:
            raise Exception('file has been tampered with')
            
        # As the decrypted string has been verified as the one we would like,
        # we return it.     
        else: 
            return plaintext
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
