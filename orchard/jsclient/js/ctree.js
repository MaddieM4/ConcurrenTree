(function() {
  var CTree, protostr, protoval, window;
  window = this;
  CTree = (function() {
    function CTree(value) {
      this.value = value;
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
      return this.insert_obj(pos(child));
    };
    CTree.prototype["delete"] = function(pos) {
      var x, _i, _j, _len, _ref, _ref2, _ref3, _results;
      _ref3 = (function() {
        _results = [];
        for (var _j = _ref = pos[0], _ref2 = pos[1]; _ref <= _ref2 ? _j <= _ref2 : _j >= _ref2; _ref <= _ref2 ? _j++ : _j--){ _results.push(_j); }
        return _results;
      }).apply(this)(window.isArray(pos) ? void 0 : this.deletions[pos] = true);
      for (_i = 0, _len = _ref3.length; _i < _len; _i++) {
        x = _ref3[_i];
        this["delete"](x);
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
        if (p < this.length) result += this.value[p];
      }
      return result;
    };
    CTree.prototype.get = function(pos, key) {
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
      return key(pos === this.length ? void 0 : [pos, key]);
    };
    return CTree;
  })();
  protostr = function(item) {
    return i(typeof i === "string" ? void 0 : "");
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
    var deletions, i, tree, value, _i, _len;
    deletions = proto.pop();
    value = protoval(proto);
    tree = new CTree(value);
    tree.deletions = deletions;
    for (_i = 0, _len = proto.length; _i < _len; _i++) {
      i = proto[_i];
      if (typeof i === !"string") tree.insert_obj(window.CTreeFromProto(i));
    }
    return tree;
  };
  this.CTree = CTree;
}).call(this);
