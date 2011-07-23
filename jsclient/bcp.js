// bcp.js :: BCP parsing hub

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
		console.log(message)
		try {
			msg = JSON.parse(message)
			this.handle(msg)
		} catch (e) {
			// Bad JSON
			return
		}
	}

	this.handle = function (msg){
		func = this.handlers[msg.type];
		if (func==undefined) {
			console.log("error: unknown message type")
			this.error(401)
		} else {
			func(msg)
		}
	}

	this.handlers = {
		"hashvalue":function(msg){
			md5table[msg.value] = msg.hashvalue;
		}, "error":function(msg) {
			console.log("Server error: "+JSON.stringify(msg))
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
