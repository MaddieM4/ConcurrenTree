__all__ = [
    'string',
    'list',
    'map',
    'number',
    'single',
    'trinary',
    'wrapper',
]

from ConcurrenTree import node
import map, string, list, number, single, trinary

def make(node_obj, opsink, *args):
	# Create a context object
	t = type(node_obj)
	if t == node.StringNode:
		return string.StringWrapper(node_obj, opsink, *args)
	elif t == node.ListNode:
		return list.ListWrapper(node_obj, opsink, *args)
	elif t == node.MapNode:
		return map.MapWrapper(node_obj, opsink, *args)
	elif t == node.NumberNode:
		return number.NumberWrapper(node_obj, opsink, *args)
	elif t == node.SingleNode:
		return single.SingleWrapper(node_obj, opsink, *args)
	elif t == node.TrinaryNode:
		return trinary.TrinaryWrapper(node_obj, opsink, *args)
	else:
		raise NotImplementedError("No wrapper exists yet for this: "+repr(node_obj))
