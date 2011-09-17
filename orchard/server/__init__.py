''' 
Wrappers that subclass BCP.PoolServer. This lets us run
our servers with the BCP.ServerPool framework.

There's a lot of useful and fairly general code in here,
so as always, feel free to copy it out for your own 
non-Orchard use.

'''

from ConcurrenTree.util.server.pool.server import Server
from ConcurrenTree.util.server.pool.policy import *
import ConcurrenTree.util.server.pool.doublequeue as dq

def startmessage(servname, port):
	servname = (servname + " Server").ljust(18)
	print "%s starting on port %d" % (servname, port)
