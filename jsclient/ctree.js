// ctree.js

// NETWORK --------------------------------------------------------------------------------------------------------------------------------------

function net_get(obj) {
	
}

// UTILITY --------------------------------------------------------------------------------------------------------------------------------------

function arrayfill(array, value, count) {
	for (var i=0;i<count;i++) {array.push(value(i))}
}

function af_obj(id) {
	return {};
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

function textdiff(olds, news) {
	// simplistic algorithm that assumes a pattern of same|different|same where any section could be length 0
	// returns a replacement object ({'start':int, 'end':int, 'new':string})
	// replacement objects ALWAYS use coordinates in old string space

	if (olds==news) return undefined;
	var min = Math.min(olds.length, news.length);
	// find start
	console.log("start")
	var start=0, end=olds.length-1;
	for(var i=0; i<min; i++) {
		console.log(olds[i]+news[i])
		start = i;
		if (olds[i]!=news[i]) break;
	}
	// find end
	console.log("end")
	for(var i=1; i<min; i++) {
		end = olds.length-i;
		console.log(olds[end]+news[news.length-i])
		console.log("end="+end+" start="+start+" i="+i);
		if (olds[end]!=news[news.length-i] || end == start || news.length-i == start) break;
	}
	var newend = news.length-(olds.length-end);
	return {'start':start, 'end':end, 'new':news.substr(start, newend-start)}
}

function read(f,g,i) {
	// Every i milliseconds, calls f, which should return either undefined or a replacement object.
	// Function g should accept replacement objects.
	return setInterval(function() {
		x=f();
		if (x!=undefined) g(x);
	}, i)
}

// CTREE ----------------------------------------------------------------------------------------------------------------------------------------

function CTree(value) {
	this.value = value;
	this.hash = md5(value);
	this.deletions = []; arrayfill(this.deletions, function(){return false}, value.length);
	this.markers = []; arrayfill(this.markers, af_obj, value.length+1);
	this.children = []; arrayfill(this.children, af_obj, value.length+1);

	this.insert = function(pos, childtext) {
		var child = new CTree(childtext);
		this.children[pos][child.hash] = child;
		return child;
	}

	this.delete = function(pos) {
		this.deletions[pos] = true;
		return this;
	}

	this.get = function(pos, hash) {
		return this.children[pos][hash];
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
		// returns {'address':string, 'position':int}
		// 'address' will == "overflow" if pos > len, 'position' will == overflow amount
		togo = pos;
		for (var i=0;i<this.value.length+1;i++) {
			for (var c in this.children[i]) {
				r = this.children[i][c].trace(togo);
				if (r['address'] == 'overflow') {
					togo -= r['position'];
				} else if (r['address'] == "") {
					return {'address':''+i+':'+c, 'position':r['position']};
				} else {
					return {'address':''+i+':'+c+'/'+r['address'], 'position':r['position']};
				}
			}
			if (togo == 0 && !this.deletions[i]) {
				return {'address':'', 'position':i};
			}
			if (i<this.value.length && !this.deletions[i]) {
				togo -= 1;
			}
		}
		return {'address':'overflow', 'position':togo};
	}

	this.untrace = function(addr, pos) {
		var resolved = this.resolve(addr);
		if (resolved==undefined) return undefined;
		return this._ut(resolved, pos)[0];
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

	this.resolve = function(addrstring) {
		if (addrstring == "") return this;
		parts = addrstring.split("/");
		tree = this;
		for (i in parts) {
			split = parts[i].split(":");
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
}