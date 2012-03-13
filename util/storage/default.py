import filestorage
from ConcurrenTree.util.crypto import *
from ConcurrenTree.model.auth import Auth

def DefaultFactory():
	# Crypto
	opener = file.KeyFileOpener("~/.ConcurrenTree/keys")
	cfac = factory.CryptoFactory(opener)
	# Storage
	return filestorage.FileStorageFactory(encryptorFactory=cfac)

def DefaultAuth():
	fac = DefaultFactory()
	return Auth(fac)
