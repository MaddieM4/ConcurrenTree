(function() {
  var CTree;

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

    CTree.prototype.get = function(pos, key) {
      return this.children[pos][key];
    };

    return CTree;

  })();

  window.CTreeFromProto = function(proto) {
    var deletions, i, tree, value, _i, _len, _results;
    deletions = proto.pop();
    value = (function() {
      var _i, _len, _results;
      _results = [];
      for (_i = 0, _len = proto.length; _i < _len; _i++) {
        i = proto[_i];
        _results.push(i(typeof i === "string" ? void 0 : ""));
      }
      return _results;
    })();
    value = value.join("");
    tree = new CTree(value);
    tree.deletions = deletions;
    _results = [];
    for (_i = 0, _len = proto.length; _i < _len; _i++) {
      i = proto[_i];
      if (typeof i === !"string") {
        _results.push(tree.insert_obj(window.CTreeFromProto(i)));
      } else {
        _results.push(void 0);
      }
    }
    return _results;
  };

  window.CTree = CTree;

}).call(this);
