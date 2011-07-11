''' 
The general-purpose BCP user-level interface. This is the Python backend,
which communicates with the graphical client frontend in ./jsclient.

All peer communication and mutual hosting is handled by Python, which will
be capable of direct P2P communication and the high-level management of a
Kademlia DHT. Once that is in place, we can start building ECP support, and
start branching out to support more DHT algorithms.

'''

import optparse
import webbrowser

import BCP
import orchardserver
import storage

parser = optparse.OptionParser()
parser.add_option("-p", "--peers", dest="peers", default="9090",
	help="The port you want to host on for peers")
parser.add_option("-w", "--websocket", dest="wsport", default="9091",
	help="The port you want to host for websocket clients")
parser.add_option("-H", "--http", dest="http", default="80",
	help="HTTP host port")
args, peers = parser.parse_args()

doc = storage.Storage()
auth = None
pool = BCP.ServerPool(doc, auth)

# add interface servers
pool.start(orchardserver.HTTP, port=args['http'])
pool.start(orchardserver.WebSocket, port=args['wsport'])
# Start browser
webbrowser.open("localhost:"+str(args['http']))
# start notification icon
pass

# start background servers
pool.start(orchardserver.Peers, port=args['peers'])
pool.start(orchardserver.HALP)
pool.start(orchardserver.DHT)
pool.run()
