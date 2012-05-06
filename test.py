#!/usr/bin/env python

import doctest
import ConcurrenTree

def test_recursive(mod):
	(failure_count, test_count) = doctest.testmod(mod)
	if "__all__" in dir(mod):
		for child in mod.__all__:
			fullchildname = mod.__name__+"."+child
			print "Testing", fullchildname
			childmod = __import__(fullchildname, fromlist=[""])
			cf, ct = test_recursive(childmod)
			failure_count += cf
			test_count    += ct
	return (failure_count, test_count)

failures, tests = test_recursive(ConcurrenTree)
print "%d failures, %d tests." % (failures, tests)
