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

		// flush the stream buffer
		self.stream.onpush()
	}

	this.receive = function(message) {
		// Parse JSON
		var msg;
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
		self.select(name);
		this.docs.send(name, op);
		self.send(op.proto())
	}

	this.select = function(name) {
		self.send({"type":"select", "docname":name})
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
		}, 0:function(msg){
			console.log("error: unknown message type")
			self.error(401)
		}
	}

	this.ehandlers = {
		100:function(msg) {
			console.error("Connection broken")
		}, 101:function(msg){
			console.log("Connection started")
		}, 0:function(msg){
			console.error("Server error: "+JSON.stringify(msg))
		}
	}

	this.send = function(obj) {
		this.stream.bcp_push(JSON.stringify(obj)+"\x00")
	}

	this.error = function(code) {
		this.send({"type":"error", "code":code})
	}

	this.reconnect = function(){this.stream.reconnect()}
	this.thread = setInterval(function(){self.cycle()}, 100);
}
