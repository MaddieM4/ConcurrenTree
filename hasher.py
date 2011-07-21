from hashlib import new

HASH_FUNCTION = 'sha256' # was md5

def make(string):
	return new(HASH_FUNCTION, string).hexdigest()

def make6(string):
	return maken(string, 6)

def maken(string, n):
	return make(string)[:n]
