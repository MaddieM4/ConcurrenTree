// bcp.js :: BCP parsing hub

// Dependencies: CTree, Stream

function BCP(docs, stream, auth){
	this.docs = docs;
	this.stream = stream;
	this.auth = auth;
	this.buffer = ""
	var self = this;

	this.cycle = function() {
		// Read network input
		this.buffer += this.stream.bcp_pull();

		// Debuffer and apply messages
		var messages = this.buffer.split("\x00");
		this.buffer = messages.pop()
		for (i in messages) {
			this.receive(messages[i]);
		}

		// Update displays
		docs.cycle()

		// flush the stream buffer
		self.stream.onpush()
	}

	this.receive = function(message) {
		// Parse JSON
		var msg;
		self.log("recieving", message)
		console.log("Incoming message: "+message)
		try {
			msg = JSON.parse(message)
			this.handle(msg)
		} catch (e) {
			// Bad JSON
			return
		}
	}

	this.local = function(op, name) {
		console.log("selecting")
		self.select(name);
		console.log("sending local")
		this.docs.send(name, op);
		console.log("sending proto")
		self.send(op.proto())
	}

	this.select = function(name) {
		if (name==undefined){console.error("Cannot select docname of undefined"); return}
		self.send({"type":"select", "docname":name})
	}

	this.getcached = {}
	this.get = function(name) {
		// returns a prototree
		if (this.getcached[name]==undefined){
			self.select(name);
			self.send({"type":"get", "tree":0})
		} else {
			self.docs.send(this.getcached[name])
			return this.getcached[name]
		}
	}

	this.handle = function (msg){
		this._handle(msg, msg.type, this.handlers);
	}

	this.errorhandle = function (msg){
		this._handle(msg, msg.code, this.ehandlers);
	}

	this._handle = function(msg, type, hset) {
		func = hset[type];
		if (func==undefined) func = hset[0];
		func(msg)
	}

	this.handlers = {
		"hashvalue":function(msg){
			md5table[msg.value] = msg.hashvalue;
		}, "error":function(msg) {
			self.errorhandle(msg)
		}, "era":function(msg) {
			self.getcached[msg.docname] = msg.tree;
			self.docs.send(msg.docname, opfromprototree(msg.tree))
		}, 0:function(msg){
			console.log("error: unknown message type")
			self.error(401)
		}
	}

	this.ehandlers = {
		100:function(msg) {
			self.log("connection", "broken")
			console.error("Connection broken")
		}, 101:function(msg){
			self.log("connection", "started")
			console.log("Connection started")
		}, 0:function(msg){
			var str = JSON.stringify(msg)
			self.log("server error", str)
			console.error("Server error: "+str)
		}
	}

	this.send = function(obj) {
		var str = JSON.stringify(obj)
		self.log("sending", str)
		this.stream.bcp_push(str+"\x00")
	}

	this.error = function(code) {
		this.send({"type":"error", "code":code})
	}

	this.log = function(headline, detail){
	}

	this.reconnect = function(){this.stream.reconnect()}
	this.thread = setInterval(function(){self.cycle()}, 100);
}
