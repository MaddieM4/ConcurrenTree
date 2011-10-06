(function() {
  var CTree, protostr, protoval, window;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  window = this;

  CTree = (function() {

    function CTree(value) {
      this._trace = __bind(this._trace, this);
      this.trace = __bind(this.trace, this);
      this.resolve = __bind(this.resolve, this);      this.value = value;
      this.length = value.length;
      this.key = serial.key(value);
      this.deletions = [];
      window.arrayFill(this.deletions, (function() {
        return false;
      }), this.length);
      this.children = [];
      window.arrayFill(this.children, (function() {
        return {};
      }), this.length + 1);
    }

    CTree.prototype.insert = function(pos, childtext) {
      var child;
      child = new CTree(childtext);
      return this.insert_obj(pos, child);
    };

    CTree.prototype["delete"] = function(pos) {
      var x, _ref, _ref2;
      if (window.isArray(pos)) {
        for (x = _ref = pos[0], _ref2 = pos[1]; _ref <= _ref2 ? x <= _ref2 : x >= _ref2; _ref <= _ref2 ? x++ : x--) {
          this["delete"](x);
        }
      } else {
        this.deletions[pos] = true;
      }
      return this;
    };

    CTree.prototype.insert_obj = function(pos, child) {
      this.children[pos][child.key] = child;
      return child;
    };

    CTree.prototype.flatten = function() {
      var node, nodes, p, result, _i, _len, _ref;
      result = "";
      for (p = 0, _ref = this.length; 0 <= _ref ? p <= _ref : p >= _ref; 0 <= _ref ? p++ : p--) {
        nodes = this.kids(p);
        for (_i = 0, _len = nodes.length; _i < _len; _i++) {
          node = nodes[_i];
          result += node.flatten();
        }
        if (p < this.length && !this.deletions[p]) result += this.value[p];
      }
      return result;
    };

    CTree.prototype.resolve = function(addr) {
      var child, key, pos;
      if (addr.length === 0) {
        return this;
      } else {
        if (isNumber(addr[0])) {
          pos = addr.shift();
        } else {
          pos = this.length;
        }
        key = addr.shift();
        return child = this.get(pos, key).resolve(addr);
      }
    };

    CTree.prototype.trace = function(pos) {
      var result;
      result = this._trace(pos);
      if (window.isInteger(result)) {
        throw "CTree.trace: pos > this.flatten().length";
      }
      if (!((result.address != null) && (result.pos != null))) {
        throw "CTree.trace: _trace returned bad object, type " + typeof result + ", value " + JSON.stringify(result);
      }
      return result;
    };

    CTree.prototype._trace = function(togo) {
      var k, pos, _i, _len, _ref, _ref2;
      for (pos = 0, _ref = this.length; 0 <= _ref ? pos <= _ref : pos >= _ref; 0 <= _ref ? pos++ : pos--) {
        _ref2 = this.kids(pos);
        for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
          k = _ref2[_i];
          togo = k._trace(togo);
          if (!window.isNumber(togo)) {
            togo.address = this.jump(pos, k.key).concat(togo.address);
            return togo;
          }
        }
        if (togo === 0) {
          return {
            "address": [],
            "pos": pos
          };
        }
        if (pos < this.length && !this.deletions[pos]) togo -= 1;
      }
      return togo;
    };

    CTree.prototype.get = function(pos, key) {
      if (pos > this.length || pos < 0 || !window.isNumber(pos)) {
        throw "IndexError: CTree.get position out of range (" + pos.toString() + ")";
      }
      if (!((this.children[pos][key] != null) && window.isString(key))) {
        throw "KeyError: CTree.get child does not exist at position " + pos + " and with key '" + key + "'";
      }
      return this.children[pos][key];
    };

    CTree.prototype.keys = function(pos) {
      var key;
      return ((function() {
        var _results;
        _results = [];
        for (key in this.children[pos]) {
          _results.push(key);
        }
        return _results;
      }).call(this)).sort();
    };

    CTree.prototype.kids = function(pos) {
      var key, _i, _len, _ref, _results;
      _ref = this.keys(pos);
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        key = _ref[_i];
        _results.push(this.get(pos, key));
      }
      return _results;
    };

    CTree.prototype.jump = function(pos, key) {
      if (pos === this.length) {
        return [key];
      } else {
        return [pos, key];
      }
    };

    CTree.prototype.apply = function(obj) {
      return obj.apply(this);
    };

    return CTree;

  })();

  protostr = function(item) {
    if (typeof item === "string") {
      return item;
    } else {
      return "";
    }
  };

  protoval = function(list) {
    var i;
    return ((function() {
      var _i, _len, _results;
      _results = [];
      for (_i = 0, _len = list.length; _i < _len; _i++) {
        i = list[_i];
        _results.push(protostr(i));
      }
      return _results;
    })()).join("");
  };

  this.CTreeFromProto = function(proto) {
    var deletions, i, pos, tree, value, _i, _j, _len, _len2;
    deletions = proto.pop();
    value = protoval(proto);
    tree = new CTree(value);
    for (_i = 0, _len = deletions.length; _i < _len; _i++) {
      i = deletions[_i];
      tree["delete"](i);
    }
    pos = 0;
    for (_j = 0, _len2 = proto.length; _j < _len2; _j++) {
      i = proto[_j];
      if (typeof i === "string") {
        pos += i.length;
      } else {
        tree.insert_obj(pos, window.CTreeFromProto(i));
      }
    }
    return tree;
  };

  this.CTree = CTree;

}).call(this);
