// ctree.js

// NETWORK --------------------------------------------------------------------------------------------------------------------------------------

function net_get(obj) {
	
}

// UTILITY --------------------------------------------------------------------------------------------------------------------------------------

function arrayfill(array, value, count) {
	for (var i=0;i<count;i++) {array.push(value)}
}

md5table = {};

function md5(text) {
	if (md5table[text] != undefined) {
		return md5table[text];
	} else {
		// temporary solution
		return text;
	}
}

// CTREE ----------------------------------------------------------------------------------------------------------------------------------------

function CTree(value) {
	this.value = value;
	this.hash = md5(value);
	this.deletions = []; arrayfill(this.deletions, false, value.length);
	this.markers = []; arrayfill(this.markers, {}, value.length+1);
	this.children = []; arrayfill(this.children, {}, value.length+1);

	this.insert = function(pos, childtext) {
		var child = new CTree(childtext);
		this.position[pos][child.hash] = child;
	}

	this.delete = function(pos) {
		self.deletions[pos] = true;
	}

	this.get = function(pos, hash) {
		return self.children[pos][hash];
	}

	this.flatten = function() {
		// Do only plaintext for now
		result = "";
		for (var i=0; i<this.value.length+1; i++) {
			for (c in this.children[i]) {
				console.log(c);
			}
			if (i<this.value.length && !this.deletions[i]) {
				result += this.value[i];
			}
		}
		return result;
	}

	this.trace = function(pos) {
		// returns {'address':string, 'position':int}
		// 'address' will == "overflow" if pos > len
		
	}

	this.resolve = function(addrstring) {
		parts = addrstring.split("/");
		if (parts == [""]) return this;
		tree = this;
		for (i in parts) {
			split = i.split(":");
			tree = tree.get(split[0], split[1]);
		}
		return tree;
	}
}

cable = new CTree("cable");
console.log(cable.flatten());
