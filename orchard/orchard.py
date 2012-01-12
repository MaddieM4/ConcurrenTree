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
	"1":{
		"peers":9090,
		"sioport":9091,
		"http":8080,
		"icon":""
	},
	"2":{
		"peers":9190,
		"sioport":9191,
		"http":8180,
		"icon":"Red"
	},
	"3":{
		"peers":9290,
		"sioport":9291,
		"http":8280,
		"icon":"Blue"
	}

}

parser = optparse.OptionParser(description=''' 
Orchard is a BCP client with a web interface and
a Python server that runs in the background. It's
a reference implementation of the ConcurrenTree
concurrent text model.
''', version="Orchard v0.3")

parser.add_option("-p", "--peers", dest="peers", default=0,
	help="The port you want to host on for peers")
parser.add_option("-w", "--websocket", dest="sioport", default=0,
	help="The port you want to host for websocket clients")
parser.add_option("-H", "--http", dest="http", default=0,
	help="HTTP host port")
parser.add_option("-b", "--browserless", dest="browser", action="store_true",
	help="Open orchard with no browser")
parser.add_option("-v", action="store_true", help="Print version")
parser.add_option("-1", dest="portset", const="1", action="store_const", default="1",
	help="Use default port set")
parser.add_option("-2", dest="portset", const="2", action="store_const",
	help="Use secondary port set")
parser.add_option("-3", dest="portset", const="3", action="store_const",
	help="Use third port set")
args, startpeers = parser.parse_args()
parser.destroy()

#print args

parser.print_version()
if args.v:
	quit()

if args.portset:
	def default(argname):
		if getattr(args, argname)==0:
			setattr(args, argname, defaults[args.portset][argname])
	default("peers")
	default("sioport")
	default("http")

import gevent
from gevent import monkey; monkey.patch_all()
from server import http, sio#, icon, peers
from ConcurrenTree.util.storage.default import DefaultAuth

auth = DefaultAuth()

# add interface servers
s_http = http.HTTP(auth, port=args.http)
s_sio  = sio.SocketIOServer(port=args.sioport, auth=auth)
# Start browser
if not args.browser:
	s_http.open("/?ws=" + str(args.sioport))
# start notification icon
#pool.start(icon.IconServer, pool, logo=(args.portset and defaults[args.portset]['icon']) or "")

# start background servers
#peerserver = pool.start(peers.Peers, port=args.peers, docs = docs)

# Connect to cmdline peers
#for peer in startpeers:
#	peerserver.connect(peer)

servers = [s_http, s_sio]
greenlets = [gevent.spawn(x.run) for x in servers]

try:
	print "Starting servers"
	gevent.joinall(greenlets)
except KeyboardInterrupt:
	print "Closing servers"
	for x in servers:
		x.close()
	#gevent.joinall(greenlets, timeout=5)
