# buffer.coffee  :: Implements python like queue

# Dependancies: none

class Buffer
    constructor: ->
        @readposition = 0
        @writeposition = 0
        @_contents = {}
        @readlock = off
    write: (value) ->
        pos = ++@writeposition
        @_contents[pos - 1] = value
    read: ->
        if @readlock then return undefined
        @readlock = on
        read = @readposition
        write = @writeposition
        if read < write
            result = @_contents[read]
            delete @_contents[read]
            @readposition++
        @readlock = off
        result
    read_all: ->
        result = []
        value = @read()
        until value is undefined
            result.push(value)
            value = @read()
        result
        
