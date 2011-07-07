''' 
The general-purpose BCP user-level interface. This is the Python backend,
which communicates with the graphical client frontend in ./jsclient.

All peer communication and mutual hosting is handled by Python, which will
be capable of direct P2P communication and the high-level management of a
Kademlia DHT. Once that is in place, we can start building ECP support, and
start branching out to support more DHT algorithms.

'''

import optparse
import orchardlive

parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="port", default="9090",
	help="The port you want to host on for peers")
parser.add_option("-w", "--websocket", dest="wsport", default="9091",
	help="The port you want to host for websocket clients")
args, peers = parser.parse_args()

live = orchardlive.Live(args['port'], args['wsport'], peers)
live.run()
