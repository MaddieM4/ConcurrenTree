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

	var min = Math.min(olds.length, news.length);
	// find start
	var start, end;
	for(var i=0; i<min; i++) {
		start = i;
		if (olds[i]!=news[i]) break;
	}
	// find end
	for(var i=0; i<min; i++) {
		end = olds.length-i;
		if (olds[end]!=news[news.length-i] || end == start || news.length-i == start) break;
	}
	var newend = news.length-(olds.length-end);
	return {'start':start, 'end':end, 'new':news.substr(start, newend-start)}
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
			if (togo == 0) {
				return {'address':'', 'position':i};
			}
			for (c in this.children[i]) {
				r = this.children[i][c].trace(togo);
				console.log(r)
				if (r['address'] == 'overflow') {
					togo -= r['position'];
				} else if (r['address'] == "") {
					return {'address':''+i+':'+c, 'position':r['position']};
				} else {
					return {'address':''+i+':'+c+'/'+r['address'], 'position':r['position']};
				}
			}
			if (i<this.value.length && !this.deletions[i]) {
				togo -= 1;
			}
		}
		return {'address':'overflow', 'position':togo};
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
bacon = cable.insert(3, "bacon");
console.log(cable.flatten());
