#!/usr/bin/env python

import doctest
import ConcurrenTree

def test_recursive(mod, debug=False):
	(failure_count, test_count) = doctest.testmod(mod)
	if "__all__" in dir(mod):
		for child in mod.__all__:
			fullchildname = mod.__name__+"."+child
			if debug:
				print "Testing", fullchildname
			childmod = __import__(fullchildname, fromlist=[""])
			cf, ct = test_recursive(childmod, debug)
			failure_count += cf
			test_count    += ct
	return (failure_count, test_count)

def test_ctree(debug = False):
	failures, tests = test_recursive(ConcurrenTree, debug)
	print "%d failures, %d tests." % (failures, tests)

if __name__ == "__main__":
	import sys
	debug = "-l" in sys.argv
	test_ctree(debug)
