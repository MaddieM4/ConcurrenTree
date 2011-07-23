// buffer.js :: Analagous to Python Queue

// Dependencies: none

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

	this.read_all = function() {
		var result = [];
		while (true){
			var value = this.read();
			if (value==undefined) return result;
			result.push(value);
		}
	}
}
