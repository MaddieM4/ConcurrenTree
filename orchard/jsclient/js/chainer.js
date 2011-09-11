(function() {
  var Chainer;
  Chainer = (function() {
    /* 
    A chaining wrapper for the tree. Call s on it like a regular tree.
    For properties, use mychain.tree.propertyname
    */
    function Chainer(tree) {
      this.tree = tree;
      this.lastpos = void 0;
      this.startpos = void 0;
      this.chain = "";
    }
    Chainer.prototype.insert = function(pos, childtext) {
      this.apply();
      return this.tree.insert(pos, childtext);
    };
    Chainer.prototype["delete"] = function(pos) {
      this.apply();
      return this.tree["delete"](pos);
    };
    Chainer.prototype.get = function(pos, hash) {
      this.apply();
      return this.tree.get(pos, hash);
    };
    Chainer.prototype.flatten = function() {
      this.apply();
      return this.tree.flatten();
    };
    Chainer.prototype.trace = function(pos) {
      this.apply();
      return this.tree.trace(pos);
    };
    Chainer.prototype.untrace = function(addr, pos) {
      this.apply();
      return this.tree.untrace(addr, pos);
    };
    Chainer.prototype.resolve = function(addrstring) {
      this.apply();
      return this.tree.resolve(addrstring);
    };
    Chainer.prototype.kidscan = function() {
      this.apply();
      return this.tree.kidscan();
    };
    Chainer.prototype.flatinsert = function(pos, value) {
      if (this.startpos === void 0) {
        this.startpos = pos;
        this.lastpos = pos;
        this.chain += value;
      } else if (pos === this.lastpos + 1) {
        this.chain += value;
        this.lastpos = pos;
      } else {
        this.apply();
        this.tree.flatinsert(pos, value);
      }
    };
    Chainer.prototype.flatdelete = function(pos) {
      if (this.startpos !== void 0 && pos === this.lastpos) {
        return this.chain = this.chain.substr(0, chain.length - 1);
      } else {
        this.apply();
        return this.tree.flatdelete(pos);
      }
    };
    Chainer.prototype.flatreplace = function(start, end, value) {
      this.apply();
      return this.tree.flatreplace(start, end, value);
    };
    Chainer.prototype.apply = function() {
      if (this.chain !== "") {
        this.tree.flatinsert(this.startpos, this.chain);
        this.startpos = void 0;
        this.lastpos = void 0;
        return this.chain = "";
      }
    };
    return Chainer;
  })();
  console.log("test");
  window.Chainer = Chainer;
}).call(this);
