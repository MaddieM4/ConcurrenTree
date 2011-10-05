(function() {
  var Stream, context, types;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  context = window;

  types = {
    websocket: "js/stream/ws.js"
  };

  Stream = (function() {

    function Stream(type, url) {
      var jsaddress;
      this.type = type;
      this.url = url;
      this.connect = __bind(this.connect, this);
      this.reconnect = __bind(this.reconnect, this);
      this.closed = __bind(this.closed, this);
      this.close = __bind(this.close, this);
      this._error = __bind(this._error, this);
      this._message = __bind(this._message, this);
      this._connect = __bind(this._connect, this);
      this.send = __bind(this.send, this);
      this.started = false;
      this.running = false;
      if (!this.type in types) throw "Unknown stream type";
      jsaddress = types[this.type];
      this.worker = new Worker(jsaddress);
      this.worker.onmessage = this._message;
      this.worker.onerror = this._error;
      this.reconnect();
    }

    Stream.prototype.send = function(value) {
      return this.worker.postMessage([2, value]);
    };

    Stream.prototype._connect = function(event) {
      if (this.onconnect != null) return this.onconnect(event);
    };

    Stream.prototype._message = function(event) {
      switch (event.data[0]) {
        case 0:
          return this.close();
        case 1:
          return this._connect(event);
        case 2:
          if (this.onmessage != null) return this.onmessage(event.data[1]);
          break;
        default:
          return console.log("Stream worker debug: " + event.data);
      }
    };

    Stream.prototype._error = function(event) {
      if (this.onerror != null) return this.onerror(event);
    };

    Stream.prototype.close = function() {
      this.worker.postMessage([0]);
      return this.running = false;
    };

    Stream.prototype.closed = function() {
      if (started && !running) return true;
    };

    Stream.prototype.reconnect = function() {
      this.close();
      return this.connect(this.url);
    };

    Stream.prototype.connect = function(url) {
      this.worker.postMessage([1, url]);
      this.started = true;
      return this.running = true;
    };

    return Stream;

  })();

  context.Stream = Stream;

}).call(this);
