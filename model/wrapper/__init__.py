from ConcurrenTree.model import node
import map, string

def make(node_obj, opsink, *args):
	# Create a context object
	t = type(node_obj)
	if t == node.MapNode:
		return map.MapWrapper(node_obj, opsink, *args)
	elif t == node.StringNode:
		return string.StringWrapper(node_obj, opsink, *args)
	else:
		raise NotImplementedError("No wrapper exists yet for this: "+repr(node_obj))
