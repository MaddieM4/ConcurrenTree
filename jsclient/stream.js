// stream.js :: Stream functional protocol

/*
	Stream objects of any type connect an internet
	stream to the BCP parser in a predictable and
	universal way.

	BCP requests text with this.bcp_pull and puts
	text into the outward buffer with this.bcp_push.

	"Subclasses" must use these functions, but other
	than that, implementation is up to them.
*/

function Buffer() {
	this.readposition = 0;
	this.writeposition = 0;
	this._contents = {};
	this.readlock = false;

	this.write = function(value) {
		var pos = ++this.writeposition;
		this._contents[pos-1] = value;
	}

	this.read = function() {
		if (this.readlock) return undefined;
		this.readlock = true;
		var read = this.readposition;
		var write = this.writeposition;
		var result = undefined;
		if (read<write) {
			result = this._contents[read]
			this.readposition++;
		}
		this.readlock = false;
		return result;
	}
}

function ctree_stream(self) {
	if (self==undefined) self = this;
	self.inbuffer = new Buffer();
	self.outbuffer = new Buffer();

	self.bcp_pull = function() {
		return this.inbuffer.read();
	}

	self.bcp_push = function(text) {
		self.outbuffer.write(text)
		self.onpush()
	}

	self.stream_push = function(text){
		self.inbuffer.write(text);
	}

	self.stream_pull = function(){
		return self.outbuffer.read()
	}

	self.onpush = function(){}
	self.onconnect = function(){
		// Use 1XX Connection notice
	}
	self.onclose = function(){
		// Use 1XX Connection notice
	}
}

function ws_stream(url){
	ctree_stream(this);
	this.socket = new WebSocket(url);
	this.onpush = function() {
		value = this.stream_pull()
		if (value != undefined) {
			this.socket.send(value)
		}
	}

	var stream_push = this.stream_push;

	this.socket.onconnect = function(){this.onconnect()};
	this.socket.onclose = function(){this.onclose()};
	this.socket.onmessage = function(e){stream_push(e.data)};
	this.socket.error = function(e){alert(e)};
}
