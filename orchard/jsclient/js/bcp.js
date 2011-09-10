(function() {
  var BCP;
  BCP = (function() {
    function BCP(docs, stream, auth) {
      this.docs = docs;
      this.stream = stream;
      this.auth = auth;
      this.buffer = "";
      this.selected = "";
      this.subscriptions = {};
      this.bflag = {};
      this.other = {
        selected: "",
        subscriptions: {}
      };
      this.getcached = {};
    }
    BCP.prototype.cycle = function() {
      var m, messages, _i, _len;
      this.buffer += this.stream.bcp_pull();
      messages = this.buffer.split("\x00");
      this.buffer = messages.pop();
      for (_i = 0, _len = messages.length; _i < _len; _i++) {
        m = messages[_i];
        this.recieve(m);
      }
      this.docs.cycle();
      return this.stream.onpush();
    };
    BCP.prototype.recieve = function(message) {
      var msg;
      this.log("recieving", message);
      console.log("Incoming message: " + message);
      try {
        msg = JSON.parse(message);
        this.handle(msg);
      } catch (error) {

      }
    };
    BCP.prototype.local = function(op, name) {
      console.log("selecting");
      this.select(name);
      console.log("sending local");
      this.docs.send(name, op);
      console.log("sending proto");
      return this.send(op.proto());
    };
    BCP.prototype.select = function(name) {
      assert(isString(name), "Docnames must be a string");
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
      assert(isString(name), "Docnames must be a string");
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
        type: get,
        tree: 0
      });
    };
    BCP.prototype.broadcast = function(name) {
      /*
              Send a loaded document to docs as an operation, 
              or flag for it to happen when get returns
      */
      if (name === void 0) name = this.selected;
      assert(isString(name), "Docnames must be a string.");
      if (this.getcached[name] === void 0) {
        return this.bflag[name] = true;
      } else {
        return this.docs.send(name, opfromprototree(this.getcached[name]));
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
      return f(message);
    };
    BCP.prototype.handlers = {
      "hashvalue": function(message) {
        return md5table[message.value] = message.hashvalue;
      },
      "error": function(message) {
        return this.errorhandle(message);
      },
      "era": function(message) {
        this.getcached[message.docname] = message.tree;
        if (this.bflag[message.docname]) {
          this.broadcast(message.docname);
          return this.bflag[message.docname] = false;
        }
      },
      0: function(message) {
        console.log("error: unknown message type");
        return this.error(401);
      }
    };
    BCP.prototype.ehandlers = {
      100: function(message) {
        this.log("connection", "broken");
        return console.error("Connection broken");
      },
      101: function(message) {
        return this.log("connection", "started");
      },
      0: function(message) {
        var m;
        m = JSON.stringify(message);
        this.log("server error", m);
        return console.error("Server error: " + m);
      }
    };
    BCP.prototype.send = function(obj) {
      var s;
      s = JSON.stringify(obj);
      this.log("sending", s);
      return this.stream.bcp_push(s + "\x00");
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
    BCP.prototype.thread = setInterval((function() {
      return this.cycle;
    }), 100);
    return BCP;
  })();
}).call(this);
