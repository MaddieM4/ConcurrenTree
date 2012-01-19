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
