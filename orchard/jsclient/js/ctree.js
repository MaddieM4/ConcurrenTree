(function() {
  var CTree;

  CTree = (function() {

    function CTree(value) {
      this.value = value;
      this.length = value.length;
      this.key = serial.key(value);
      this.deletions = [];
      arrayfill(this.deletions, (function() {
        return false;
      }), this.length);
      this.children = [];
      arrayfill(this.children, af_obj, this.length + 1);
    }

    CTree.prototype.insert = function(pos, childtext) {
      var child;
      child = new CTree(childtext);
      return this.children[pos][child.key] = child;
    };

    CTree.prototype["delete"] = function(pos) {
      this.deletions[pos] = true;
      return this;
    };

    CTree.prototype.get = function(pos, key) {
      return this.children[pos][key];
    };

    return CTree;

  })();

}).call(this);
