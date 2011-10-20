# util.test.coffee :: tests for util.coffee

# Test arrayfill

tests = 
    arrayFill: ->
        ### test case 1
            padding with zeroes
            tests with a function which always returns none
        ###
        testcase = [0, 0, 0, 0, 0, 0, 0] 
        output = arrayFill [], (-> 0), 7
        result = if testcase is output then 'successful' else 'failed'
        console.log "arrayFill #1 #{result}"
        ### test case 2
            padding with index
        ###
        testcase = [0, 1, 2, 3, 4, 5]
        output = arrayFill [], ((i) -> i), 6
        result = if testcase is output then 'successful' else 'failed'
        console.log "arrayFill #2 #{result}"
        ### test case 3
            negative value of count
        ###
        testcase = [0, -1, -2, -3] 
        output = arrayFill [], ((i) -> i), 4
        result = if testcase is output then 'successful' else 'failed'
        console.log "arrayFill #3 #{result}"
    af_object: ->
        ### test case 1 
        ###
        testcase = {}
        output = af_object(null)
        result = if testcase is output then 'successful' else 'failed'
        console.log "af_object #1 #{result}"
    isArray: ->
        ### test suite
            [] returns true
        ###
        testcasesTrue = [
            [] # array evaluating to false
            [undefined] # arrays evaluating to true
            [null]
            [0]
            [false]
            ['']
            [[]]
            [{}]
            ['test']
            ]
        testcasesFalse = [
            {}
            0
            1
            true
            false
            ''
            'hello, world'
            undefined
            null
            ]
        for i in testcasesTrue
            if isArray i
                console.log "isArray test successful: #{i} is an Array"
            else
                console.log "isArray test FAILED: #{i} is an Array"
        for i in testcasesFalse
            if isArray i
                console.log "isArray test FAILED: #{i} is NOT an Array"
            else
                console.log "isArray test successful: #{i} is not an Array"
            
            
            
            
        