(function() {
  var BCP, context;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  context = window;
  BCP = (function() {
    function BCP(stream, auth) {
      this._handle = __bind(this._handle, this);
      this.errorhandle = __bind(this.errorhandle, this);
      this.handle = __bind(this.handle, this);
      this.recieve = __bind(this.recieve, this);      this.docs = [];
      this.stream = stream;
      this.stream.onmessage = this.recieve;
      this.auth = auth;
      this.selected = "";
      this.subscriptions = {};
      this.bflag = {};
      this.other = {
        selected: "",
        subscriptions: {}
      };
      this.getcached = {};
    }
    BCP.prototype.recieve = function(message) {
      var msg;
      message = message.slice(0, -1);
      this.log("recieving", message);
      console.log("Incoming message: " + message);
      try {
        msg = JSON.parse(message);
      } catch (error) {
        if (typeof this.log === "function") {
          this.log("error", "bad message from remote end");
        }
      }
      this.handle(msg);
    };
    BCP.prototype.local = function(op, name) {
      /*
              Process a locally-generated op
      */
      console.log("selecting");
      this.select(name);
      console.log("sending local");
      this.docssend(name, op);
      console.log("sending proto");
      return this.send(op.proto());
    };
    BCP.prototype.select = function(name) {
      assert(typeof name === "string", "Docnames must be a string");
      if (name === this.selected) return;
      this.send({
        "type": "select",
        "docname": name
      });
      return this.selected = name;
    };
    BCP.prototype.get = function(name) {
      /*
              recieve or sync a document
              does not broadcast
      */
      if (name === void 0) name = this.selected;
      assert(typeof name === "string", "Docnames must be a string");
      if (this.getcached[name] === void 0) {
        this.getcached[name] = [[]];
        return this.load(name);
      } else {
        return this.sync(name);
      }
    };
    BCP.prototype.load = function(name) {
      this.select(name);
      return this.send({
        type: "get",
        address: []
      });
    };
    BCP.prototype.broadcast = function(name) {
      /*
              Send a loaded document to docs as an operation, 
              or flag for it to happen when get returns
      */

      var op;
      if (name === void 0) name = this.selected;
      assert(typeof name === "string", "Docnames must be a string.");
      if (this.getcached[name] === void 0) {
        return this.bflag[name] = true;
      } else {
        op = new Operation([]);
        op.fromTree([], CTreeFromProto(this.getcached[name]));
        return this.docssend(op, name);
      }
    };
    BCP.prototype.sync = function(name) {
      if (name === void 0) name = this.selected;
      this.select(name);
      return this.send({
        "type": "check",
        "eras": 0
      });
    };
    BCP.prototype.docssend = function(op, name) {
      var doc, _i, _len, _ref, _results;
      _ref = this.docs;
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        doc = _ref[_i];
        _results.push(doc.external(op, name));
      }
      return _results;
    };
    BCP.prototype.register = function(display) {
      return this.docs.push(display);
    };
    BCP.prototype.handle = function(message) {
      return this._handle(message, message.type, this.handlers);
    };
    BCP.prototype.errorhandle = function(message) {
      return this._handle(message, message.code, this.ehandlers);
    };
    BCP.prototype._handle = function(message, type, handlerset) {
      var f;
      f = handlerset[type];
      if (f === void 0) f = handlerset[0];
      if (!(message.docname != null)) message.docname = this.other.selected;
      return f(this, message);
    };
    BCP.prototype.handlers = {
      "select": function(self, message) {
        return self.other.selected = message.docname;
      },
      "hashvalue": function(self, message) {
        return md5table[message.value] = message.hashvalue;
      },
      "error": function(self, message) {
        return self.errorhandle(message);
      },
      "tree": function(self, message) {
        self.getcached[message.docname] = message.value;
        if (self.bflag[message.docname]) {
          self.broadcast(message.docname);
          return self.bflag[message.docname] = false;
        }
      },
      0: function(self, message) {
        console.log("error: unknown message type");
        return self.error(401);
      }
    };
    BCP.prototype.ehandlers = {
      100: function(self, message) {
        self.log("connection", "broken");
        return console.error("Connection broken");
      },
      101: function(self, message) {
        return self.log("connection", "started");
      },
      0: function(self, message) {
        var m;
        m = JSON.stringify(message);
        self.log("server error", m);
        return console.error("Server error: " + m);
      }
    };
    BCP.prototype.send = function(obj) {
      var s;
      s = JSON.stringify(obj);
      this.log("sending", s);
      return this.stream.send(s);
    };
    BCP.prototype.error = function(code) {
      return this.send({
        "type": "error",
        "code": code
      });
    };
    BCP.prototype.log = function(headline, detail) {};
    BCP.prototype.reconnect = function() {
      return this.stream.reconnect();
    };
    return BCP;
  })();
  context.BCP = BCP;
}).call(this);
