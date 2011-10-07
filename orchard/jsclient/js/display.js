(function() {
  var Display, context, workerurl;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  context = window;
  workerurl = "/js/displayworker.js";
  Display = (function() {
    function Display(docname, handler, immediate) {
      this.docname = docname;
      this.handler = handler;
      this.immediate = immediate;
      this.onwerror = __bind(this.onwerror, this);
      this.onwmessage = __bind(this.onwmessage, this);
      this.onwconnect = __bind(this.onwconnect, this);
      this.act = __bind(this.act, this);
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
    Display.prototype.act = function(callback) {
      var newcallback;
      newcallback = __bind(function() {
        callback(this);
        return this.unlock();
      }, this);
      return this.lock(newcallback);
    };
    Display.prototype.cursor = function(id, pos) {
      this.checklock();
      return this.worker.postMessage(["cursor", id, pos]);
    };
    Display.prototype.insert = function(value) {
      this.checklock();
      return this.worker.postMessage(["insert", value]);
    };
    Display.prototype["delete"] = function(amount) {
      this.checklock();
      return this.worker.postMessage(["delete", amount]);
    };
    Display.prototype.checklock = function() {
      if (!this.islocked || this.switching) {
        throw "Display not locked or in switching state";
      }
    };
    Display.prototype.onwconnect = function(e) {
      return this.ready = true;
    };
    Display.prototype.onwmessage = function(e) {
      var data, type;
      data = e.data;
      console.log("Display worker output: " + JSON.stringify(data));
      type = data[0];
      switch (type) {
        case "op":
          return this.internal(new Operation(data[1].instructions));
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
        case "lock":
          return this._onlock();
        case "unlock":
          return this._onunlock();
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
    Display.prototype.close = function() {
      return this.worker.postMessage(["close"]);
    };
    return Display;
  })();
  context.Display = Display;
}).call(this);
