from ConcurrenTree import node
import string, map, list, number, single, trinary

def make(node_obj, *args):
	# Create a context object
	t = type(node_obj)
	if t == node.StringNode:
		return string.StringContext(node_obj)
	elif t == node.ListNode:
		return list.ListContext(node_obj)
	elif t == node.MapNode:
		return map.MapContext(node_obj)
	elif t == node.SingleNode:
		return single.SingleContext(node_obj)
	elif t == node.NumberNode:
		return number.NumberContext(node_obj, *args)
	elif t == node.TrinaryNode:
		return trinary.TrinaryContext(node_obj, *args)
