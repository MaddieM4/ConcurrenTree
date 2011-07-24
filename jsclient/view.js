// view.js :: A high-level representation of a display/tree pair

// Dependencies: Buffer, BCP

function View(tree, name, display){
	this.tree = tree;
	this.name = name;
	this.display = display;

	this.netbuffer = new Buffer(); // Input from BCP
	// Input from user is either applied immediately or buffered by display

	this.netinput = function(op){this.netbuffer.write(op)}

	// flat functions for display convenience (TODO: chaining)

	this.delete = function(start, end) {
		for (var pos=start; start<=end; start++){
			bcp.local(this.tree.flatdelete(pos), this.name);
		}
	}

	this.insert = function(pos, value) {
		bcp.local(this.tree.flatinsert(pos, value), this.name);
	}

	this.update = function(){
		if (this.display==undefined) return this.update_displayless();
		this.display.lock()
		var netops = this.netbuffer.read_all();
		for (var i in netops){
			var op = netops[i];
			var reps = op.replacements(this.tree);
			for (var i in reps) {
				var rep = reps[i]
				display.replace(rep[0],rep[1],rep[2]);
			}
			op.apply(this.tree)
		}
		this.display.unlock()
	}

	this.update_displayless = function() {
		var netops = this.netbuffer.read_all();
		for (var i in netops) netops[i].apply(this.tree)
	}
}
