// stream.js :: Stream functional protocol

// Dependencies: Buffer

/*
	Stream objects of any type connect an internet
	stream to the BCP parser in a predictable and
	universal way.

	BCP requests text with this.bcp_pull and puts
	text into the outward buffer with this.bcp_push.

	"Subclasses" must use these functions, but other
	than that, implementation is up to them.
*/

CTREE_STREAM_UNSTARTED = 0;
CTREE_STREAM_STARTED = 1;
CTREE_STREAM_CLOSED = 2;

function ctree_stream(self) {
	if (self==undefined) self = this;
	self.inbuffer = new Buffer();
	self.outbuffer = new Buffer();
	self.state == CTREE_STREAM_UNSTARTED;

	self.bcp_pull = function() {
		return this.inbuffer.read_all().join("");
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

	self.started = function(){return self.state==CTREE_STREAM_STARTED}
	self.closed = function(){return self.state==CTREE_STREAM_CLOSED}

	self.onpush = function(){}
	self.onconnect = function(){
		self.state = CTREE_STREAM_STARTED;
		self.stream_push('{"type":"error", "code":101}\x00')
	}
	self.onclose = function(){
		if (self.closed()) return;
		self.state = CTREE_STREAM_CLOSED;
		self.stream_push('{"type":"error", "code":100}\x00')
	}
}

function ws_stream(url){
	ctree_stream(this);
	var self = this;
	this.url = url;

	this.connect = function(url){
		this.socket = new WebSocket(url);

		this.socket.onopen = function(e){self.onconnect()};
		this.socket.onclose = function(e){self.onclose()};
		this.socket.onmessage = function(e){self.stream_push(e.data)};
		this.socket.error = function(e){alert(e)};
	};

	this.reconnect = function(){
		this.onclose();
		this.connect(this.url)
	};
	this.connect(this.url)

	this.onpush = function() {
		value = this.stream_pull()
		if (value != undefined) {
			this.socket.send(value)
		}
	}

}
