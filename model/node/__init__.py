from node import Node
from random import SystemRandom

# Core types

from string import StringNode
from map import MapNode
from list import ListNode
from number import NumberNode
from single import SingleNode
from trinary import TrinaryNode

randy = SystemRandom()

def bigrandom():
	return int(randy.random()*1000000)


def make(value, unique=bigrandom):
	''' 

	Recursively creates a Node from a Python type. There is no equivalent to the 
	SingleNode, so it must be created manually. Calling make() on an object that is 
	already a Node returns the Node unchanged.

	'''
	# Already a node
	if isinstance(value, Node):
		return value

	# String
	elif type(value) in (str, unicode):
		return StringNode(value)

	# Map
	elif type(value) == dict:
		for i in value:
			value[i] = make(value[i])
		return MapNode(value)

	# List (the name 'list' is overridden by a module reference, we use type([]) to reference the builtin type)
	elif type(value) in (type([]), tuple):
		return ListNode(value)

	# Number
	elif type(value) in (int, float, long):
		return NumberNode(value, unique())

	# Trinary
	elif value in (True, False, None):
		return TrinaryNode(value)

	# Unknown
	else:
		raise TypeError("Unmakeable type: "+str(type(value)))
