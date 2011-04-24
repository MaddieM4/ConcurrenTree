// chainer.js

function Chainer(tree) {
	// A chaining wrapper for the tree. Call functions on it like a regular tree.
	// For properties, use mychain.tree.propertyname

	this.tree = tree;
	this.lastpos = undefined;
	this.startpos = undefined;
	this.chain = "";

	this.insert = function(pos, childtext) {this.apply(); return this.tree.insert(pos, childtext)}
	this.delete = function(pos) {this.apply(); return this.tree.delete(pos)}
	this.get = function(pos, hash) {this.apply(); return this.tree.get(pos, hash)}

	this.flatten = function() {this.apply(); return this.tree.flatten()}
	this.trace = function(pos) {this.apply(); return this.tree.trace(pos)}
	this.untrace = function(addr, pos) {this.apply(); return this.tree.untrace(addr, pos)}
	this.resolve = function(addrstring) {this.apply(); return this.tree.resolve(addrstring)}
	this.kidscan = function() {this.apply(); return this.tree.kidscan()}

	this.flatinsert = function(pos, value) {
		if (this.startpos == undefined) {
			this.startpos = pos;
			this.lastpos = pos;
			this.chain += value;
		} else if (pos == this.lastpos+1) {
			this.chain += value;
			this.lastpos = pos;
		} else {
			this.apply();
			this.tree.flatinsert(pos, value);
		}
	}

	this.flatdelete = function(pos) {
		if (this.startpost != undefined && pos == this.lastpos) {
			this.chain = this.chain.substr(0, this.chain.length-1);
		} else {
			this.apply();
			this.tree.flatdelete(pos);
		}
	}

	this.flatreplace = function(start, end, value) {this.apply(); return this.tree.flatreplace(start, end, value)}

	this.apply = function() {
		if (this.chain != "") {
			this.tree.flatinsert(this.startpos, this.chain);
			this.startpos = undefined;
			this.lastpos = undefined;
			this.chain = "";
		}
	}
}
