// operation.js

// Instruction format:
// {'type':'insert', 'address':string, 'pos':int, 'value':string}
// {'type':'delete', 'address':string, 'pos':int}

function Operation() {
	this.instructions = [];

	this.push = function(i) {
		this.instructions.push(i);
	}

	this.apply = function(tree, display) {
		display.lock();
		this.display(this.apply_tree(), display);
		display.unlock();
	}

	this.apply_tree = function(tree) {
		// returns an array of replacements
		var replacements = [];
		for (var i in self.instructions) {
			if (i.type == "insert") {
				var pos = tree.untrace(i.address, i.pos);
				replacements.push(pos, pos, i.value);
				tree.resolve(i.address).insert(i.pos, i.value);
			} else if (i.type == "delete") {
				var pos = tree.untrace(i.address, i.pos);
				replacements.push(pos, pos+1,"");				
				tree.resolve(i.address).delete(i.pos);
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