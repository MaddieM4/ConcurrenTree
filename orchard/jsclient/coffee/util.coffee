# util.coffee :: Utilities

# Dependencies: A BCP object must be available to handle md5 requests

arrayFill = (array, value, count) ->
    ### Fills an array with the values returned by value when given an index
    
        Arguments:
            array: the array to be extended
            value: a function returning the value to be appended when given an       
                index possible index values being between 0 and count exclusive 
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
    array.push value i for i in [0 ... count]
    array

af_object = (id) -> # I have no idea why this function exists :)
    {}

isArray = (obj) ->
    # tests if an object is an array
    if typeof obj is "object" 
        Object.prototype.toString.call(obj) is "[object Array]"
    else
        false

isObject = (obj) ->
    # tests if an object is a hash/dictionary type object
    if typeof obj is "object"
        Object.prototype.toString.call(obj) is "[object Object]"
    else
        false

isNumber = (obj) ->
    # tests if an object is a number
    typeof obj is "number"

isBoolean = (obj) ->
    ### tests if an object is a boolean object
        
        Note! This does not test if an object can resolve to a boolean, it 
        tests whether it is a boolean object. 
        This test is equivalent to 
        if obj is true or obj is false then true else false
        
        JS Condition (obj === true || obj === false), not '=='! 
    ###
    typeof obj is "boolean"

range = (start, end, step = 1) ->
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

urlParameters = (url = window.location.href) ->
    ### extracts a dictionary of url parameters from the given url
        
        Arguments:
            url: a url to parse parameters from. (Optional, default = 
                window.location.href)
        
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
get_url_variable = getUrlParameter = (name, def) -> 
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

isJSON = (str) ->
    # tests if the suppled string is valid JSON
    # Arguments: str: a string. 
    # Returns: true/false
    try
        JSON.parse str
        true
    catch e
        false

serial = 
    key: (str) ->
        # I don't know what this function does
        ###
            Arguments:
                str: the string to be formed into a key 
            
            Returns: 
                The key formed from the given string 
            
            Notes:
            
            Examples:
            
        ###
        if str.length > 10
            str.slice(0, 10) + serial.sum(str.slice(10))
        else
            str
    
    modulo: 65536 # 2^8? This is 2^16
    
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
        s = 0 
        for i in [0... str.length] 
            s = (s * s + str.charCodeAt(i)) % serial.modulo
        s 
    
    strict: (obj) ->
        # does nothing whatsoever :) 
        
assert = (condition, message) ->
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
        
