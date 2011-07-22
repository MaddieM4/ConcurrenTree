// bcp.js :: BCP parsing hub

function BCP(docs, stream, auth){
	this.docs = docs;
	this.stream = stream;
	this.auth = auth;
	this.buffer = ""

	this.cycle = function() {
		// Read network input
		this.buffer += this.stream.bcp_pull();

		// Debuffer and apply messages
		var messages = this.buffer.split("\x00");
		this.buffer = messages.pop()
		for (i in messages) {
			this.apply(messages[i]);
		}

		// flush the stream buffer
		self.stream.onpush()
	}

	this.apply = function(message) {
		// Parse JSON
		var msg;
		console.log(message)
		try {
			msg = JSON.parse(message)
		} catch (e) {
			// Bad JSON
			return
		}
	}

	this.send = function(obj) {
		this.stream.bcp_push(JSON.stringify(obj)+"\x00")
	}

	this.error = function(code) {
		//TODO
	}
	self = this;
	this.thread = setInterval(function(){self.cycle()}, 100);
}
