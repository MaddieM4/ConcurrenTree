// view.js :: A high-level representation of a display/tree pair

// Dependencies: Buffer, BCP

function View(tree, name, display){
	this.tree = tree;
	this.name = name;
	this.display = display;
	//bcp.get(this.name);

	this.netbuffer = new Buffer(); // Input from BCP
	// Input from user is either applied immediately or buffered by display

	this.netinput = function(op){this.netbuffer.write(op)}

	// flat functions for display convenience (TODO: chaining)

	this.delete = function(start, end) {
		if (end==undefined) end = start;
		var op = new Operation()
		for (var pos=start; pos<=end; pos++){
			op.pushflatdelete(pos,this.tree)
		}
		console.log(op)
		op.apply(tree)
		bcp.local(op, this.name);
	}

	this.insert = function(pos, value) {
		var op = new Operation()
		op.pushflatinsert(pos,value,this.tree)
		op.apply(tree)
		bcp.local(op, this.name);
	}

	this.value = function(){
		return this.tree.flatten()
	}

	this.update = function(){
		if (this.display==undefined) {
			// console.log("No display")
			return this.update_displayless();
		}
		var netops = this.netbuffer.read_all();
		if (netops.length>0){
			this.display.lock()
			for (var i in netops){
				var op = netops[i];
				console.log(op);
				if ("replace" in this.display) {
					var reps = op.replacements(this.tree);
					console.log(reps)
					for (var i in reps) {
						var rep = reps[i]
						this.display.replace(rep[0],rep[1],rep[2]);
					}
				}
				op.apply(this.tree)
			}
			if ("rewrite" in this.display) {
				this.display.rewrite(this.value())
			}
			this.display.unlock()
		}
	}

	this.update_displayless = function() {
		var netops = this.netbuffer.read_all();
		for (var i in netops) {
			netops[i].apply(this.tree);
		}
	}
}
