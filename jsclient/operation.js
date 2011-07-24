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

	this.pushinsert = function(address, pos, value){
		this.push([1,address,pos,value])
	}

	this.pushdelete = function(address, victims){
		this.push([0,address].concat(victims))
	}

	this.pushflatinsert = function(pos, value) {
		// pass
	}

	this.apply = function(tree, display) {
		display.lock();
		this.display(this.apply_tree(), display);
		display.unlock();
	}

	this.apply_tree = function(tree) {
		// returns an array of replacements
		var replacements = [];
		for (var i in this.instructions) {
			i = this.instructions[i];
			if (i[0] == 1) {
				// insertion
				var pos = tree.untrace(i[1], i[2]);
				replacements.push(pos, pos, i[3]);
				tree.resolve(i[1]).insert(i[2], i[3]);
			} else {
				// deletion
				var victims = i.slice(2);
				strike = function(del){
					var pos = tree.untrace(i[1], del);
					replacements.push(pos, pos+1,"");
					tree.resolve(i.address).delete(i.pos);
				}
				for (del in victims) {
					if (isArray(del)) {
						for (var deli=del[0];deli<del[1];deli++) strike(deli);
					} else {
						strike(del);
					}
				}
			}
		}
		return replacements;
	}

	this.display = function(replacements, display) {
		for (var i in replacements) {
			display.replace(i);
		}
	}

	this.serialize = function() {
		// return protocol string
		return "";
	}
}
