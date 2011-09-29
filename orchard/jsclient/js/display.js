(function() {
  var Display, worker, workerurl;

  worker = "\nvar window = {}\nimportScripts('/js/util.js');\nserial = window.serial;\nimportScripts('js/ctree.js');\nCTree = window.CTree\n\nlog = function(obj) {postMessage(['log',obj])}\ncursors = {0:0};\nlocked = false;\ntree = CTree(\"\") // The document for this display\n\nfunction pushCursors(){\n    postMessage([\"cursor\", cursors]);\n}\n\nfunction rewrite(){\n    postMessage([\"rewrite\",tree.flatten()]);\n}\n\nfunction insert(value){\n    var pos, t, node;\n    pos = cursors[0];\n    t = tree.trace(pos);\n\n    // convert to operations system later\n    node = tree.resolve(t.addr);\n    node.insert(t.pos, value);\n    rewrite();\n}\n\nfunction deleteone(pos) {\n    t = tree.trace(pos);\n\n    // convert to operations system later\n    node = tree.resolve(t.addr);\n    node.delete(t.pos);    \n}\n\nfunction deletemany(amount){\n    var start, times, pos;\n    pos = cursors[0];\n    if (amount==0) return;\n    if (amount > 0) {start=pos, times=amount}\n    if (amount < 0) {start=pos+amount, times=-amount}\n    for (var i =0; i<times;i++){\n        deleteone(start);\n    }\n    rewrite();\n}\n\nfunction operate(op) {\n// work on this later\n}\n\nonmessage = function(e){\n    data = e.data;\n    type = data[0];\n    switch(type){\n      case \"cursor\":\n        var id = data[1], value = data[2];\n        cursors[id] = value;\n        return postMessage([\"cursor\", {id:value}]);\n      case \"insert\": return insert(data[1]);\n      case \"delete\": return deletemany(data[1]);\n      case \"op\": return operate(data[1]);\n      case \"lock\":\n        locked = true; break;\n      case \"unlock\":\n        locked = false; break;\n      default:\n        return log(\"Unknown message type:\"+type.toString());\n    }\n}\n";

  workerurl = blobworker.createBlobURL(worker);

  Display = (function() {

    function Display(docname, handler, immediate) {
      this.docname = docname;
      this.handler = handler;
      this.immediate = immediate;
      this.islocked = false;
      this.switching = false;
      this.ready = false;
      this.worker = new Worker(workerurl);
      this.worker.onconnect = this.onwconnect;
      this.worker.onmessage = this.onwmessage;
      this.worker.onerror = this.onwerror;
      this.onwrite = null;
      this.ondelete = null;
      this.onmove = null;
      this.onrewrite = null;
      this.onlock = null;
      this.onunlock = null;
      this.handler.register(this);
    }

    Display.prototype.external = function(op, name) {
      if (name === this.docname) return this.apply(op);
    };

    Display.prototype.internal = function(op) {
      return this.handler.local(op, this.docname);
    };

    Display.prototype.apply = function(op) {
      return this.worker.postMessage(["op", op]);
    };

    Display.prototype.lock = function(callback) {
      if (this.switching) throw "Display in switching state, cannot lock";
      this.switching = true;
      if (callback != null) this.onlock = callback;
      return this.worker.postMessage(["lock"]);
    };

    Display.prototype.unlock = function(callback) {
      if (this.switching) throw "Display in switching state, cannot unlock";
      this.switching = true;
      if (callback != null) this.onunlock = callback;
      return this.worker.postMessage(["unlock"]);
    };

    Display.prototype.cursor = function(id, pos) {
      if (this.islocked || this.switching) {
        throw "Display not locked or in switching state";
      }
      return this.worker.postMessage(["cursor", id, pos]);
    };

    Display.prototype.insert = function(value) {
      if (this.islocked || this.switching) {
        throw "Display not locked or in switching state";
      }
      return this.worker.postMessage(["insert", value]);
    };

    Display.prototype["delete"] = function(amount) {
      if (this.islocked || this.switching) {
        throw "Display not locked or in switching state";
      }
      return this.worker.postMessage(["delete", amount]);
    };

    Display.prototype.onwconnect = function(e) {
      return this.ready = true;
    };

    Display.prototype.onwmessage = function(e) {
      var data, type;
      data = e.data;
      type = data[0];
      switch (type) {
        case "op":
          return this.internal(data[1]);
        case "log":
          return console.log(data[1]);
        case "lock":
          return this._onlock();
        case "unlock":
          return this._onunlock();
        case "cursor":
        case "rewrite":
        case "write":
        case "delete":
          return this.event(data);
      }
    };

    Display.prototype.onwerror = function(e) {
      console.error(e);
      return this.ready = false;
    };

    Display.prototype.event = function(message) {
      switch (message[0]) {
        case "cursor":
          return typeof this.onmove === "function" ? this.onmove(message[1]) : void 0;
        case "write":
          return this.onwrite(message[1], message[2]);
        case "delete":
          return typeof this.ondelete === "function" ? this.ondelete(message[1], message[2]) : void 0;
        case "rewrite":
          return typeof this.onrewrite === "function" ? this.onrewrite(message[1]) : void 0;
      }
    };

    Display.prototype._onlock = function() {
      this.switching = false;
      this.islocked = true;
      return typeof this.onlock === "function" ? this.onlock() : void 0;
    };

    Display.prototype._onunlock = function() {
      this.switching = false;
      this.islocked = false;
      return typeof this.onunlock === "function" ? this.onunlock() : void 0;
    };

    return Display;

  })();

  window.Display = Display;

}).call(this);
