// operation.js :: Operation class and Instruction processing

// Dependencies: none

/*
	Instruction format:

	[0, address, int, range] - Deletion, flexible number of args
	[1, address, pos, value] - Insertion, always 4
*/

function Operation() {
	this.instructions = [];

	this.push = function(i) {
		this.instructions.push(i);
	}

	this.push_list = function(array){
		for (i in array){
			this.push(array[i])
		}
	}

	this.pushinsert = function(address, pos, value){
		this.push([1,address,pos,value])
	}

	this.pushdelete = function(address, victims){
		this.push([0,address].concat(victims))
	}

	this.pushflatinsert = function(pos, value, tree) {
		var trace = tree.trace(pos);
		this.pushinsert(trace.address, trace.position, value)
	}

	this.pushflatdelete = function(pos, tree) {
		var trace = tree.trace(pos);
		this.pushdelete(trace.address, [trace.position])
	}

	this.apply = function(tree) {
		for (var i in this.instructions) {
			i = this.instructions[i];
			if (i[0] == 1) {
				// insertion
				tree.resolve(i[1]).insert(i[2], i[3]);
			} else {
				// deletion
				var victims = i.slice(2);
				strike = function(del){
					tree.resolve(i[1]).delete(del);
				}
				for (del in victims) {
					del = victims[del]
					if (isArray(del)) {
						for (var deli=del[0];deli<del[1];deli++) strike(deli);
					} else {
						strike(del);
					}
				}
			}
		}
	}

	this.replacements = function(tree) {
		// returns a series of replacements on the plaintext
		// represented by the tree.
		var temptree = tree.valueOf()
		results = []
		for (var i in this.instructions){
			var instr = this.instructions[i];
			if (instr[0]==1) {
				// Insertion
				var subaddr = instr[1].concat([[instr[2], instr[3]]])
				var resolved = temptree.resolve(subaddr)
				if (resolved==undefined){
					var pos = temptree.untrace(instr[1],instr[2]);
					results.push([pos,pos,instr[3]]);
					temptree.flatinsert(pos, instr[3])
				}
			} else {
				// Deletion
				var addr = instr[1]
				var target = temptree.resolve(addr)
				var victims = instr.concat().slice(2)
				for (v in victims){
					if (!isArray(victims[v])){
						victims[v] = [victims[v]]
					} else {
						victims[v] = range(victims[v][0],victims[v][1]+1);
					}
					for (x in victims[v]){
						x = victims[v][x];
						if (!target.deletions[x]) {
							var pos = temptree.untrace(addr,x)
							results.push([pos,pos+1, ""])
							target.delete(x)
						}
					}
				}
			}
		}
		return results
	}

	this.display = function(replacements, display) {
		for (var i in replacements) {
			display.replace(i);
		}
	}

	this.serialize = function() {
		// return protocol string
		return JSON.stringify(this.proto());
	}

	this.proto = function(){
		// return protocol object
		return {"type":"op","instructions":this.instructions}
	}
}

function opfromprototree(proto, addr){
	if (addr==undefined) addr=[];
	var tree;
	if (isArray(proto)){
		tree = new treefromprototree(proto);
	} else {
		tree = proto;
	}
	var op = new Operation()
	for (pos in tree.children){
		for (c in tree.children[pos]){
			var child = tree.children[pos][c]
			var childaddr = addr.concat([[pos, child.value]]);

			op.pushinsert(addr, pos, child.value);
			op.pushdelete(childaddr, child.deletions);

			subop = opfromprototree(child, childaddr)
			op.push_list(subop.instructions)	
		}
	}
	return op;
}

function treefromprototree(proto){
	this.deletions = proto.pop()
	this.value = "";
	this.children = {}
	for (i in proto) {
		if (isArray(proto[i])) {
			var pos = this.value.length;
			if (this.children[pos]==undefined) this.children[pos]=[]
			this.children[pos].push(new treefromprototree(proto[i]))
		} else {
			this.value += proto[i]
		}
	}	
}
