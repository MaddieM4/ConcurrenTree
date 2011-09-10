# chainer.coffee

# dependancies: none

class Chainer
    ### 
    A chaining wrapper for the tree. Call s on it like a regular tree.
    For properties, use mychain.tree.propertyname
    ###
    constructor: (tree) ->
        @tree = tree
        @lastpos = undefined
        @startpos = undefined
        @chain = ""
    insert: (pos, childtext) ->
        @apply()
        @tree.insert pos, childtext
    delete: (pos) -> 
        @apply()
        @tree.delete pos
    get: (pos, hash) ->
        @apply()
        @tree.get pos, hash
    flatten: () ->
        @apply()
        @tree.flatten()      
    trace: (pos) -> 
        @apply()
        @tree.trace pos
    untrace: (addr, pos) ->
        @apply()
        @tree.untrace addr, pos
    resolve: (addrstring) -> 
        @apply()
        @tree.resolve addrstring
    kidscan: -> 
        @apply()
        @tree.kidscan()
    flatinsert: (pos, value) ->
        if @startpos is undefined
            @startpos = pos
            @lastpos = pos
            @chain += value
        else if pos is @lastpos + 1
            @chain += value
            @lastpos = pos
        else
            @apply()
            @tree.flatinsert pos, value
        return
    flatdelete: (pos) ->
        if @startpos isnt undefined and pos is @lastpos
            @chain = @chain.substr 0, chain.length-1
        else
            @apply()
            @tree.flatdelete pos
    flatreplace: (start, end, value) ->
        @apply()
        @tree.flatreplace start, end, value
    apply: ->
        if @chain isnt ""
            @tree.flatinsert @startpos, @chain
            @startpos = undefined
            @lastpos = undefined
            @chain = ""
console.log "test"