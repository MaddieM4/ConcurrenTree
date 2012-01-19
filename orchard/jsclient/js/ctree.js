(function() {
  var SHA1, getUrlParameter;

  this.arrayFill = function(array, value, count) {
    /* Fills an array with the values returned by value when given an index
    
        Arguments:
            array: the array to be extended
            value: a function returning the value to be appended when given an       
                index, possible index values being between 0 and count exclusive 
                of count
            count: the number of values to append
        
        Returns: 
            The modified array
        
        Notes: 
            For negative values of count, the function will pass negative values 
            starting from 0 and decreasing to count+1, like so
            (function 'f' returns the value given: f = (i) -> i)
            arrayFill [], f, 5
            returns [0, -1, -2, -3, -4]
        
        Examples:
            pad an array with nulls
            arrayFill [], (-> null), 4
                returns [null, null, null, null]
            
            Produce the 6 first square numbers 
            arrayFill [], ((i) -> i * i), 6
                returns [0, 1, 4, 9, 16, 25]
    */
    var i;
    assert(isArray(array), 'array (first argument) must be an array');
    assert(isFunction(value), 'value (second argument) must be a function');
    assert;
    for (i = 0; 0 <= count ? i < count : i > count; 0 <= count ? i++ : i--) {
      array.push(value(i));
    }
    return array;
  };

  this.isArray = function(obj) {
    if (typeof obj === "object") {
      return Object.prototype.toString.call(obj) === "[object Array]";
    } else {
      return false;
    }
  };

  this.isObject = function(obj) {
    if (typeof obj === "object") {
      return Object.prototype.toString.call(obj) === "[object Object]";
    } else {
      return false;
    }
  };

  this.isFunction = function(obj) {
    if (typeof obj === "function") return true;
    if (typeof obj === "object") {
      return Object.prototype.toString.call(obj) === "[object Function]";
    } else {
      return false;
    }
  };

  this.isInteger = function(obj) {
    return isNumber(obj) && Math.floor(obj) === obj;
  };

  this.isNumber = function(obj) {
    return typeof obj === "number";
  };

  this.isBoolean = function(obj) {
    /* tests if an object is a boolean object
        
        Note! This does not test if an object can resolve to a boolean, it 
        tests whether it is a boolean object. 
        This test is equivalent to 
        if obj is true or obj is false then true else false
        
        JS Condition (obj === true || obj === false), not '=='!
    */    return typeof obj === "boolean";
  };

  this.isString = function(obj) {
    return typeof obj === "string";
  };

  this.range = function(start, end, step) {
    var i, _results;
    if (step == null) step = 1;
    /* returns an array containing integers ranged between start and end,
        with a gap of step between each one.
        
        Arguments: 
            start: the first value in the range, any integer is valid
            end: the final value in the range, any integer is valid
            step: the step between each value in the range, any non-zero integer 
                is valid. (optional, default = 1)
            
        Returns:
            An array containing all integers between start and end (inclusive of 
            start, exclusive of end), where each integer is different by step 
            from the integers adjacent to it in sequence. 
        
        Notes: 
            Step can be either negative or positive, as the function calculates 
            the correct sign by testing whether the value of start or end is 
            greater. 
            This is done by XORing the conditions end < start, step > 0, and 
            changes the sign if this is true. 
        
        Examples:
            range 0, 5
                [0, 1, 2, 3, 4]
            range 5, 0
                [5, 4, 3, 2, 1]
            range 0, 5, 2
                [0, 2, 4]
            range 5, 0, 2
                [5, 3, 1]
    */
    step = (start < end && step > 0) || (start > end && step < 0) ? step : -step;
    _results = [];
    for (i = start; start <= end ? i < end : i > end; i += step) {
      _results.push(i);
    }
    return _results;
  };

  this.urlParameters = function(url) {
    var i, kv, pairs, params, _i, _len;
    if (url == null) url = this.location.href;
    /* extracts a dictionary of url parameters from the given url
        
        Arguments:
            url: a url to parse parameters from. (Optional, default = 
                this.location.href)
        
        Returns:
            An object containing key: value pairs of the url parameters.
            value is null when the parameter has no value (ie y in '...?x=1&y')
        
        Examples: 
            urlParameters 'http://y.tld/?x=1&b=sugar&magic'
                {x: '1', b: 'sugar', magic: null}
            
        Developer:
            This should logically be extended to use the url decode function 
            to decode urlencoded values, and where possible, these values 
            could be unstringified (1 should be 1 not '1', perhaps?)
    */
    params = {};
    pairs = url.slice(url.indexOf('?') + 1).split('&');
    for (_i = 0, _len = pairs.length; _i < _len; _i++) {
      i = pairs[_i];
      kv = i.split('=');
      params[kv[0]] = kv.length > 1 ? kv[1] : null;
    }
    return params;
  };

  this.get_url_variable = getUrlParameter = function(name, def) {
    /* extracts the parameter name from the current page url, or returns def if
        name does not exist.
        
        Arguments:
            name: the name of the url parameter to extract.
            def: a default value to be returned if name does not exist as a 
                parameter value in the page url.
        
        Returns:
            The value of name, or def.
        
        Notes:
            If name exists but has no value, null is returned (see urlParameters
            function).
        
        Examples:
            (in all examples, the page url is 'http://x.tld/?y=dog&n')
            getUrlParameter 'y', 'default'
                'dog'
            getUrlParameter 'n', 'default'
                null
            getUrlParameter 'z', 'default'
                'default'
    */
    var params;
    params = urlParameters();
    if (params[name] !== void 0) {
      return params[name];
    } else {
      return def;
    }
  };

  this.Stream = function(callback, port, host, addr) {
    var longaddr;
    if (!(port != null)) port = 9091;
    if (!(host != null)) host = "localhost";
    if (!(addr != null)) addr = "/";
    longaddr = "http://" + host + ":" + port + addr;
    return this.LoadSIO("http://" + host + ":" + port + "/socket.io/socket.io.js", {
      port: port
    }, callback);
  };

  this.LoadSIO = function(base, options, callback) {
    console.log(base);
    return head.js(base, function() {
      var sock;
      sock = new io.Socket(void 0, options);
      sock.connect();
      return callback(sock);
    });
  };

  this.isJSON = function(str) {
    try {
      JSON.parse(str);
      return true;
    } catch (e) {
      return false;
    }
  };

  SHA1 = function(msg) {
    var A, B, C, D, E, H0, H1, H2, H3, H4, Utf8Encode, W, blockstart, cvt_hex, i, j, lsb_hex, msg_len, rotate_left, temp, temp1, temp2, word_array;
    rotate_left = function(n, s) {
      var t4;
      t4 = (n << s) | (n >>> (32 - s));
      return t4;
    };
    lsb_hex = function(val) {
      var i, str, vh, vl;
      str = "";
      i = void 0;
      vh = void 0;
      vl = void 0;
      i = 0;
      while (i <= 6) {
        vh = (val >>> (i * 4 + 4)) & 0x0f;
        vl = (val >>> (i * 4)) & 0x0f;
        str += vh.toString(16) + vl.toString(16);
        i += 2;
      }
      return str;
    };
    cvt_hex = function(val) {
      var i, str, v;
      str = "";
      i = void 0;
      v = void 0;
      i = 7;
      while (i >= 0) {
        v = (val >>> (i * 4)) & 0x0f;
        str += v.toString(16);
        i--;
      }
      return str;
    };
    Utf8Encode = function(string) {
      var c, n, utftext;
      string = string.replace(/\r\n/g, "\n");
      utftext = "";
      n = 0;
      while (n < string.length) {
        c = string.charCodeAt(n);
        if (c < 128) {
          utftext += String.fromCharCode(c);
        } else if ((c > 127) && (c < 2048)) {
          utftext += String.fromCharCode((c >> 6) | 192);
          utftext += String.fromCharCode((c & 63) | 128);
        } else {
          utftext += String.fromCharCode((c >> 12) | 224);
          utftext += String.fromCharCode(((c >> 6) & 63) | 128);
          utftext += String.fromCharCode((c & 63) | 128);
        }
        n++;
      }
      return utftext;
    };
    blockstart = void 0;
    i = void 0;
    j = void 0;
    W = new Array(80);
    H0 = 0x67452301;
    H1 = 0xEFCDAB89;
    H2 = 0x98BADCFE;
    H3 = 0x10325476;
    H4 = 0xC3D2E1F0;
    A = void 0;
    B = void 0;
    C = void 0;
    D = void 0;
    E = void 0;
    temp = void 0;
    msg = Utf8Encode(msg);
    msg_len = msg.length;
    word_array = new Array();
    i = 0;
    while (i < msg_len - 3) {
      j = msg.charCodeAt(i) << 24 | msg.charCodeAt(i + 1) << 16 | msg.charCodeAt(i + 2) << 8 | msg.charCodeAt(i + 3);
      word_array.push(j);
      i += 4;
    }
    switch (msg_len % 4) {
      case 0:
        i = 0x080000000;
        break;
      case 1:
        i = msg.charCodeAt(msg_len - 1) << 24 | 0x0800000;
        break;
      case 2:
        i = msg.charCodeAt(msg_len - 2) << 24 | msg.charCodeAt(msg_len - 1) << 16 | 0x08000;
        break;
      case 3:
        i = msg.charCodeAt(msg_len - 3) << 24 | msg.charCodeAt(msg_len - 2) << 16 | msg.charCodeAt(msg_len - 1) << 8 | 0x80;
    }
    word_array.push(i);
    while ((word_array.length % 16) !== 14) {
      word_array.push(0);
    }
    word_array.push(msg_len >>> 29);
    word_array.push((msg_len << 3) & 0x0ffffffff);
    blockstart = 0;
    while (blockstart < word_array.length) {
      i = 0;
      while (i < 16) {
        W[i] = word_array[blockstart + i];
        i++;
      }
      i = 16;
      while (i <= 79) {
        W[i] = rotate_left(W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16], 1);
        i++;
      }
      A = H0;
      B = H1;
      C = H2;
      D = H3;
      E = H4;
      i = 0;
      while (i <= 19) {
        temp1 = (B & C) | (~B & D);
        temp2 = rotate_left(A, 5) + temp1 + E + W[i] + 0x5A827999;
        temp = temp2 & 0x0ffffffff;
        E = D;
        D = C;
        C = rotate_left(B, 30);
        B = A;
        A = temp;
        i++;
      }
      i = 20;
      while (i <= 39) {
        temp = (rotate_left(A, 5) + (B ^ C ^ D) + E + W[i] + 0x6ED9EBA1) & 0x0ffffffff;
        E = D;
        D = C;
        C = rotate_left(B, 30);
        B = A;
        A = temp;
        i++;
      }
      i = 40;
      while (i <= 59) {
        temp1 = (B & C) | (B & D) | (C & D);
        temp2 = rotate_left(A, 5) + temp1 + E + W[i] + 0x8F1BBCDC;
        temp = temp2 & 0x0ffffffff;
        E = D;
        D = C;
        C = rotate_left(B, 30);
        B = A;
        A = temp;
        i++;
      }
      i = 60;
      while (i <= 79) {
        temp = (rotate_left(A, 5) + (B ^ C ^ D) + E + W[i] + 0xCA62C1D6) & 0x0ffffffff;
        E = D;
        D = C;
        C = rotate_left(B, 30);
        B = A;
        A = temp;
        i++;
      }
      H0 = (H0 + A) & 0x0ffffffff;
      H1 = (H1 + B) & 0x0ffffffff;
      H2 = (H2 + C) & 0x0ffffffff;
      H3 = (H3 + D) & 0x0ffffffff;
      H4 = (H4 + E) & 0x0ffffffff;
      blockstart += 16;
    }
    temp = cvt_hex(H0) + cvt_hex(H1) + cvt_hex(H2) + cvt_hex(H3) + cvt_hex(H4);
    return temp.toLowerCase();
  };

  this.serial = {
    key: function(str) {
      /* Creates a textual node key
      
          Arguments:
              str: the string to be formed into a key 
          
          Returns: 
              The key formed from the given string 
          
          Notes:
          
          Examples:
      */      if (str.length > 10) {
        return str.slice(0, 10) + serial.sum(str.slice(10)).slice(0, 6);
      } else {
        return str;
      }
    },
    sum: function(str) {
      /* sums the string passed to it
          
          Arguments: 
              str: the string to be summed
          
          Returns:
              the integer sum of the string given
          
          Notes:
              http://stackoverflow.com/q/7538590/473479
          
          Examples:
      */      return SHA1(str);
    },
    strict: function(obj) {
      throw "serial.strict is not yet implemented";
    }
  };

  this.assert = function(condition, message) {
    /* throws an error if the condition passed is not true. Optionally provide
        the error message to be thrown.
        
        Arguments:
            condition: a boolean
            message: an error message (optional)
        
        Returns: 
            nothing
        
        Throws: 
            'Assertion error' 
        
        Notes:
            Recommended use is:
            assert this is that, 'error if not'
            
            This is because asserting a definite boolean is reduntant, the 
            error can just be thrown instead of calling assert.
        
        Examples:
            assert (isString str), 'str is not a string!'
    */    message = message !== "" ? "Assertion error: '" + message + "'" : 'Assertion error';
    if (!condition) throw message;
  };

}).call(this);
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
(function() {
  var Operation;

  Operation = (function() {

    function Operation(instructions) {
      this.instructions = instructions;
    }

    Operation.prototype.push = function(i) {
      return this.instructions.push(i);
    };

    Operation.prototype.push_list = function(list) {
      var i, _i, _len, _results;
      _results = [];
      for (_i = 0, _len = list.length; _i < _len; _i++) {
        i = list[_i];
        _results.push(this.push(i));
      }
      return _results;
    };

    Operation.prototype.pushinsert = function(addr, pos, value) {
      return this.push([1, addr, pos, value]);
    };

    Operation.prototype.pushdelete = function(addr, victims) {
      return this.push([0, addr].concat(victims));
    };

    Operation.prototype.pushflatinsert = function(pos, value, tree) {
      var trace;
      trace = tree.trace_index(pos);
      return this.pushinsert(trace.address, trace.pos, value);
    };

    Operation.prototype.pushflatdelete = function(pos, tree) {
      var trace;
      trace = tree.trace_char(pos);
      return this.pushdelete(trace.address, trace.pos);
    };

    Operation.prototype.pushflatdeletes = function(pos, amount, tree) {
      var i, _results;
      _results = [];
      for (i = 0; 0 <= amount ? i < amount : i > amount; 0 <= amount ? i++ : i--) {
        _results.push(this.pushflatdelete(pos + i, tree));
      }
      return _results;
    };

    Operation.prototype.apply = function(tree) {
      var i, _i, _len, _ref, _results;
      _ref = this.instructions;
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        i = _ref[_i];
        _results.push(this.apply_instruction(tree, i));
      }
      return _results;
    };

    Operation.prototype.apply_instruction = function(tree, i) {
      var type;
      type = i[0];
      switch (type) {
        case 0:
          return this.apply_deletion(tree, i);
        case 1:
          return this.apply_insertion(tree, i);
      }
    };

    Operation.prototype.apply_deletion = function(tree, i) {
      var addr, pos, target, victims, _i, _len, _results;
      addr = i[1];
      victims = i.slice(2);
      target = tree.resolve(addr);
      _results = [];
      for (_i = 0, _len = victims.length; _i < _len; _i++) {
        pos = victims[_i];
        _results.push(target["delete"](pos));
      }
      return _results;
    };

    Operation.prototype.apply_insertion = function(tree, i) {
      var addr, pos, target, value;
      addr = i[1];
      pos = i[2];
      value = i[3];
      target = tree.resolve(addr);
      return target.insert(pos, value);
    };

    Operation.prototype.proto = function() {
      return {
        "type": "op",
        "instructions": this.instructions
      };
    };

    Operation.prototype.victimize_deletions = function(deletions) {
      var i, result, running, _ref;
      running = -1;
      result = [];
      for (i = 0, _ref = deletions.length; 0 <= _ref ? i <= _ref : i >= _ref; 0 <= _ref ? i++ : i--) {
        if (!deletions[i]) {
          if (running !== -1) {
            if (running === i - 1) {
              result.push(running);
            } else {
              result.push([running, i - 1]);
            }
          }
          running = -1;
        } else {
          if (running === -1) running = i;
        }
      }
      return result;
    };

    Operation.prototype.serialize = function() {
      return JSON.stringify(this.proto());
    };

    Operation.prototype.fromTree = function(address, tree) {
      var deletions, key, node, nodeaddr, p, _ref, _results;
      _results = [];
      for (p = 0, _ref = tree.length; 0 <= _ref ? p <= _ref : p >= _ref; 0 <= _ref ? p++ : p--) {
        _results.push((function() {
          var _ref2, _results2;
          _ref2 = tree.children[p];
          _results2 = [];
          for (key in _ref2) {
            node = _ref2[key];
            nodeaddr = address.concat(tree.jump(p, key));
            deletions = this.victimize_deletions(node.deletions);
            this.pushinsert(address, p, node.value);
            if (deletions.length > 0) this.pushdelete(nodeaddr, deletions);
            _results2.push(this.fromTree(nodeaddr, node));
          }
          return _results2;
        }).call(this));
      }
      return _results;
    };

    return Operation;

  })();

  this.Operation = Operation;

}).call(this);
(function() {
  var CTree, protostr, protoval, window;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  window = this;

  CTree = (function() {

    function CTree(value) {
      this._trace_char = __bind(this._trace_char, this);
      this._trace_index = __bind(this._trace_index, this);
      this.trace_verify = __bind(this.trace_verify, this);
      this.resolve = __bind(this.resolve, this);      this.value = value;
      this.length = value.length;
      this.key = serial.key("t" + value);
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

    CTree.prototype.trace_index = function(pos) {
      return this.trace_verify(this._trace_index(pos));
    };

    CTree.prototype.trace_char = function(pos) {
      return this.trace_verify(this._trace_char(pos));
    };

    CTree.prototype.trace_verify = function(result) {
      if (window.isInteger(result)) {
        throw "CTree.trace: pos > this.flatten().length";
      }
      if (!((result.address != null) && (result.pos != null))) {
        throw "CTree.trace: _trace returned bad object, type " + typeof result + ", value " + JSON.stringify(result);
      }
      return result;
    };

    CTree.prototype._trace_index = function(togo) {
      var k, pos, _i, _len, _ref, _ref2;
      for (pos = 0, _ref = this.length; 0 <= _ref ? pos <= _ref : pos >= _ref; 0 <= _ref ? pos++ : pos--) {
        _ref2 = this.kids(pos);
        for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
          k = _ref2[_i];
          togo = k._trace_index(togo);
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

    CTree.prototype._trace_char = function(togo) {
      var k, pos, _i, _len, _ref, _ref2;
      for (pos = 0, _ref = this.length; 0 <= _ref ? pos <= _ref : pos >= _ref; 0 <= _ref ? pos++ : pos--) {
        _ref2 = this.kids(pos);
        for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
          k = _ref2[_i];
          togo = k._trace_char(togo);
          if (!window.isNumber(togo)) {
            togo.address = this.jump(pos, k.key).concat(togo.address);
            return togo;
          }
        }
        if (pos < this.length && !this.deletions[pos]) {
          if (togo === 0) {
            return {
              "address": [],
              "pos": pos
            };
          }
          togo -= 1;
        }
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
