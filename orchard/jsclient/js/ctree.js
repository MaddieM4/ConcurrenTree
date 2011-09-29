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

  window.CTree = CTree;

}).call(this);
