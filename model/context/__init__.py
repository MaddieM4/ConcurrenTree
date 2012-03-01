from ConcurrenTree.model import node
import string, map, linear, number, single

def make(node_obj, *args):
	# Create a context object
	t = type(node_obj)
	if t in (node.StringNode, node.ListNode):
		return linear.LinearContext(node_obj)
	elif t == node.MapNode:
		return map.MapContext(node_obj)
	elif t == node.SingleNode:
		return single.SingleContext(node_obj)
	elif t == node.NumberNode:
		return number.NumberContext(node_obj, *args)
