from hashlib import md5

def make(string):
	return md5(string).hexdigest()
