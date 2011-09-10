(function() {
  var Buffer;
  Buffer = (function() {
    function Buffer() {
      this.readposition = 0;
      this.writeposition = 0;
      this._contents = {};
      this.readlock = false;
    }
    Buffer.prototype.write = function(value) {
      var pos;
      pos = ++this.writeposition;
      return this._contents[pos - 1] = value;
    };
    Buffer.prototype.read = function() {
      var read, result, write;
      if (this.readlock) return;
      this.readlock = true;
      read = this.readposition;
      write = this.writeposition;
      if (read < write) {
        result = this._contents[read];
        delete this._contents[read];
        this.readposition++;
      }
      this.readlock = false;
      return result;
    };
    Buffer.prototype.read_all = function() {
      var result, value;
      result = [];
      value = this.read();
      while (value !== void 0) {
        result.push(value);
        value = this.read();
      }
      return result;
    };
    return Buffer;
  })();
}).call(this);
