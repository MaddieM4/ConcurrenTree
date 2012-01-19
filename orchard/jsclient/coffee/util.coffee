# util.coffee :: Utilities

# Dependencies: none

this.arrayFill = (array, value, count) ->
    ### Fills an array with the values returned by value when given an index
    
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
    ###
    assert (isArray array), 'array (first argument) must be an array'
    assert (isFunction value), 'value (second argument) must be a function'
    assert 
    
    array.push value i for i in [0 ... count]
    array

this.isArray = (obj) ->
    # tests if an object is an array
    if typeof obj is "object" 
        Object.prototype.toString.call(obj) is "[object Array]"
    else
        false

this.isObject = (obj) ->
    # tests if an object is a hash/dictionary type object
    if typeof obj is "object"
        Object.prototype.toString.call(obj) is "[object Object]"
    else
        false

this.isFunction = (obj) ->
    # tests if an object is a function
    return true if typeof obj is "function"
    if typeof obj is "object"
        Object.prototype.toString.call(obj) is "[object Function]"
    else 
        false

this.isInteger = (obj) ->
    # tests if an object belongs to the Integer set
    isNumber(obj) and Math.floor(obj) is obj


this.isNumber = (obj) ->
    # tests if an object is a number
    typeof obj is "number"

this.isBoolean = (obj) ->
    ### tests if an object is a boolean object
        
        Note! This does not test if an object can resolve to a boolean, it 
        tests whether it is a boolean object. 
        This test is equivalent to 
        if obj is true or obj is false then true else false
        
        JS Condition (obj === true || obj === false), not '=='! 
    ###
    typeof obj is "boolean"

this.isString = (obj) ->
    typeof obj is "string"

this.range = (start, end, step = 1) ->
    ### returns an array containing integers ranged between start and end,
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
        
    ###
    step = if (start < end and step > 0) or (start > end and step < 0) then step else - step
    i for i in [start... end] by step

this.urlParameters = (url = this.location.href) ->
    ### extracts a dictionary of url parameters from the given url
        
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
    ###
    params = {}
    pairs = url.slice(url.indexOf('?') + 1).split('&')
    for i in pairs
        kv = i.split('=')
        params[kv[0]] = if kv.length > 1 then kv[1] else null
    params

# get_url_variable is a pythonic name, variable should be parameter, recommend changing
this.get_url_variable = getUrlParameter = (name, def) -> 
    ### extracts the parameter name from the current page url, or returns def if
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
            
    ###
    params = urlParameters()
    if params[name] isnt undefined then params[name] else def

this.Stream = (callback, port, host, addr) ->
    # Works asynchronously because it has to load Socket.IO JS lib
    port = 9091 if not port?
    host = "localhost" if not host?
    addr = "/" if not addr?
    longaddr = "http://"+host+":"+port+addr
    this.LoadSIO("http://"+host+":"+port+"/socket.io/socket.io.js", {port:port}, callback)

this.LoadSIO = (url, options, callback) ->
    # URL should be path to socket.io.js
    console.log(url)
    head.js(url, ()->
      sock = new io.Socket(undefined, options)
      sock.connect()
      callback(sock)
    )

this.isJSON = (str) ->
    # tests if the suppled string is valid JSON
    # Arguments: str: a string. 
    # Returns: true/false
    try
        JSON.parse str
        true
    catch e
        false

