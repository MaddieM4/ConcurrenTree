#!/usr/bin/python

''' 
The general-purpose BCP user-level interface. This is the Python backend,
which communicates with the graphical client frontend in ./jsclient.

All peer communication and mutual hosting is handled by Python, which will
be capable of direct P2P communication and the high-level management of a
Kademlia DHT. Once that is in place, we can start building ECP support, and
start branching out to support more DHT algorithms.

'''

import optparse

defaults = {
	1:{
		"peers":9090,
		"wsport":9091,
		"http":8080
	},
	2:{
		"peers":9092,
		"wsport":9093,
		"http":8081
	}

}

parser = optparse.OptionParser(description=''' 
Orchard is a BCP client with a web interface and
a Python server that runs in the background. It's
a reference implementation of the ConcurrenTree
concurrent text model.
''', version="Orchard v0.3")

parser.add_option("-p", "--peers", dest="peers", default=defaults[1]['peers'],
	help="The port you want to host on for peers")
parser.add_option("-w", "--websocket", dest="wsport", default=defaults[1]['wsport'],
	help="The port you want to host for websocket clients")
parser.add_option("-H", "--http", dest="http", default=defaults[1]['http'],
	help="HTTP host port")
parser.add_option("-b", "--browserless", dest="browser", action="store_true",
	help="Open orchard with no browser")
parser.add_option("-v", action="store_true", help="Print version")
#parser.add_option("-2", "--browserless", dest="browser", action="store_true",
#	help="Open orchard with no browser")
args, startpeers = parser.parse_args()

if args.v:
	parser.print_version()
	quit()

import webbrowser

from BCP.serverpool import ServerPool
from orchardserver import http, ws, peers
import storage

doc = storage.Storage()
auth = None
pool = ServerPool(doc, auth)

# add interface servers
pool.start(http.HTTP, port=args.http)
pool.start(ws.WebSocketServer, port=args.wsport)
# Start browser
if not args.browser:
	webbrowser.open("localhost:"+str(args.http))
# start notification icon
pass

# start background servers
pool.start(peers.Peers, port=args.peers)
#pool.start(orchardserver.HALP)
#pool.start(orchardserver.DHT)
try:
	pool.run()
except KeyboardInterrupt:
	print
	pool.close()
