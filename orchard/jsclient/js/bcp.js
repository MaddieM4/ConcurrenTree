(function() {
  var BCP, context;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  context = window;

  BCP = (function() {

    function BCP(stream, auth) {
      this.stream = stream;
      this.auth = auth;
      this.unsubscribe = __bind(this.unsubscribe, this);
      this.subscribe = __bind(this.subscribe, this);
      this.disconnect = __bind(this.disconnect, this);
      this.connect = __bind(this.connect, this);
      this._handle = __bind(this._handle, this);
      this.errorhandle = __bind(this.errorhandle, this);
      this.handle = __bind(this.handle, this);
      this.recieve = __bind(this.recieve, this);
      this.docs = [];
      this.stream.on('message', this.recieve);
      this.stream.on('connect', this.connect);
      this.stream.on('disconnect', this.disconnect);
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
      */      console.log("selecting");
      this.select(name);
      console.log("sending local");
      this.docssend(op, name);
      console.log("sending proto");
      return this.send(op.proto());
    };

    BCP.prototype.foreign = function(op, name) {
      /*
              Process a remotely-generated op
      */      return this.docssend(op, name);
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
      */      if (name === void 0) name = this.selected;
      assert(typeof name === "string", "Docnames must be a string");
      if (this.getcached[name] === void 0) {
        this.getcached[name] = [[]];
        return this.load(name);
      } else {
        return this.sync(name);
      }
    };

    BCP.prototype.load = function(name) {
      return this.send({
        "type": "load",
        "docname": name
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
      "op": function(self, message) {
        var op;
        op = new Operation(message.instructions);
        return self.foreign(op, self.other.selected);
      },
      "subscribe": function(self, message) {
        var i, _i, _len, _ref, _results;
        if (message.docnames.length === 0) {
          return self.other.subscriptions[self.other.selected] = true;
        } else {
          _ref = message.docnames;
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            i = _ref[_i];
            _results.push(self.other.subscriptions[i] = true);
          }
          return _results;
        }
      },
      "unsubscribe": function(self, message) {
        var i, _i, _len, _ref, _results;
        if (messages.docnames != null) {
          if (messages.docnames.length === 0) {
            return self.other.subscriptions = {};
          } else {
            _ref = messages.docnames;
            _results = [];
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              i = _ref[_i];
              _results.push(self.other.subscriptions[i] = false);
            }
            return _results;
          }
        } else {
          return self.other.subscriptions[self.other.selected] = false;
        }
      },
      "error": function(self, message) {
        return self.errorhandle(message);
      },
      "extensions": function(self, message) {
        return self.log("extensions", message.available.toString());
      },
      0: function(self, message) {
        console.log("error: unknown message type");
        return self.error(401);
      }
    };

    BCP.prototype.ehandlers = {
      0: function(self, message) {
        var m;
        m = JSON.stringify(message);
        self.log("server error", m);
        return console.error("Server error: " + m);
      }
    };

    BCP.prototype.connect = function() {
      return this.log("connection", "started");
    };

    BCP.prototype.disconnect = function() {
      this.log("connection", "broken");
      return console.error("Connection broken");
    };

    BCP.prototype.subscribe = function(name, type) {
      var i, _i, _len, _results;
      if (typeof name === "string") name = [name];
      this.send({
        "type": "subscribe",
        "subtype": type,
        "docnames": name
      });
      _results = [];
      for (_i = 0, _len = name.length; _i < _len; _i++) {
        i = name[_i];
        _results.push(this.subscriptions[i] = true);
      }
      return _results;
    };

    BCP.prototype.unsubscribe = function(names) {
      var i, _i, _len, _results;
      if (names.length === 0) throw "Use BCP.unsubscribe_all()";
      this.send({
        "type": "unsubscribe",
        "docnames": names
      });
      _results = [];
      for (_i = 0, _len = names.length; _i < _len; _i++) {
        i = names[_i];
        _results.push(this.subscriptions[i] = false);
      }
      return _results;
    };

    BCP.prototype.unsubscribe_all = function() {
      this.send({
        "type": "unsubscribe",
        "docnames": []
      });
      return this.subscriptions = {};
    };

    BCP.prototype.send = function(obj) {
      var s;
      s = JSON.stringify(obj);
      this.log("sending", s);
      return this.stream.send(s + "\x00");
    };

    BCP.prototype.error = function(code, details, data) {
      var message;
      message = {
        "type": "error",
        "code": code
      };
      if (details) message.details = details;
      if (data) message.data = data;
      return this.send(message);
    };

    BCP.prototype.log = function(headline, detail) {
      return console.log(headline + ":" + detail);
    };

    return BCP;

  })();

  context.BCP = BCP;

}).call(this);