SHA1 = (msg) ->
  rotate_left = (n, s) ->
    t4 = (n << s) | (n >>> (32 - s))
    t4
  lsb_hex = (val) ->
    str = ""
    i = undefined
    vh = undefined
    vl = undefined
    i = 0
    while i <= 6
      vh = (val >>> (i * 4 + 4)) & 0x0f
      vl = (val >>> (i * 4)) & 0x0f
      str += vh.toString(16) + vl.toString(16)
      i += 2
    str
  cvt_hex = (val) ->
    str = ""
    i = undefined
    v = undefined
    i = 7
    while i >= 0
      v = (val >>> (i * 4)) & 0x0f
      str += v.toString(16)
      i--
    str
  Utf8Encode = (string) ->
    string = string.replace(/\r\n/g, "\n")
    utftext = ""
    n = 0

    while n < string.length
      c = string.charCodeAt(n)
      if c < 128
        utftext += String.fromCharCode(c)
      else if (c > 127) and (c < 2048)
        utftext += String.fromCharCode((c >> 6) | 192)
        utftext += String.fromCharCode((c & 63) | 128)
      else
        utftext += String.fromCharCode((c >> 12) | 224)
        utftext += String.fromCharCode(((c >> 6) & 63) | 128)
        utftext += String.fromCharCode((c & 63) | 128)
      n++
    utftext
  blockstart = undefined
  i = undefined
  j = undefined
  W = new Array(80)
  H0 = 0x67452301
  H1 = 0xEFCDAB89
  H2 = 0x98BADCFE
  H3 = 0x10325476
  H4 = 0xC3D2E1F0
  A = undefined
  B = undefined
  C = undefined
  D = undefined
  E = undefined
  temp = undefined
  msg = Utf8Encode(msg)
  msg_len = msg.length
  word_array = new Array()
  i = 0
  while i < msg_len - 3
    j = msg.charCodeAt(i) << 24 | msg.charCodeAt(i + 1) << 16 | msg.charCodeAt(i + 2) << 8 | msg.charCodeAt(i + 3)
    word_array.push j
    i += 4
  switch msg_len % 4
    when 0
      i = 0x080000000
    when 1
      i = msg.charCodeAt(msg_len - 1) << 24 | 0x0800000
    when 2
      i = msg.charCodeAt(msg_len - 2) << 24 | msg.charCodeAt(msg_len - 1) << 16 | 0x08000
    when 3
      i = msg.charCodeAt(msg_len - 3) << 24 | msg.charCodeAt(msg_len - 2) << 16 | msg.charCodeAt(msg_len - 1) << 8 | 0x80
  word_array.push i
  word_array.push 0  until (word_array.length % 16) is 14
  word_array.push msg_len >>> 29
  word_array.push (msg_len << 3) & 0x0ffffffff
  blockstart = 0
  while blockstart < word_array.length
    i = 0
    while i < 16
      W[i] = word_array[blockstart + i]
      i++
    i = 16
    while i <= 79
      W[i] = rotate_left(W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16], 1)
      i++
    A = H0
    B = H1
    C = H2
    D = H3
    E = H4
    i = 0
    while i <= 19
      temp1 = (B & C) | (~B & D)
      temp2 = rotate_left(A, 5) + temp1 + E + W[i] + 0x5A827999
      temp = temp2 & 0x0ffffffff
      E = D
      D = C
      C = rotate_left(B, 30)
      B = A
      A = temp
      i++
    i = 20
    while i <= 39
      temp = (rotate_left(A, 5) + (B ^ C ^ D) + E + W[i] + 0x6ED9EBA1) & 0x0ffffffff
      E = D
      D = C
      C = rotate_left(B, 30)
      B = A
      A = temp
      i++
    i = 40
    while i <= 59
      temp1 = (B & C) | (B & D) | (C & D)
      temp2 = rotate_left(A, 5) + temp1 + E + W[i] + 0x8F1BBCDC
      temp = temp2 & 0x0ffffffff
      E = D
      D = C
      C = rotate_left(B, 30)
      B = A
      A = temp
      i++
    i = 60
    while i <= 79
      temp = (rotate_left(A, 5) + (B ^ C ^ D) + E + W[i] + 0xCA62C1D6) & 0x0ffffffff
      E = D
      D = C
      C = rotate_left(B, 30)
      B = A
      A = temp
      i++
    H0 = (H0 + A) & 0x0ffffffff
    H1 = (H1 + B) & 0x0ffffffff
    H2 = (H2 + C) & 0x0ffffffff
    H3 = (H3 + D) & 0x0ffffffff
    H4 = (H4 + E) & 0x0ffffffff
    blockstart += 16
  temp = cvt_hex(H0) + cvt_hex(H1) + cvt_hex(H2) + cvt_hex(H3) + cvt_hex(H4)
  temp.toLowerCase()

this.serial = 
    key: (str) ->
        ### Creates a textual node key

            Arguments:
                str: the string to be formed into a key 
            
            Returns: 
                The key formed from the given string 
            
            Notes:
            
            Examples:
            
        ###
        if str.length > 10
            str.slice(0, 10) + serial.sum(str.slice(10)).slice(0,6)
        else
            str
    
    sum: (str) ->
        ### sums the string passed to it
            
            Arguments: 
                str: the string to be summed
            
            Returns:
                the integer sum of the string given
            
            Notes:
                http://stackoverflow.com/q/7538590/473479
            
            Examples:
            
        ###
        return SHA1(str)
    
    strict: (obj) ->
        # does nothing whatsoever :) 
        throw "serial.strict is not yet implemented"        

this.assert = (condition, message) ->
    ### throws an error if the condition passed is not true. Optionally provide
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
    ###

    message = if message isnt "" then "Assertion error: '#{message}'" else 'Assertion error'
    if not condition then throw message
