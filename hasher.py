from hashlib import new

HASH_FUNCTION = 'sha256' # was md5

def make(string):
	return new(HASH_FUNCTION, string).hexdigest()
