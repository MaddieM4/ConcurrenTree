#!/usr/bin/python

from ejtp.util.crypto import make
from ejtp.util import hasher

# Create random keys
key1 = make(['rsa', None])
key2 = make(['rsa', None])

# Configure
TEST_COUNT = 103

def message(i):
	result = hasher.make(str(i))
	return result, result*10

# Wrapper functions
def encode(msg, sender, reciever):
	return reciever.encrypt(sender.decrypt(msg))

def decode(msg, sender, reciever):
	return encode(msg, reciever, sender)

def test_run(sender, reciever):
	for i in range(0, TEST_COUNT):
		desc, plaintext = message(i)
		ciphertext = encode(plaintext, key1, key2)
		if plaintext != decode(ciphertext, key1, key2):
			print "%r\n" % desc

# Actual test:
print "key1 >> key2"
test_run(key1, key2)
print "key2 >> key1"
test_run(key2, key1)
