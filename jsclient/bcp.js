// bcp.js :: BCP parsing hub

function BCP(docs, stream, auth){
	this.docs = docs;
	this.stream = stream;
	this.auth = auth;
	this.buffer = ""

	this.cycle = function() {
		// Read network input
		var netin = this.stream.read_all();
		for (i in netin) this.buffer += netin[i];

		// Debuffer and apply messages
		var messages = this.buffer.split("\x00");
		this.buffer = message.pop()
		for (i in messages) {
			this.apply(messages[i]);
		}
	}

	this.apply = function(message) {
		// Parse JSON
		var msg;
		try {
			msg = JSON.parse(message)
		} catch (e) {
			// Bad JSON
			return
		}
	}

	this.error = function(code) {
		//TODO
	}
	this.thread = setInterval(this.cycle, 100);
}
