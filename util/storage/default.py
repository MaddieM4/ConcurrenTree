import ramstorage
from ConcurrenTree.util.crypto import *
from ConcurrenTree.model.auth import Auth

def DefaultFactory():
	# Crypto
	opener = file.KeyFileOpener("~/.ConcurrenTree/keys")
	cfac = factory.CryptoFactory(opener)
	# Storage
	return ramstorage.RAMStorageFactory(encryptorFactory=cfac)

def DefaultAuth():
	fac = DefaultFactory()
	return Auth(fac)
