from hashlib import new

HASH_FUNCTION = 'sha256' # was md5

def make(string):
	return new(HASH_FUNCTION, string).hexdigest()

def make6(string):
	return maken(string, 6)

def maken(string, n):
	return make(string)[:n]

def sum(string):
	s = 0
	for i in string:
		s += ord(i)
	return s

def key(string):
	if len(string)>10:
		return string[:10]+str(sum(string[10:]))
	else:
		return string
