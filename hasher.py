from hashlib import new

HASH_FUNCTION = 'sha512' # was md5

def make(string):
	return new(HASH_FUNCTION, string).hexdigest()
