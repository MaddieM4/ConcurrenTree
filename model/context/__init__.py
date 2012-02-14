from ConcurrenTree.model import node
import string, map, linear

def make(node_obj):
	# Create a context object
	t = type(node_obj)
	if t in (node.StringNode, node.ListNode):
		return linear.LinearContext(node_obj)
	elif t == node.MapNode:
		return map.MapContext(node_obj)
	elif t == node.SingleNode:
		return single.SingleContext(node_obj)
