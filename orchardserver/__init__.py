''' 
Wrappers that subclass BCP.PoolServer. This lets us run
our servers with the BCP.ServerPool framework.

There's a lot of useful and fairly general code in here,
so as always, feel free to copy it out for your own 
non-Orchard use.

'''

from BCP.serverpool import PoolServer

class Peers(PoolServer):
	pass

class HALP(PoolServer):
	pass

class DHT(PoolServer):
	''' By default, the Kademlia CTree hosting cloud. '''
	pass
