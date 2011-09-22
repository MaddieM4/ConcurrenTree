# util.coffee :: Utilities

# Dependencies: A BCP object must be available to handle md5 requests

arrayFill = (array, value, count) ->
    ###
        array: the array to be extended
        value: a function returning the value to be appended when given an index
            possible index values being between 0 and count exclusive of count
        count: the number of values to append
        
        returns the given array
        
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
    if typeof obj is "object" 
        Object.prototype.toString.call(obj) is "[object Array]"
    else
        false

isObject = (obj) ->
    if typeof obj is "object"
        Object.prototype.toString.call(obj) is "[object Object]"
    else
        false

isNumber = (obj) ->
    typeof obj is "number"

isBoolean = (obj) ->
    typeof obj is "boolean"

range = (start, end, step = 1) ->
    i for i in [start... max] by step

urlParameters = (url = window.location.href) ->
    params = {}
    pairs = url.slice(url.indexOf('?') + 1).split('&')
    for i in pairs
        kv = i.split('=')
        params[kv[0]] = if kv.length > 1 then kv[1] else null
    params

get_url_variable = getUrlParameter = (name, def) -> 
    # get_url_variable is a pythonic name, variable should be parameter
    # recommend changing
    params = urlParameters()
    if params[name] isnt undefined then params[name] else def

isJSON = (str) ->
    try
        JSON.parse str
        true
    catch e
        false





