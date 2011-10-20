(function() {
  var tests;
  tests = {
    arrayFill: function() {
      /* test case 1
          padding with zeroes
          tests with a function which always returns none
      */

      var output, result, testcase;
      testcase = [0, 0, 0, 0, 0, 0, 0];
      output = arrayFill([], (function() {
        return 0;
      }), 7);
      result = testcase === output ? 'successful' : 'failed';
      console.log("arrayFill #1 " + result);
      /* test case 2
          padding with index
      */

      testcase = [0, 1, 2, 3, 4, 5];
      output = arrayFill([], (function(i) {
        return i;
      }), 6);
      result = testcase === output ? 'successful' : 'failed';
      console.log("arrayFill #2 " + result);
      /* test case 3
          negative value of count
      */

      testcase = [0, -1, -2, -3];
      output = arrayFill([], (function(i) {
        return i;
      }), 4);
      result = testcase === output ? 'successful' : 'failed';
      return console.log("arrayFill #3 " + result);
    },
    af_object: function() {
      /* test case 1
      */

      var output, result, testcase;
      testcase = {};
      output = af_object(null);
      result = testcase === output ? 'successful' : 'failed';
      return console.log("af_object #1 " + result);
    },
    isArray: function() {
      /* test suite
          [] returns true
      */

      var i, testcasesFalse, testcasesTrue, _i, _j, _len, _len2, _results;
      testcasesTrue = [[], [void 0], [null], [0], [false], [''], [[]], [{}], ['test']];
      testcasesFalse = [{}, 0, 1, true, false, '', 'hello, world', void 0, null];
      for (_i = 0, _len = testcasesTrue.length; _i < _len; _i++) {
        i = testcasesTrue[_i];
        if (isArray(i)) {
          console.log("isArray test successful: " + i + " is an Array");
        } else {
          console.log("isArray test FAILED: " + i + " is an Array");
        }
      }
      _results = [];
      for (_j = 0, _len2 = testcasesFalse.length; _j < _len2; _j++) {
        i = testcasesFalse[_j];
        if (isArray(i)) {
          _results.push(console.log("isArray test FAILED: " + i + " is NOT an Array"));
        } else {
          _results.push(console.log("isArray test successful: " + i + " is not an Array"));
        }
      }
      return _results;
    }
  };
}).call(this);
