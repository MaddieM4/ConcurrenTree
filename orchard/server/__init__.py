''' 
Wrappers that subclass BCP.PoolServer. This lets us run
our servers with the BCP.ServerPool framework.

There's a lot of useful and fairly general code in here,
so as always, feel free to copy it out for your own 
non-Orchard use.

'''

from ConcurrenTree.model.bcp.serverpool import PoolServer, Policy
import ConcurrenTree.model.bcp.doublequeue as dq

def startmessage(servname, port):
	servname = (servname + " Server").ljust(18)
	print "%s starting on port %d" % (servname, port)
