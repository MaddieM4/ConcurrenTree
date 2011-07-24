// ctree.js :: CTree object and DocumentHandler object

// Dependencies: Util, MD5(util, bcp), View

function CTree(value) {
	// Action functions should return trees

	this.value = value;
	this.length = this.value.length
	this.hash = function() {return md5(this.value, bcp);}
	this.hash();
	this.deletions = []; arrayfill(this.deletions, function(){return false}, value.length);
	this.markers = []; arrayfill(this.markers, af_obj, value.length+1);
	this.children = []; arrayfill(this.children, af_obj, value.length+1);

	this.insert = function(pos, childtext) {
		// Insert and return a child tree

		var child = new CTree(childtext);
		this.children[pos][child.value] = child;
		return child;
	}

	this.delete = function(pos) {
		// Mark a character in this tree as deleted

		this.deletions[pos] = true;
		return this;
	}

	this.get = function(pos, value) {
		return this.children[pos][value];
	}

	this.flatten = function() {
		// Do only plaintext for now
		result = "";
		for (var i=0; i<this.value.length+1; i++) {
			for (c in this.children[i]) {
				result += this.children[i][c].flatten();
			}
			if (i<this.value.length && !this.deletions[i]) {
				result += this.value[i];
			}
		}
		return result;
	}

	this.trace = function(pos) {
		// Find an address/position pair for a textual position

		// returns {'address':address_js, 'position':int}
		// 'address' will == "overflow" if pos > len, 'position' will == overflow amount
		togo = pos;
		for (var i=0;i<this.value.length+1;i++) {
			for (var c in this.children[i]) {
				r = this.children[i][c].trace(togo);
				if (r['address'] == 'overflow') {
					togo -= r['position'];
				} else {
					addr = [[i,c]].concat(r['address']);
					return {'address':addr, 'position':r['position']};
				}
			}
			if (togo == 0 && !this.deletions[i]) {
				return {'address':[], 'position':i};
			}
			if (i<this.value.length && !this.deletions[i]) {
				togo -= 1;
			}
		}
		return {'address':'overflow', 'position':togo};
	}

	this.untrace = function(addr, pos) {
		// Find textual position of an address/position pair.

		var resolved = this.resolve(addr);
		if (resolved==undefined) {
			console.warn("untrace: Could not resolve address")
			return undefined;
		}
		result = this._ut(resolved, pos);
		if (result[1]) {
			return result[0];
		} else {
			console.warn("untrace: Position not found")
			return undefined;
		}
	}

	this._ut = function(targtree, pos) {
		// return [amount, done]
		var result = 0;
		var iam = (this == targtree);
		for (var i in this.children) {
			if (iam && i==pos) {
				return [result, true]
			}
			for (c in this.children[i]) {
				var ut = this.children[i][c]._ut(targtree, pos);
				result += ut[0];
				if (ut[1]) return [result, true]
			}
			if (i < this.value.length && !this.deletions[i]) result += 1;
		}
		return [result, false];
	}

	this.resolve = function(addr) {
		if (addr == []) return this;
		tree = this;
		for (i in addr) {
			split = addr[i]
			tree = tree.get(split[0], split[1]);
		}
		return tree;
	}

	this.kidscan = function() {
		var result = [];
		for (var i in this.children) {
			var index = {};
			for (var c in this.children[i]) {
				index[c] = this.children[i][c].kidscan()
			}
			result.push(index);
		}
		return result;
	}

	this.flatinsert = function(pos, value) {
		trace = this.trace(pos);
		return this.resolve(trace['address']).insert(trace['position'], value);
	}

	this.flatdelete = function(pos) {
		trace = this.trace(pos);
		return this.resolve(trace['address']).delete(trace['position']);
	}

	this.flatreplace = function(start, end, value) {
		if (start>end) return undefined;
		for (var i=end; i>=start; i--) this.flatdelete(i);
		return this.flatinsert(start, value);
	}

	this.proto = function() {
		// return a protocol representation of the tree

		var runstr = "";
		var rundel = -1;
		var deletions = [];
		var result = [];
		for (var pos in this.children){
			for (var c in this.children[pos]){
				if (runstr!="") {
					result.push(runstr);
					runstr = "";
				}
				result.push(this.children[pos][c].proto());
			}
			if (pos<this.length) {
				if (this.deletions[pos]) {
					if (rundel == -1) {
						rundel = int(pos);
					}
				} else {
					if (rundel != -1) {
						if (rundel == pos-1) deletions.push(rundel)
						else deletions.push([rundel, pos-1])
						rundel = -1;
					}
				}
				runstr += this.value[pos]
			}
		}
		if (runstr!="") result.push(runstr)
		if (rundel!=-1) {
			if (rundel == pos-1) deletions.push(rundel)
			else deletions.push([rundel, pos-1])
		}
		result.push(deletions);
		return result;
	}
}

function DocumentHandler(){
	// Stores lists of Views
	var self = this;
	this.contents = {};

	this.get = function(name, display) {
		if (!this.contains(name)) this.set(name, [new View(new CTree(""), name, display)]);
		return this.contents[name]
	}

	this.set = function(name, value) {
		this.contents[name] = value;
	}

	this.drop = function(name) {
		delete this.contents[name]
	}

	this.contains = function(name){
		return this.contents[name]!=undefined;
	}

	this.names = function() {
		result = [];
		for (i in self.contents) result.push(i);
		return result;
	}

	this.send = function(name, op){
		var views = self.get(name);
		for (var i in views) {
			views[i].netinput(op);
		}
	}

}
