# Probably not the most complete test functions, but better than nothing.

def tstring():
	from ConcurrenTree import node
	grey = node.make("grey")
	gc = grey.context()
	gc.live.insert(4, " cat.") # "grey cat."
	gc.live.delete(0, 1) # "rey cat."
	gc.live.delete(7, 1) # "rey cat"
	gc.live.insert(0, "G") # "Grey cat"
	gc.live.insert(8, "!") # "Grey cat!"
	return gc.value == "Grey cat!" or gc.value

def tlist():
	from ConcurrenTree import node
	hello = node.make(["Hello"])
	hc = hello.context()
	hc.live.insert(1, ['world']) # ["Hello", "world"]
	hc.live.delete(0,1) # ["world"]
	hc.live.insert(1, ['wide', 'web']) # ["world", "wide", "web"]
	hc.live.delete(0,2) # ["web"]
	hc.live.insert(1,['site']) # ["web", "site"]
	hc.live.insert(0,['major']) # ["major", "web", "site"]
	hc.live.delete(1,1) # ["major", "site"]
	return hc.value == ["major", "site"] or hc.value
